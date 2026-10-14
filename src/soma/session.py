from dataclasses import dataclass, field

from irsdk import IRSDK

from soma.car import Car
from soma.driver import Driver
from soma.irsdk_vars import PLAYER_CAR_IDX, SESSION_TIME


@dataclass
class Session:
    session_time: int
    player_car_idx: int
    cars: list[Car] = field(default_factory=list)
    drivers: list[Driver] = field(default_factory=list)

    @classmethod
    def from_irsdk(cls, ir: IRSDK) -> Session:
        return Session(
            session_time=ir[SESSION_TIME],
            player_car_idx=ir[PLAYER_CAR_IDX],
            cars=Car.cars_from_irsdk(ir),
            drivers=Driver.drivers_from_irsdk(ir),
        )
