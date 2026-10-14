import logging
from dataclasses import dataclass

import irsdk

logger = logging.getLogger(__file__)


@dataclass
class State:
    is_ir_connected: bool = False


class iRacing:  # noqa: N801  (brand name capitalization)
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.state = State()

    def connect(self) -> None:
        self.ir.startup()
        self.state.is_ir_connected = True
        logger.info("iRacing:Connected")

    def disconnect(self):
        self.ir.shutdown()
        self.state.is_ir_connected = False
        logger.info("iRacing:Connected")
