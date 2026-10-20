import pytest

# Rolling start, 10-20 race (recording 20261020-120232): CarIdxLapCompleted goes -1 -> 0
# with a pct wrap at the green; today that is counted as a completed lap.


def test_start_crossing_is_not_a_lap() -> None:
    pytest.fail("TODO: -1 -> 0 + pct wrap at the green -> 0 laps completed")


def test_first_lap_counts_after_start() -> None:
    pytest.fail("TODO: start crossing, then 0 -> 1 + wrap -> 1 lap completed")


def test_no_caught_call_after_first_lap() -> None:
    pytest.fail("TODO: green, then 1 full lap -> no CaughtFact (needs 2 full laps)")
