from copy import deepcopy
from dataclasses import dataclass, field

from soma.event import Event, SessionChanged
from soma.player_constants import PlayerConstants
from soma.session import Session


@dataclass
class Player:
    player_constants_for_session: PlayerConstants
    events: list[Event] = field(default_factory=list)

    def __init__(self, player_constants: PlayerConstants) -> None:
        self.player_constants = player_constants

    def handle_session_change(self) -> None:
        self.player_constants_for_session = deepcopy(self.player_constants)

    def check_for_session_change(self, session_events: list[Event]) -> None:
        for event in session_events:
            if isinstance(event, SessionChanged):
                self.handle_session_change()

    def handle_frame(self, session: Session) -> None:
        self.events = []

        self.check_for_session_change(session.events)
