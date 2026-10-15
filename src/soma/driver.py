from dataclasses import dataclass

from irsdk import IRSDK

from soma.irsdk_vars import CAR_IDX, DRIVER_INFO, DRIVERS, USER_NAME
from soma.loader import Snapshot


@dataclass
class Driver:
    car_idx: int
    name: str

    @classmethod
    def from_frame(cls, driver: dict) -> Driver:
        return Driver(car_idx=driver[CAR_IDX], name=driver[USER_NAME])

    @classmethod
    def drivers_from_frame(cls, ir: IRSDK | Snapshot) -> list[Driver]:
        drivers: list[Driver] = []
        for driver in ir[DRIVER_INFO][DRIVERS]:
            drivers.append(cls.from_frame(driver))
        return drivers
