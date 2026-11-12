import logging
from enum import IntFlag

from irsdk import Flags

from soma.irsdk_vars import SESSION_FLAGS
from soma.snapshot import Snapshot

logger = logging.getLogger(__file__)


class SessionFlag(IntFlag):
    CHECKERED = Flags.checkered
    WHITE = Flags.white
    GREEN = Flags.green
    YELLOW = Flags.yellow  # 10/31 assuming this is full course
    YELLOW_WAVING = Flags.yellow_waving  # 10/31 assuming this is local
    BLUE = Flags.blue

    @classmethod
    def get_flags_from_int(cls, flags: int) -> set[SessionFlag]:
        session_flags: set[SessionFlag] = set()
        for v in SessionFlag:
            if cls.flag_is_on(v, flags):
                session_flags.add(v)
        return session_flags

    @classmethod
    def from_frame(cls, frame: Snapshot) -> set[SessionFlag]:
        return cls.get_flags_from_int(frame[SESSION_FLAGS])

    @classmethod
    def flag_is_on(cls, flag: int, flags: int) -> bool:
        return bool(flag & flags)

    @classmethod
    def flags_changed(cls, cur_flags: set[SessionFlag], prev_flags: set[SessionFlag]):
        return cur_flags != prev_flags
