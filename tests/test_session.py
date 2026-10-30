import pytest

from soma.session_type import SessionType


def test_unknown_session_type() -> None:
    unknown_session = SessionType("TEST_UNKNOWN")
    assert unknown_session == SessionType.UNKNOWN


def test_player_car_idx_follows_server_switch() -> None:
    # recording: recordings/20261019-175649 (gitignored), no fixture yet; spans two
    #   servers (SessionTime resets), so trim_recording.py can't cut it as is
    pytest.fail("TODO: PlayerCarIdx 35 -> 18 mid-stream -> player_car_idx follows")
