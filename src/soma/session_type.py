import logging
from enum import StrEnum

logger = logging.getLogger(__file__)


class SessionType(StrEnum):
    PRACTICE = "Practice"
    LONE_QUALIFY = "Lone Qualify"
    OPEN_QUALIFY = "Open Qualify"
    RACE = "Race"
    UNKNOWN = "Unknown"

    @classmethod
    def _missing_(cls, value):
        logger.warning(f"UNKNOWN SESSION TYPE: {value!r}")
        return cls.UNKNOWN

    def is_practice(self) -> bool:
        return self in {SessionType.PRACTICE}

    def is_qualifying(self) -> bool:
        return self in {SessionType.LONE_QUALIFY, SessionType.OPEN_QUALIFY}

    def is_race(self) -> bool:
        return self in {SessionType.RACE}
