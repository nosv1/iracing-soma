import pytest

from soma.session_type import SessionType


def test_unknown_session_type() -> None:
    unknown_session = SessionType("TEST_UNKNOWN")
    assert unknown_session == SessionType.UNKNOWN


def test_player_car_idx_follows_server_switch() -> None:
    pytest.fail("TODO: PlayerCarIdx 35 -> 18 mid-stream -> player_car_idx follows")
