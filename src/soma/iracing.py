import logging
from dataclasses import dataclass

import irsdk

logger = logging.getLogger(__file__)


@dataclass
class State:
    is_ir_connected: bool = False
    last_car_setup_tick: int = -1


class iRacing:  # noqa: N801  (brand name capitalization)
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.state = State()

    def check_iracing(self) -> None:
        if self.state.is_ir_connected and not (
            self.ir.is_initialized and self.ir.is_connected
        ):
            self.state.is_ir_connected = False
            # don't forget to reset your State variables
            self.state.last_car_setup_tick = -1
            # we are shutting down ir library (clearing all internal variables)
            self.ir.shutdown()
            logger.info("iRacing:IRSDK disconnected")
            return

        elif (
            not self.state.is_ir_connected
            and self.ir.startup()
            and self.ir.is_initialized
            and self.ir.is_connected
        ):
            self.state.is_ir_connected = True
            logger.info("iRacing:IRSDK connected")
            return

        logger.error("iRacing:IRSDK failed to connect")
        return
