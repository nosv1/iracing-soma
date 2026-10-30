import logging
from enum import Enum

logger = logging.getLogger(__file__)


class TrackSurface(Enum):
    NOT_IN_WORLD = -1
    OFF_TRACK = 0
    IN_PIT_STALL = 1
    APPROACHING_PITS = 2
    ON_TRACK = 3

    def is_not_in_world(self) -> bool:
        return self == self.NOT_IN_WORLD
