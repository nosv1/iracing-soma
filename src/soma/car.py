from dataclasses import dataclass

from irsdk import IRSDK

from soma.irsdk_vars import CAR_IDX_POSITION
from soma.loader import Snapshot


@dataclass
class Car:
    idx: int
    position: int

    @classmethod
    def from_frame(cls, idx: int, position: int) -> Car:
        return Car(idx=idx, position=position)

    @classmethod
    def cars_from_frame(cls, ir: IRSDK | Snapshot) -> dict[int, Car]:
        cars: dict[int, Car] = {}
        for i, position in enumerate(ir[CAR_IDX_POSITION]):
            cars[i] = cls.from_frame(i, position)
        return cars
