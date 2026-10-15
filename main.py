import argparse
import logging
import sys
import time
from pathlib import Path

import sounddevice
from irsdk import IRSDK
from piper import PiperVoice

from soma.car import Car
from soma.iracing import iRacing
from soma.irsdk_vars import PLAYER_CAR_IDX
from soma.loader import Loader, Snapshot
from soma.recorder import Recorder
from soma.session import Session

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def cli() -> None:
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument(
        "-r",
        "--record",
        nargs="?",
        const="./recordings",
        default=None,
        type=Path,
        metavar="DIR",
        help="record iRacing data",
    )
    parser.add_argument(
        "-l",
        "--load",
        nargs="?",
        default=None,
        type=Path,
        metavar="DIR",
        help="directory holding the recording to load (probably timestamped)",
    )
    args = parser.parse_args()
    main(args.record, args.load)


def check_stop_loop(next_stop_check: float, stop_file: Path) -> bool | float:
    # check about once a second; the loop spins far faster than that
    now = time.monotonic()
    if now >= next_stop_check:
        if stop_file.exists():
            logger.info("stop file found, stopping")
            return True
        next_stop_check = now + 1.0

    return next_stop_check


def handle_frame(frame: IRSDK | Snapshot, voice: PiperVoice) -> Session:
    session = Session.from_frame(frame)
    return session


def loop_recording(loader: Loader, voice: PiperVoice) -> None:
    logger.info(f"looping recording: {loader.recording_path}")
    session: Session | None = None
    for frame in loader.snapshots():
        session = handle_frame(frame, voice)


def loop_iracing_stream(
    stop_file: Path, recorder: Recorder | None, voice: PiperVoice
) -> None:
    ir = iRacing()
    ir.connect()

    session: Session | None = None
    reconnect_timer = 1
    next_stop_check = 0.0

    try:
        while True:
            do_stop_loop: bool | float = check_stop_loop(next_stop_check, stop_file)
            if isinstance(do_stop_loop, bool) and do_stop_loop:
                break
            elif isinstance(do_stop_loop, float):
                next_stop_check = do_stop_loop

            if ir.ir.is_connected:
                # freeze data stream
                ir.ir.freeze_var_buffer_latest()

                if recorder is not None:
                    recorder.handle_new_tick(ir)

                session = handle_frame(ir.ir, voice)

                # unfreeze data stream
                ir.ir.unfreeze_var_buffer_latest()

            # iRacing disconnected
            else:
                ir.disconnect()
                reconnect_timer *= 2
                reconnect_timer = min(30, reconnect_timer)
                logger.info(f"Attempting to re-connect in {reconnect_timer} seconds...")
                time.sleep(reconnect_timer)
                ir.connect()
    finally:
        ir.disconnect()

        if recorder is not None:
            recorder.q.put(recorder.STOP)
            recorder._t.join()


def main(record_path: Path | None, recording_path: Path | None) -> None:
    cur_dir = Path(__file__).resolve().parent
    voices_dir = cur_dir / "voices"
    voice_path = voices_dir / "en_GB-southern_english_female-low.onnx"
    voice = PiperVoice.load(voice_path)

    # creating this file stops the loop cleanly (finally still flushes the recorder)
    stop_file = (record_path or Path.cwd()) / "STOP"
    stop_file.unlink(
        missing_ok=True
    )  # a leftover from last run would stop us immediately
    logger.info(f"create {stop_file} to stop")

    # loop recording
    if recording_path is not None:
        loader = Loader(recording_path=recording_path)
        loop_recording(loader, voice)

    # loop iracing stream
    else:
        recorder: Recorder | None = None
        if record_path is not None:
            recorder = Recorder(record_path, iracing_fps=60, recorded_fps=10)
        loop_iracing_stream(stop_file, recorder, voice)


if __name__ == "__main__":
    cli()
