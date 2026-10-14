import argparse
import logging
import sys
import time
from pathlib import Path

import sounddevice
from piper import PiperVoice

from soma.car import Car
from soma.iracing import iRacing
from soma.irsdk_vars import PLAYER_CAR_IDX
from soma.loader import Loader
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


def main(record_path: Path | None, recordings_path: Path | None) -> None:
    loader: Loader | None = None
    if recordings_path is not None:
        loader = Loader(recordings_path=recordings_path)

    if loader is None:
        ir = iRacing()
        ir.connect()

    cur_dir = Path(__file__).resolve().parent
    voices_dir = cur_dir / "voices"
    voice_path = voices_dir / "en_GB-southern_english_female-low.onnx"
    voice = PiperVoice.load(voice_path)

    recorder: Recorder | None = None
    # creating this file stops the loop cleanly (finally still flushes the recorder)
    stop_file = (record_path or Path.cwd()) / "STOP"
    stop_file.unlink(
        missing_ok=True
    )  # a leftover from last run would stop us immediately
    next_stop_check = 0.0
    logger.info(f"create {stop_file} to stop")

    session: Session | None = None
    reconnect_timer = 1

    try:
        while True:
            # check about once a second; the loop spins far faster than that
            now = time.monotonic()
            if now >= next_stop_check:
                if stop_file.exists():
                    logger.info("stop file found, stopping")
                    break
                next_stop_check = now + 1.0

            if ir.ir.is_connected:
                if loader is None:
                    if recorder is None and record_path is not None:
                        # starts recorder thread
                        recorder = Recorder(
                            output_dir=record_path,
                            recorded_fps=10,
                            iracing_fps=ir.ir._header.tick_rate,
                        )

                    # freeze data stream
                    ir.ir.freeze_var_buffer_latest()

                    if recorder is not None:
                        recorder.handle_new_tick(ir)

                # session = Session.from_dict(ir.ir)

                # unfreeze data stream
                if loader is None:
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
        if loader is None:
            ir.disconnect()

        if recorder is not None:
            recorder.q.put(recorder.STOP)
            recorder._t.join()

    # chunk_array = voice.synthesize(f"player car index is {player_car.idx}")

    # for chunk in chunk_array:
    #     sounddevice.play(chunk.audio_float_array, chunk.sample_rate)
    #     sounddevice.wait()


if __name__ == "__main__":
    cli()
