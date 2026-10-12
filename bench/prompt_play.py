"""Prompt playground: edit SYSTEM, EXAMPLES and FACTS, run, compare models.

uv run bench/prompt_play.py
uv run bench/prompt_play.py --speak    # also read each reply aloud with Piper
"""

import argparse
import json
from pathlib import Path

import ollama

MODELS = ["llama3.2:3b", "llama3.1:8b"]
OPTIONS = {"temperature": 0.3, "num_predict": 60}

SYSTEM = """You are a calm race engineer on the radio to your driver.
Convert the JSON to a speakable. Use the numbers exactly as given. Add nothing else.
"""

# (facts, reply) pairs, sent as earlier user/assistant turns before the real facts
EXAMPLES = [
    (
        {"event": "caught", "driver_ahead": "Smith", "gained_s": 0.2},
        "Caught Smith by 0.2 seconds",
    ),
    (
        {"event": "gap_ahead", "to_position": 1, "gap_s": 1.2, "trend": "decreasing"},
        "gap to P1 ahead is decreasing, now at 1.2 seconds",
    ),
    (
        {
            "event": "fuel_short",
            "laps_of_fuel": 6.5,
            "race_laps_remaining": 9,
            "options": [
                {"action": "save", "save_per_lap_pct": 23},
                {"action": "pit", "by_lap": 6, "add_l": 3},
            ],
        },
        "Fuel's short, six and a half laps for nine to go. "
        "Save twenty-eight percent a lap, or box by lap six for twelve litres.",
    ),
]


def build_messages(facts: dict) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM}]
    for example_facts, reply in EXAMPLES:
        messages.append({"role": "user", "content": json.dumps(example_facts)})
        messages.append({"role": "assistant", "content": reply})
    messages.append({"role": "user", "content": json.dumps(facts)})
    return messages


FACTS = [
    {"event": "caught", "driver_ahead": "Smith", "gained_s": 0.8},
    {"event": "gap_ahead", "to_position": 4, "gap_s": 1.3, "trend": "closing"},
    {"event": "fuel_status", "laps_of_fuel": 6.5, "laps_remaining": 9},
]

VOICES_DIR = Path(__file__).parent.parent / "voices"
VOICE = VOICES_DIR / "en_GB-southern_english_female-low.onnx"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speak", action="store_true")
    args = ap.parse_args()

    if args.speak:
        import sounddevice as sd
        from piper import PiperVoice

        voice = PiperVoice.load(str(VOICE))

    for facts in FACTS:
        print(f"\n{json.dumps(facts)}")
        for model in MODELS:
            r = ollama.chat(
                model=model, messages=build_messages(facts), options=OPTIONS
            )
            reply = r.message.content.strip()
            secs = r.total_duration / 1e9
            print(f"  {model:12} {secs:5.2f}s {r.prompt_eval_count:4} tok  {reply}")
            if args.speak:
                for chunk in voice.synthesize(reply):
                    sd.play(chunk.audio_float_array, chunk.sample_rate)
                    sd.wait()


if __name__ == "__main__":
    main()
