import logging
from dataclasses import dataclass, field

from soma.car import Car
from soma.driver import Driver
from soma.irsdk_vars import (
    PLAYER_CAR_IDX,
    SESSION_ID,
    SESSION_INFO,
    SESSION_NUM,
    SESSION_TICK,
    SESSION_TIME,
    SESSION_TYPE,
    SESSIONS,
    WEEKEND_INFO,
)
from soma.loader import Snapshot
from soma.session_type import SessionType

logger = logging.getLogger(__file__)


@dataclass
class Session:
    session_id: int
    session_num: int
    session_time: float
    session_tick: int
    session_type: SessionType
    player_car_idx: int
    cars: dict[int, Car] = field(default_factory=dict)  # CarIdx, Car
    drivers: dict[int, Driver] = field(default_factory=dict)  # CarIdx, Driver
    positions: dict[int, int] = field(default_factory=dict)  # position, CarIdx

    @property
    def player_car(self) -> Car:
        return self.cars[self.player_car_idx]

    @classmethod
    def from_frame(cls, frame: Snapshot) -> Session:
        # this can prob move to handle_frame, we don't need to create objects
        # every frame, we just need to figure out which ones exist now that
        # didn't before
        cars = Car.cars_from_frame(frame)
        drivers = Driver.drivers_from_frame(frame)

        return Session(
            session_id=frame[WEEKEND_INFO][SESSION_ID],
            session_num=frame[SESSION_NUM],
            session_time=frame[SESSION_TIME],
            session_tick=frame[SESSION_TICK],
            session_type=SessionType(
                frame[SESSION_INFO][SESSIONS][frame[SESSION_NUM]][SESSION_TYPE]
            ),
            player_car_idx=frame[PLAYER_CAR_IDX],
            cars=cars,
            drivers=drivers,
        )

    def update_session(self, new_session: Session) -> None:
        self.session_id = new_session.session_id
        self.session_time = new_session.session_time
        self.session_tick = new_session.session_tick
        self.session_type = new_session.session_type
        self.player_car_idx = new_session.player_car_idx
        self.positions = {c.position: c.idx for c in new_session.cars.values()}

    def is_race(self) -> bool:
        return self.session_type.is_race()

    def handle_frame(self, frame: Snapshot, new_session: Session):
        self.update_session(new_session)

        # add any new cars to existing dict
        for idx, new_car in new_session.cars.items():
            if idx not in self.cars:
                self.cars[idx] = new_car

        # handle all known cars
        for idx, car in self.cars.items():
            if idx in new_session.cars:
                car.handle_frame(frame, new_session.cars[idx])
            else:
                # TODO NEED TO HANDLE CARS THAT HAVE DIPPED
                pass
