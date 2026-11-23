from copy import deepcopy

from soma.car import Car
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

    def check_for_session_change(self, session_events: list[Event]) -> None:
        for event in session_events:
            if isinstance(event, SessionChanged):
                self.handle_session_change()

    def check_for_lap_milestones(self, player_car: Car) -> None:
        if len(self.race_milestones) == 0:
            return

        if not player_car.new_lap_detected():
            return

        milestone = self.race_milestones[0]
        if isinstance(milestone, RaceDistanceMilestoneAsLap):
            self.events.append(
                # TODO remove the placeholders from time/laps remain
                ReachedRaceDistanceMilestone(time_remain=0.0, laps_remain=0.0)
            )
            self.race_milestones.pop(0)

    def handle_frame(self, session: Session) -> None:
        self.events = []

        self.check_for_session_change(session.events)
        self.check_for_lap_milestones(session.player_car)
