from dataclasses import dataclass
from typing import ClassVar


@dataclass
class EventFact:
    event: ClassVar[str]

    def to_json(self):
        pass

    def to_str(self):
        pass


@dataclass
class GapFact(EventFact):
    event: ClassVar[str] = "gap to"
    pos: int
    gap_s_as_positive: float

    def to_json(self):
        return {
            "event": self.event,
            "position": self.pos,
            "gap_s": self.gap_s_as_positive,
        }

    def to_str(self):
        return f"Gap to P{self.pos} is {round(self.gap_s_as_positive, 1)} seconds"


@dataclass
class CaughtFact(EventFact):
    event: ClassVar[str] = "caught"
    pos: int
    gain_s_as_positive: float
    gap_fact: GapFact

    def to_json(self):
        return {
            "event": self.event,
            "position": self.pos,
            "gain_s": self.gain_s_as_positive,
            "gap_fact": self.gap_fact.to_json(),
        }

    def to_str(self):
        # i know this is robotic, these to_str methods are mainly for testing
        # event fact -> to_json (or to str) -> to_llm
        return (
            f"Caught P{self.pos} by {round(self.gain_s_as_positive, 1)} seconds\n"
            f"{self.gap_fact.to_str()}"
        )
