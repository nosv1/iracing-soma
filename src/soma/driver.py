from dataclasses import dataclass

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
    def drivers_from_frame(cls, ir: Snapshot) -> dict[int, Driver]:
        drivers: dict[int, Driver] = {}
        for driver_dict in ir[DRIVER_INFO][DRIVERS]:
            driver = cls.from_frame(driver_dict)
            drivers[driver.car_idx] = driver
        return drivers
