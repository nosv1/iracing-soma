from dataclasses import dataclass
import irsdk


@dataclass
class State:
    ir_connected: bool = False
    last_car_setup_tick: int = -1


class iRacing:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.state = State()

    def check_iracing(self):
        if self.state.ir_connected and not (
            self.ir.is_initialized and self.ir.is_connected
        ):
            self.state.ir_connected = False
            # don't forget to reset your State variables
            self.state.last_car_setup_tick = -1
            # we are shutting down ir library (clearing all internal variables)
            self.ir.shutdown()
            print("irsdk disconnected")
        elif (
            not self.state.ir_connected
            and self.ir.startup()
            and self.ir.is_initialized
            and self.ir.is_connected
        ):
            self.state.ir_connected = True
            print("irsdk connected")
