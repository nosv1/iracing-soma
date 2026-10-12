"""Throwaway: does a local LLM hurt iRacing frame rate in VR?

Start at the desk, get in the rig. Waits until you're on track, then steps through
phases on its own and announces each one through Piper so the headset stays on.

    env/Scripts/python bench/gpu_contention.py            # real run (~15 min of laps)
    env/Scripts/python bench/gpu_contention.py --quick    # desk dry run, 10 s phases, no on-track wait

Writes bench/runs/<timestamp>/{phases,telemetry,gpu,llm}.csv, all keyed on t (s since start).
"""

import argparse
import csv
import json
import random
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import irsdk
import sounddevice as sd
from piper import PiperVoice

sys.path.insert(0, str(Path(__file__).parent.parent))  # repo root, for src/
from src.irsdk_vars import CPU_USAGE_FG, FRAME_RATE, GPU_USAGE, IS_ON_TRACK, SESSION_TIME

OLLAMA = "http://127.0.0.1:11434"
VOICE = Path(__file__).parent.parent / "voices" / "en_GB-southern_english_female-low.onnx"
SMALL, BIG = "llama3.2:3b", "llama3.1:8b"

# (name, minutes, model, mode); mode: none | idle | periodic | continuous
PHASES = [
    ("baseline", 2, None, "none"),
    ("small idle", 2, SMALL, "idle"),
    ("small periodic", 3, SMALL, "periodic"),
    ("small continuous", 3, SMALL, "continuous"),
    ("big periodic", 2, BIG, "periodic"),
    ("big continuous", 2, BIG, "continuous"),
    ("baseline again", 1, None, "none"),
]
PERIODIC_INTERVAL_S = 12

SYSTEM = "You are a calm race engineer on the radio. Reply with one short sentence. Use the numbers exactly as given."

T0 = time.perf_counter()


def now() -> float:
    return round(time.perf_counter() - T0, 3)


class CsvLog:
    def __init__(self, path: Path, fields: list[str]):
        self.f = open(path, "w", newline="")
        self.w = csv.DictWriter(self.f, fields)
        self.w.writeheader()
        self.lock = threading.Lock()

    def row(self, **kw):
        with self.lock:
            self.w.writerow({"t": now(), **kw})
            self.f.flush()


# ---------- announcements ----------

voice = PiperVoice.load(str(VOICE))


def say(text: str):
    print(f"[{now():7.1f}] SAY: {text}")
    for chunk in voice.synthesize(text):
        sd.play(chunk.audio_float_array, chunk.sample_rate)
        sd.wait()


# ---------- ollama ----------

