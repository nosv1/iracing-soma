import sys
from pathlib import Path

import sounddevice
from piper import PiperVoice

from soma.car import Car
from soma.iracing import iRacing
from soma.irsdk_vars import PLAYER_CAR_IDX


def main(args: list[str]) -> None:
    ir = iRacing()
    ir.check_iracing()

    cur_dir = Path(__file__).resolve().parent
    voices_dir = cur_dir / "voices"
    voice_path = voices_dir / "en_GB-southern_english_female-low.onnx"
    voice = PiperVoice.load(voice_path)

    player_car = Car(idx=ir.ir[PLAYER_CAR_IDX])

    chunk_array = voice.synthesize(f"player car index is {player_car.idx}")

    for chunk in chunk_array:
        sounddevice.play(chunk.audio_float_array, chunk.sample_rate)
        sounddevice.wait()


if __name__ == "__main__":
    main(sys.argv)
