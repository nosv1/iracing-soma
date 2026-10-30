from pathlib import Path

import pytest

RECORDINGS = Path(__file__).parent / "recordings"


def test_every_yaml_tick_is_a_frame_tick() -> None:
    # recording: recordings/* (gitignored, real recorder output); tests/recordings/valid
    pytest.fail("TODO: every index.json tick is also a recorded frame tick")