def post(path: str, body: dict, stream: bool = False):
    req = urllib.request.Request(
        OLLAMA + path, json.dumps(body).encode(), {"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=300)
    return resp if stream else json.loads(resp.read())


def load(model: str):
    post("/api/generate", {"model": model, "keep_alive": "60m"})


def unload_all():
    for m in (SMALL, BIG):
        post("/api/generate", {"model": m, "keep_alive": 0})


def fake_facts() -> dict:
    return random.choice([
        {"event": "gap_ahead", "position": random.randint(2, 15), "gap_s": round(random.uniform(0.3, 4), 1), "trend": random.choice(["closing", "opening"])},
        {"event": "caught", "car_number": random.randint(1, 99), "gained_s": round(random.uniform(0.1, 1.5), 1)},
        {"event": "fuel", "laps_left": round(random.uniform(2, 12), 1), "laps_remaining_in_race": random.randint(3, 20)},
    ])


def generate(model: str, llm: CsvLog, phase: str, num_predict: int):
    facts = fake_facts()
    body = {
        "model": model, "system": SYSTEM, "prompt": json.dumps(facts), "stream": True,
        "keep_alive": "60m", "options": {"num_predict": num_predict, "temperature": 0.3},
    }
    t_send = time.perf_counter()
    ttft, text, final = None, [], {}
    with post("/api/generate", body, stream=True) as resp:
        for line in resp:
            msg = json.loads(line)
            if ttft is None and msg.get("response"):
                ttft = time.perf_counter() - t_send
            text.append(msg.get("response", ""))
            if msg.get("done"):
                final = msg
    total = time.perf_counter() - t_send
    eval_n, eval_ns = final.get("eval_count", 0), final.get("eval_duration", 1)
    llm.row(phase=phase, model=model, ttft_s=round(ttft or -1, 3), total_s=round(total, 3),
            tokens=eval_n, tok_per_s=round(eval_n / (eval_ns / 1e9), 1),
            facts=json.dumps(facts), reply="".join(text).strip())


def llm_worker(model, mode, stop: threading.Event, llm: CsvLog, phase: str):
    while not stop.is_set():
        if mode == "periodic":
            generate(model, llm, phase, num_predict=40)
            stop.wait(PERIODIC_INTERVAL_S)
        elif mode == "continuous":
            generate(model, llm, phase, num_predict=200)


# ---------- samplers ----------

def telemetry_sampler(ir: irsdk.IRSDK, stop: threading.Event, tel: CsvLog, hz=10):
    while not stop.is_set():
        if ir.is_initialized and ir.is_connected:
            ir.freeze_var_buffer_latest()
            tel.row(session_time=ir[SESSION_TIME], on_track=ir[IS_ON_TRACK],
                    frame_rate=ir[FRAME_RATE], gpu_usage=ir[GPU_USAGE], cpu_fg=ir[CPU_USAGE_FG])
        else:
            ir.startup()
        stop.wait(1 / hz)


def start_gpu_sampler(gpu: CsvLog) -> subprocess.Popen:
    p = subprocess.Popen(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,clocks.gr,temperature.gpu",
         "--format=csv,noheader,nounits", "-lms", "500"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True,
    )

    def read():
        for line in p.stdout:
            util, mem, clk, temp = (s.strip() for s in line.split(","))
            gpu.row(util_pct=util, mem_mib=mem, clock_mhz=clk, temp_c=temp)

    threading.Thread(target=read, daemon=True).start()
    return p  # caller must terminate it, or nvidia-smi outlives the script


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="10 s phases, don't wait for on-track")
    args = ap.parse_args()

    out = Path(__file__).parent / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    phases = CsvLog(out / "phases.csv", ["t", "event", "phase", "model", "mode"])
    tel = CsvLog(out / "telemetry.csv", ["t", "session_time", "on_track", "frame_rate", "gpu_usage", "cpu_fg"])
    gpu = CsvLog(out / "gpu.csv", ["t", "util_pct", "mem_mib", "clock_mhz", "temp_c"])
    llm = CsvLog(out / "llm.csv", ["t", "phase", "model", "ttft_s", "total_s", "tokens", "tok_per_s", "facts", "reply"])
    print(f"logging to {out}")

    ir = irsdk.IRSDK()
    stop_all = threading.Event()
    threading.Thread(target=telemetry_sampler, args=(ir, stop_all, tel), daemon=True).start()
    smi = start_gpu_sampler(gpu)

    unload_all()
    say("Contention test armed.")

    if not args.quick:
        say("Waiting for you to get on track.")
        while not (ir.is_connected and ir[IS_ON_TRACK]):
            time.sleep(1)
        say("On track. Settle in, starting in thirty seconds.")
        time.sleep(30)

    try:
        for i, (name, minutes, model, mode) in enumerate(PHASES, 1):
            duration = 10 if args.quick else minutes * 60
            if model is None:
                unload_all()
            elif mode == "idle" or model != PHASES[i - 2][2]:
                unload_all()
                load(model)
            say(f"Phase {i} of {len(PHASES)}: {name}. {minutes} minute{'s' if minutes != 1 else ''}.")
            phases.row(event="start", phase=name, model=model, mode=mode)

            stop = threading.Event()
            worker = threading.Thread(target=llm_worker, args=(model, mode, stop, llm, name), daemon=True)
            worker.start()
            time.sleep(duration)
            stop.set()
            worker.join()
            phases.row(event="end", phase=name, model=model, mode=mode)

        unload_all()
        say("Test complete. You can get out.")
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        stop_all.set()
        smi.terminate()
        print(f"logs in {out}")


if __name__ == "__main__":
    main()
