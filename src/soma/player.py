from copy import deepcopy

from soma.event import Event, ReachedRaceDistanceMilestone, SessionChanged
from soma.player_constants import (
    PlayerConstants,
    RaceDistanceMilestoneAsLap,
    RaceDistanceMilestoneAsPercentRemaining,
)
from soma.session import Session


class Player:
    def __init__(self, player_constants: PlayerConstants) -> None:
        self.player_constants = player_constants
        self.events: list[Event] = []
        ##### \/ copy the constants for initial session
        self.race_milestones: list[
            RaceDistanceMilestoneAsLap | RaceDistanceMilestoneAsPercentRemaining
        ]
        self.handle_session_change()
        ##### /\ copy the constants for the initial session

    def handle_session_change(self) -> None:
        self.race_milestones = deepcopy(self.player_constants.race_milestones)

    def handle_reached_race_milestone(
        self, time_remaining: float | None, laps_remaining: float | None
    ) -> None:
        self.events.append(
            # TODO remove the placeholders from time/laps remain
            ReachedRaceDistanceMilestone(
                time_remaining=time_remaining,
                laps_remaining=laps_remaining,
            )
        )
        self.race_milestones.pop(0)

    def check_for_session_change(self, session_events: list[Event]) -> None:
        for event in session_events:
            if isinstance(event, SessionChanged):
                self.handle_session_change()

    def check_for_lap_milestones(self, session: Session) -> None:
        if len(self.race_milestones) == 0:
            return

        if not session.player_car.new_lap_detected():
            return

        milestone = self.race_milestones[0]
        if isinstance(milestone, RaceDistanceMilestoneAsLap):
            if (
                session.laps_remaining is not None
                and session.laps_remaining <= milestone.laps_remaining
            ):
                self.handle_reached_race_milestone(
                    time_remaining=session.session_time_remain,
                    laps_remaining=session.laps_remaining,
                )

        elif isinstance(milestone, RaceDistanceMilestoneAsPercentRemaining):
            if (
                session.percent_remaining is not None
                and session.percent_remaining <= milestone.percent_remaining
            ):
                self.handle_reached_race_milestone(
                    time_remaining=session.session_time_remain,
                    laps_remaining=session.laps_remaining,
                )

    def handle_frame(self, session: Session) -> None:
        self.events = []

        self.check_for_session_change(session.events)
        self.check_for_lap_milestones(session)
