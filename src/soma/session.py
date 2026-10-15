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
    cars: dict[int, Car] = field(default_factory=dict)  # CarIdx, Car
    drivers: dict[int, Driver] = field(default_factory=dict)  # CarIdx, Driver
    positions: dict[int, int] = field(default_factory=dict)  # position, CarIdx

    @classmethod
    def from_frame(cls, frame: IRSDK | Snapshot) -> Session:
        cars = Car.cars_from_frame(frame)
        drivers = Driver.drivers_from_frame(frame)
        positions = {c.position: c.idx for c in cars.values()}

        return Session(
            session_time=frame[SESSION_TIME],
            player_car_idx=frame[PLAYER_CAR_IDX],
            cars=cars,
            drivers=drivers,
            positions=positions,
        )
