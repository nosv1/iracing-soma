import pytest

from soma.session_type import SessionType


def test_unknown_session_type() -> None:
    unknown_session = SessionType("TEST_UNKNOWN")
    assert unknown_session == SessionType.UNKNOWN


def test_new_session_num_is_session_change() -> None:
    # Recording used: none (build in code; P -> Q on one server: SessionNum 0 -> 1,
    #   same SubSessionID)
    pytest.fail("TODO: SessionNum 0 -> 1, same SubSessionID -> one SessionChanged")


def test_new_sub_session_id_is_session_change() -> None:
    # Recording used: none (build in code; server switch as in 20261019-175649: SessionNum
    #   stays 0, SubSessionID 89493421 -> 89494186)
    pytest.fail("TODO: SubSessionID changes, same SessionNum -> one SessionChanged")


def test_session_change_fires_once() -> None:
    # Recording used: none (build in code; P -> Q, then more frames of Q)
    pytest.fail(
        "TODO: SessionNum 0 -> 1, then 3 more frames at 1 -> exactly one"
        " SessionChanged in total"
    )


def test_one_session_no_session_change() -> None:
    # Recording used: tests/recordings/rolling_start (one session, SessionNum 2 throughout)
    pytest.fail("TODO: every frame of rolling_start -> no SessionChanged")


def test_player_car_idx_follows_server_switch() -> None:
    # Recording used: recordings/20261019-175649 (gitignored), no fixture yet; spans two
    #   servers (SessionTime resets), so trim_recording.py can't cut it as is
    pytest.fail("TODO: PlayerCarIdx 35 -> 18 mid-stream -> player_car_idx follows")
