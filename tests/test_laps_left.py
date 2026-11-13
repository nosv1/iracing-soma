import pytest

# Laps left. Every recorded race so far is timed (YAML SessionLaps "unlimited",
# SessionLapsRemainEx 32767). End-of-race fixtures can't be cut yet: trim_recording.py
# keeps only the vars src/soma reads, so cut them once the code reads SessionTimeRemain.


def test_timed_race_detected() -> None:
    # recording: tests/recordings/rolling_start (YAML SessionLaps: unlimited)
    pytest.fail("TODO: race with SessionLaps 'unlimited' -> timed race")


def test_lap_race_detected() -> None:
    # recording: none (no lap-count race recorded yet; build the session in code)
    pytest.fail("TODO: race with SessionLaps 15 -> lap race, not timed")


def test_two_to_go_spoken_once() -> None:
    # recording: recordings/20261020-112829 (gitignored), race end; not trimmed yet
    pytest.fail(
        "TODO: whole race end -> exactly one 2-to-go fact,"
        " at the player's crossing before white"
    )


def test_one_to_go_on_white() -> None:
    # recording: recordings/20261020-112829 (gitignored), race end; not trimmed yet
    pytest.fail("TODO: player's WHITE turns on -> exactly one 1-to-go fact")


def test_time_runs_out_with_leader_at_line() -> None:
    # recording: none (build in code)
    pytest.fail(
        "TODO: time hits 0 with leader < 1 s from the line"
        " -> (your call: what Soma says)"
    )
