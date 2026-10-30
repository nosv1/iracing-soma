import pytest

from soma.session import Session

# Rolling start, 10-20 race (recording 20261020-120232): CarIdxLapCompleted goes -1 -> 0
# with a pct wrap at the green; today that is counted as a completed lap.


def test_start_crossing_is_not_a_lap(rolling_start_session: Session) -> None:
    player_race_laps = rolling_start_session.player_car.laps[
        rolling_start_session.player_car.session_num
    ]
    assert player_race_laps[1].estimated_timestamp == pytest.approx(155.83, abs=0.01)


def test_first_lap_counts_after_start() -> None:
    # recording: tests/recordings/rolling_start
    pytest.fail("TODO: start crossing, then 0 -> 1 + wrap -> 1 lap completed")


def test_no_caught_call_after_first_lap() -> None:
    # recording: tests/recordings/rolling_start
    pytest.fail("TODO: green, then 1 full lap -> no CaughtFact (needs 2 full laps)")
