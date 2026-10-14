from dataclasses import dataclass

from irsdk import IRSDK

from soma.irsdk_vars import CAR_IDX_POSITION


@dataclass
class Car:
    idx: int
    position: int

    @classmethod
    def from_irsdk(cls, idx: int, position: int) -> Car:
        return Car(idx=idx, position=position)

    @classmethod
    def cars_from_irsdk(cls, ir: IRSDK) -> list[Car]:
        cars: list[Car] = []
        for i, position in enumerate(ir[CAR_IDX_POSITION]):
            cars.append(cls.from_irsdk(i, position))
        return cars
