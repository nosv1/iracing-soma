from dataclasses import dataclass, field

from soma.car import Car
from soma.driver import Driver
from soma.irsdk_vars import PLAYER_CAR_IDX, SESSION_TICK, SESSION_TIME
from soma.loader import Snapshot


@dataclass
class Session:
    session_time: float
    session_tick: int
    player_car_idx: int
    cars: dict[int, Car] = field(default_factory=dict)  # CarIdx, Car
    drivers: dict[int, Driver] = field(default_factory=dict)  # CarIdx, Driver
    positions: dict[int, int] = field(default_factory=dict)  # position, CarIdx

    @classmethod
    def from_frame(cls, frame: Snapshot) -> Session:
        # this can prob move to handle_frame, we don't need to create objects
        # every frame, we just need to figure out which ones exist now that
        # didn't before
        cars = Car.cars_from_frame(frame)
        drivers = Driver.drivers_from_frame(frame)
        positions = {c.position: c.idx for c in cars.values()}

        return Session(
            session_time=frame[SESSION_TIME],
            session_tick=frame[SESSION_TICK],
            player_car_idx=frame[PLAYER_CAR_IDX],
            cars=cars,
            drivers=drivers,
            positions=positions,
        )

    def update_session(self, new_session: Session) -> None:
        self.session_time = new_session.session_time
        self.session_tick = new_session.session_tick

    def handle_frame(self, frame: Snapshot, new_session: Session):
        self.update_session(new_session)

        for idx, new_car in new_session.cars.items():
            if idx not in self.cars:
                self.cars[idx] = new_car
            else:
                self.cars[idx].handle_frame(frame, new_car)
