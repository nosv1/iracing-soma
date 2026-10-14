from dataclasses import dataclass

from irsdk import IRSDK

from soma.irsdk_vars import CAR_IDX, DRIVER_INFO, DRIVERS, USER_NAME


@dataclass
class Driver:
    car_idx: int
    name: str

    @classmethod
    def from_irsdk(cls, driver: dict) -> Driver:
        return Driver(car_idx=driver[CAR_IDX], name=driver[USER_NAME])

    @classmethod
    def drivers_from_irsdk(cls, ir: IRSDK) -> list[Driver]:
        drivers: list[Driver] = []
        for driver in ir[DRIVER_INFO][DRIVERS]:
            drivers.append(cls.from_irsdk(driver))
        return drivers
