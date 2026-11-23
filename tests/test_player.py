import pytest

from soma.do_stuff import StuffPacket, do_stuff
from soma.event import ReachedRaceDistanceMilestone
from soma.loader import Loader
from soma.player import (
    Player,
    PlayerConstants,
    RaceDistanceMilestoneAsLap,
    RaceDistanceMilestoneAsPercentRemaining,
)
from soma.session import Session

# Player: per-player constants (race milestones) and which of them have fired.
# Design (2026-11-17): one sorted list per milestone type, a fresh deep copy per session
# (SessionUniqueID change), pop every milestone reached, say at most one per lap.
# Detection and popping happen in Player.handle_frame (after Session and Car);
# handle_player_events only turns player.events into facts.


def test_first_session_is_armed() -> None:
    # recording: none (build in code)
    player_constants = PlayerConstants(race_milestones=[RaceDistanceMilestoneAsLap(5)])
    player = Player(player_constants)
    assert id(player.race_milestones) != id(player.player_constants.race_milestones)
    assert len(player.race_milestones) == 1
    assert isinstance(player.race_milestones[0], RaceDistanceMilestoneAsLap)
    assert player.race_milestones[0].laps_remaining == 5

    # pytest.fail(
    #     "Player(constants) -> player_constants_for_session equals constants,"
    #     " before any SessionChanged"
    # )


def test_session_copy_is_not_the_constants() -> None:
    # recording: none (build in code)
    player_constants = PlayerConstants(
        race_milestones=[RaceDistanceMilestoneAsLap(5), RaceDistanceMilestoneAsLap(3)]
    )
    player = Player(player_constants)
    player.race_milestones = player.race_milestones[1:]
    assert len(player.race_milestones) + 1 == len(player_constants.race_milestones)

    # pytest.fail(
    #     "pop a milestone from the session copy -> player.player_constants"
    #     " still has every milestone"
    # )


def test_session_change_resets_milestones() -> None:
    # recording: none (two sessions with different session_uid, built in code)
    player_constants = PlayerConstants(
        race_milestones=[RaceDistanceMilestoneAsLap(5), RaceDistanceMilestoneAsLap(3)]
    )
    player = Player(player_constants)
    player.race_milestones = player.race_milestones[1:]
    player.handle_session_change()
    assert len(player.race_milestones) == len(player.player_constants.race_milestones)
    # pytest.fail(
    #     "pop a milestone, then a SessionChanged -> session copy is full again"
    # )


def test_no_milestones_no_crash(laps_p3_loader: Loader) -> None:
    # recording: tests/recordings/laps_p3 (test_caught_call hits this today:
    # IndexError at player.py race_milestones[0])
    session: Session | None = None
    packet: StuffPacket | None = None
    player = Player(PlayerConstants(race_milestones=[]))
    milestone_events: list[ReachedRaceDistanceMilestone] = []
    for frame in laps_p3_loader.snapshots():
        packet = do_stuff(old_session=session, frame=frame, speaker=None, player=player)
        assert packet.player is not None
        for event in packet.player.events:
            if isinstance(event, ReachedRaceDistanceMilestone):
                milestone_events.append(event)
    assert len(milestone_events) == 0
    # pytest.fail(
    #     "Player with race_milestones=[] over a multi-lap race -> no exception,"
    #     " no milestone events"
    # )


def test_all_milestones_fired_no_crash() -> None:
    # recording: none (build in code)
    pytest.fail(
        "TODO: every milestone popped, then more new laps -> no exception,"
        " no milestone events"
    )


def test_lap_milestone_fires_once() -> None:
    # recording: none (build in code; laps-left estimate crosses 5)
    pytest.fail(
        "TODO: Lap(5), estimate goes 6 -> 5 -> 5 (two crossings) -> exactly one"
        " milestone event"
    )


def test_two_milestones_same_lap_one_event() -> None:
    # recording: none (build in code; 50% and Lap(10) reached on the same crossing)
    pytest.fail(
        "TODO: two milestones reached on one crossing -> both popped, one event"
        " (your call: which one is said)"
    )


def test_passed_milestone_not_said_late() -> None:
    # recording: none (build in code; estimate drops 11 -> 9 in one crossing)
    pytest.fail(
        "TODO: Lap(10) passed without a crossing at 10 -> popped,"
        " not said on the next lap (your call: said now, or silent)"
    )


def test_percent_milestone_from_time() -> None:
    # recording: none (build in code; SessionTimeRemain / SessionTimeTotal)
    pytest.fail(
        "TODO: Percent(0.5), time remaining crosses 50% of total -> one event at"
        " the next crossing, no laps-left estimate needed"
    )


def test_milestones_only_in_race() -> None:
    # recording: none (build in code; practice session)
    pytest.fail("TODO: practice session, laps-left crosses a milestone -> no event")


def test_repeated_tick_no_repeat_events() -> None:
    # recording: tests/recordings/rolling_start (GREEN at tick 77047)
    # Checked 11-17 on 6c09a8b: do_stuff twice on the green frame -> GREEN both times.
    pytest.fail(
        "TODO: do_stuff on the same frame twice -> second call has no event facts"
        " (session, car or player)"
    )
