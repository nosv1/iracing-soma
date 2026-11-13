import logging
from dataclasses import dataclass, field

from soma.car import Car
from soma.driver import Driver
from soma.event import Event, FlagsChanged
from soma.irsdk_vars import (
    PLAYER_CAR_IDX,
    SESSION_ID,
    SESSION_INFO,
    SESSION_NUM,
    SESSION_TICK,
    SESSION_TIME,
    SESSION_TIME_REMAIN,
    SESSION_TIME_TOTAL,
    SESSION_TYPE,
    SESSIONS,
    WEEKEND_INFO,
)
from soma.loader import Snapshot
from soma.session_flag import SessionFlag
from soma.session_type import SessionType

logger = logging.getLogger(__file__)


@dataclass
class Session:
    session_id: int
    session_num: int
    session_time: float
    session_tick: int
    session_type: SessionType
    # TODO determine what this is for ovals
    session_time_total: float
    session_time_remain: float
    player_car_idx: int
    session_flags: set[SessionFlag] = field(default_factory=set)
    cars: dict[int, Car] = field(default_factory=dict)  # CarIdx, Car
    drivers: dict[int, Driver] = field(default_factory=dict)  # CarIdx, Driver
    positions: dict[int, int] = field(default_factory=dict)  # position, CarIdx
    # list of events for the current frame
    # cleared then appended to in handle frame
    events: list[Event] = field(default_factory=list)

    @property
    def player_car(self) -> Car:
        return self.cars[self.player_car_idx]

    @property
    def estimated_laps_left(self) -> None | int:
        return self.estimate_laps_left()

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
            session_time_total=frame[SESSION_TIME_TOTAL],
            session_time_remain=frame[SESSION_TIME_REMAIN],
            player_car_idx=frame[PLAYER_CAR_IDX],
            session_flags=SessionFlag.from_frame(frame),
            cars=cars,
            drivers=drivers,
        )

    def update_session(self, new_session: Session) -> None:
        self.session_id = new_session.session_id
        self.session_time = new_session.session_time
        self.session_tick = new_session.session_tick
        self.session_type = new_session.session_type
        self.session_time_total = new_session.session_time_total
        self.session_time_remain = new_session.session_time_remain
        self.player_car_idx = new_session.player_car_idx
        self.session_flags = new_session.session_flags
        self.positions = {c.position: c.idx for c in new_session.cars.values()}

    def is_race(self) -> bool:
        return self.session_type.is_race()

    def estimate_laps_left(self) -> None | int:
        # TODO developed for timed races, what happens for lap count races?
        leader_car = self.cars[self.positions[1]]

        if self.session_num not in leader_car.laps:
            return None

        if self.session_num not in leader_car.best_laps:
            return None

        if not isinstance(leader_car.best_laps[self.session_num], int):
            return None

        leaders_best_lap_lap_number = leader_car.best_laps[self.session_num]
        if leaders_best_lap_lap_number is None:
            return None

        leaders_best_lap = leader_car.laps[self.session_num][
            leaders_best_lap_lap_number
        ]

        if leaders_best_lap.lap_time_s is None:
            return None

        # the amount of time to add back to session time given leader is some
        # distance through the lap already, lap dist * best lap is prob close enough
        leader_lap_time_offset = leader_car.lap_dist * leaders_best_lap.lap_time_s
        # round down the estimated laps left and add one
        return (
            int(
                (self.session_time_remain + leader_lap_time_offset)
                / leaders_best_lap.lap_time_s
            )
            + 1
        )

    def detect_flag_changes(self, new_session: Session) -> None:
        if SessionFlag.flags_changed(new_session.session_flags, self.session_flags):
            self.events.append(
                FlagsChanged(
                    old_flags=self.session_flags, cur_flags=new_session.session_flags
                )
            )

    def handle_frame(self, frame: Snapshot, new_session: Session):
        self.events = []

        self.detect_flag_changes(new_session)
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
