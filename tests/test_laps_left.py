import pytest

# Laps left. Every recorded race so far is timed (YAML SessionLaps "unlimited",
# SessionLapsRemainEx 32767). End-of-race fixtures can't be cut yet: trim_recording.py
# keeps only the vars src/soma reads, so cut them once the code reads SessionTimeRemain.


def test_timed_race_detected() -> None:
    # Recording used: tests/recordings/rolling_start (YAML SessionLaps: unlimited)
    pytest.fail("TODO: race with SessionLaps 'unlimited' -> timed race")


def test_lap_race_detected() -> None:
    # Recording used: none (no lap-count race recorded yet; build the session in code)
    pytest.fail("TODO: race with SessionLaps 15 -> lap race, not timed")


def test_two_to_go_spoken_once() -> None:
    # Recording used: recordings/20261020-112829 (gitignored), race end; not trimmed yet
    pytest.fail(
        "TODO: whole race end -> exactly one 2-to-go fact,"
        " at the player's crossing before white"
    )


def test_one_to_go_on_white() -> None:
    # Recording used: recordings/20261020-112829 (gitignored), race end; not trimmed yet
    pytest.fail("TODO: player's WHITE turns on -> exactly one 1-to-go fact")


def test_time_runs_out_with_leader_at_line() -> None:
    # Recording used: none (build in code)
    pytest.fail(
        "TODO: time hits 0 with leader < 1 s from the line"
        " -> (your call: what Soma says)"
    )


# Session.estimate_laps_left. Design (2026-11-24): extrapolate from the leader's last
# line crossing (its estimated_timestamp), not from where the leader is in the lap now.
# Finish rule still unmeasured: is the first crossing after time runs out the
# checkered, or the white? That decides the "+ 1".


def test_laps_left_from_last_crossing() -> None:
    # Recording used: none (build in code; leader with a best lap and a last crossing)
    pytest.fail(
        "TODO: known time left at the leader's last crossing and best lap"
        " -> laps left by hand (your call: best-lap or last-lap pace)"
    )


def test_laps_left_steady_through_the_lap() -> None:
    # Recording used: none (build in code; same crossing, later session_time / lap_dist)
    pytest.fail(
        "TODO: same lap, time passes and the leader is slower than best"
        " -> estimate doesn't move"
    )


def test_laps_left_last_lap_when_time_runs_out_mid_lap() -> None:
    # Recording used: none (build in code; crossed with less than a lap of time left)
    pytest.fail("TODO: time hits 0 mid-lap -> 1 (or 2: the finish rule)")


def test_laps_left_none_before_best_lap() -> None:
    # Recording used: none (build in code; one crossing, no lap time)
    pytest.fail("TODO: leader's opening lap, no best lap yet -> None")


def test_laps_left_none_without_laps_this_session() -> None:
    # Recording used: none (build in code; leader hasn't crossed the line this session)
    pytest.fail("TODO: no laps for session_num -> None")


def test_laps_left_without_p1() -> None:
    # Recording used: none (build in code; empty positions). Today: KeyError at session.py:109
    pytest.fail("TODO: no P1 in positions -> (your call: None, or raise)")
