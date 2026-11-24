from enum import Enum


class DurationType(Enum):
    TIMED = "timed"
    LAPS = "laps"
    UNKNOWN = "unknown"

    @classmethod
    def from_frame(cls, session_laps: int | str) -> DurationType:
        if isinstance(session_laps, str) and session_laps == "unlimited":
            return DurationType("timed")

        if isinstance(session_laps, int):
            return DurationType("laps")

        return DurationType("unknown")
