from copy import deepcopy

from soma.car import Car
from soma.event import Event, SessionChanged
from soma.player_constants import PlayerConstants, RaceDistanceMilestoneAsLap
from soma.session import Session


class Player:
    def __init__(self, player_constants: PlayerConstants) -> None:
        self.player_constants = player_constants
        self.events: list[Event] = []
        ##### \/ copy the constants for initial session
        self.player_constants_for_session: PlayerConstants
        self.handle_session_change()
        ##### /\ copy the constants for the initial session

    def handle_session_change(self) -> None:
        self.player_constants_for_session = deepcopy(self.player_constants)

    def check_for_session_change(self, session_events: list[Event]) -> None:
        for event in session_events:
            if isinstance(event, SessionChanged):
                self.handle_session_change()

    def check_for_lap_milestones(self, player_car: Car) -> None:
        if len(self.player_constants_for_session.race_milestones) == 0:
            return

        if not player_car.new_lap_detected():
            return

        milestone = self.player_constants_for_session.race_milestones[0]
        if isinstance(milestone, RaceDistanceMilestoneAsLap):
            pass

    def handle_frame(self, session: Session) -> None:
        self.events = []

        self.check_for_session_change(session.events)
        self.check_for_lap_milestones(session.player_car)
