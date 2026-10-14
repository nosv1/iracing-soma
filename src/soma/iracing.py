import logging
import time

import irsdk

logger = logging.getLogger(__file__)


class iRacing:  # noqa: N801  (brand name capitalization)
    def __init__(self):
        self.ir = irsdk.IRSDK()

    def connect(self) -> None:
        connected = self.ir.startup()
        if connected:
            logger.info("Connected")
        else:
            logger.info("iRacing sim is not running")

    def disconnect(self):
        was_connected = self.ir.is_connected
        self.ir.shutdown()
        if was_connected:
            logger.info("Disconnected")
