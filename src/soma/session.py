from dataclasses import dataclass, field

from irsdk import IRSDK

from soma.car import Car
from soma.driver import Driver
from soma.irsdk_vars import PLAYER_CAR_IDX, SESSION_TIME
from soma.loader import Snapshot


@dataclass
class Session:
    session_time: int
    player_car_idx: int
    cars: list[Car] = field(default_factory=list)
    drivers: list[Driver] = field(default_factory=list)

    @classmethod
    def from_frame(cls, frame: IRSDK | Snapshot) -> Session:
        return Session(
            session_time=frame[SESSION_TIME],
            player_car_idx=frame[PLAYER_CAR_IDX],
            cars=Car.cars_from_frame(frame),
            drivers=Driver.drivers_from_frame(frame),
        )
