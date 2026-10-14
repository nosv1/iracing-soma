import argparse
import sys
from pathlib import Path

import sounddevice
from piper import PiperVoice

from soma.car import Car
from soma.iracing import iRacing
from soma.irsdk_vars import PLAYER_CAR_IDX
from soma.recorder import Recorder
from soma.session import Session


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
    args = parser.parse_args()
    main(args.record)


def main(record_path: Path | None) -> None:
    ir = iRacing()
    ir.connect()

    cur_dir = Path(__file__).resolve().parent
    voices_dir = cur_dir / "voices"
    voice_path = voices_dir / "en_GB-southern_english_female-low.onnx"
    voice = PiperVoice.load(voice_path)

    session: Session | None = None
    recorder: Recorder | None = None
    if record_path is not None:
        # starts recorder thread
        recorder = Recorder(record_path)

    try:
        while True:
            if recorder is not None:
                recorder.record_iRacing_session_yaml(ir)
                recorder.queue_iRacing_frame(ir)

            session = Session.from_irsdk(ir.ir)

            if not ir.state.is_ir_connected:
                break

    finally:
        if recorder is not None:
            recorder.q.put(recorder.STOP)
            recorder.t.join()

    # chunk_array = voice.synthesize(f"player car index is {player_car.idx}")

    # for chunk in chunk_array:
    #     sounddevice.play(chunk.audio_float_array, chunk.sample_rate)
    #     sounddevice.wait()


if __name__ == "__main__":
    cli()
