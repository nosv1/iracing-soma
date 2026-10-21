import logging
from enum import IntFlag

from irsdk import Flags

logger = logging.getLogger(__file__)


class SessionFlag(IntFlag):
    CHECKERED = Flags.checkered
    WHITE = Flags.white
    YELLOW = Flags.yellow
    GREEN = Flags.green

    # @classmethod
    # def flag_triggered(cls, flag: SessionFlag, old_flag: SessionFlag) -> bool:
    #     return flag & ~old_flag
