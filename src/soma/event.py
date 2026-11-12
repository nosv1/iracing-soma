from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import StrEnum

from soma.session_flag import SessionFlag


class EventTypes(StrEnum):
    CAR_NEW_LAP = "car_new_lap"
    FLAGS_CHANGED = "flags_changed"


class Event:
    name: str


@dataclass
class FlagsChanged(Event):
    name = EventTypes.FLAGS_CHANGED
    old_flags: set[SessionFlag] = field(default_factory=set)
    cur_flags: set[SessionFlag] = field(default_factory=set)

    @property
    def new_flags(self) -> Iterator[SessionFlag]:
        for flag in self.cur_flags:
            if flag not in self.old_flags:
                yield flag
