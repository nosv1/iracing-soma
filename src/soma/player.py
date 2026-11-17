from copy import copy

from soma.player_constants import PlayerConstants


class Player:
    def __init__(self, player_constants: PlayerConstants) -> None:
        self.player_constants = player_constants

    def handle_new_session(self) -> None:
        self.player_constants_for_session = copy(self.player_constants)
