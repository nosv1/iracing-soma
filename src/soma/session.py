import logging
from dataclasses import dataclass, field

from soma.car import Car
from soma.driver import Driver
from soma.duration_type import DurationType
from soma.event import Event, FlagsChanged, SessionChanged
from soma.irsdk_vars import (
    PLAYER_CAR_IDX,
    SESSION_ID,
    SESSION_INFO,
    SESSION_LAPS,
    SESSION_LAPS_REMAIN_EX,
    SESSION_NUM,
    SESSION_TICK,
    SESSION_TIME,
    SESSION_TIME_REMAIN,
    SESSION_TIME_TOTAL,
    SESSION_TYPE,
    SESSION_UNIQUE_ID,
    SESSIONS,
    SUB_SESSION_ID,
    WEEKEND_INFO,
)
from soma.session_flag import SessionFlag
from soma.session_type import SessionType
from soma.snapshot import Snapshot

logger = logging.getLogger(__file__)


@dataclass
class Session:
    sub_session_id: int
    session_uid: int
    session_id: int
    session_num: int
    session_time: float
    session_tick: int
    session_type: SessionType
    # TODO determine what this is for ovals
    session_time_total: float
    session_time_remain: float
    session_laps_total: float
    # SessionLapsRemainEx is 32767 for timed sessions
    session_laps_remain: int
    duration_type: DurationType
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
    def laps_remaining(self) -> int | None:
        if self.duration_type == DurationType.TIMED:
            return self.estimate_laps_left()
        if self.duration_type == DurationType.LAPS:
            return self.session_laps_remain
        return None

    @property
    def percent_remaining(self) -> float | None:
        if self.duration_type == DurationType.TIMED:
            return self.session_time_remain / self.session_time_total

        if self.duration_type == DurationType.LAPS:
            if self.laps_remaining is not None:
                return self.laps_remaining / self.session_laps_total

        return None

    @classmethod
    def from_frame(cls, frame: Snapshot) -> Session:
        # this can prob move to handle_frame, we don't need to create objects
        # every frame, we just need to figure out which ones exist now that
        # didn't before
        cars = Car.cars_from_frame(frame)
        drivers = Driver.drivers_from_frame(frame)

        return Session(
            sub_session_id=frame[WEEKEND_INFO][SUB_SESSION_ID],
            session_uid=frame[SESSION_UNIQUE_ID],
            session_id=frame[WEEKEND_INFO][SESSION_ID],
            session_num=frame[SESSION_NUM],
            session_time=frame[SESSION_TIME],
            session_tick=frame[SESSION_TICK],
            session_type=SessionType(
                frame[SESSION_INFO][SESSIONS][frame[SESSION_NUM]][SESSION_TYPE]
            ),
            duration_type=DurationType.from_frame(
                frame[SESSION_INFO][SESSIONS][frame[SESSION_NUM]][SESSION_LAPS]
            ),
            session_time_total=frame[SESSION_TIME_TOTAL],
            session_time_remain=frame[SESSION_TIME_REMAIN],
            session_laps_total=frame[SESSION_INFO][SESSIONS][frame[SESSION_NUM]][
                SESSION_LAPS
            ],
            session_laps_remain=frame[SESSION_LAPS_REMAIN_EX],
            player_car_idx=frame[PLAYER_CAR_IDX],
            session_flags=SessionFlag.from_frame(frame),
            cars=cars,
            drivers=drivers,
        )

    def update_session(self, new_session: Session) -> None:
        self.sub_session_id = new_session.sub_session_id
        self.session_uid = new_session.session_uid
        self.session_id = new_session.session_id
        self.session_num = new_session.session_num
        self.session_time = new_session.session_time
        self.session_tick = new_session.session_tick
        self.session_type = new_session.session_type
        self.duration_type = new_session.duration_type
        self.session_time_total = new_session.session_time_total
        self.session_time_remain = new_session.session_time_remain
        self.session_laps_total = new_session.session_laps_total
        self.session_laps_remain = new_session.session_laps_remain
        self.player_car_idx = new_session.player_car_idx
        self.session_flags = new_session.session_flags
        self.positions = {c.position: c.idx for c in new_session.cars.values()}

    def is_race(self) -> bool:
        return self.session_type.is_race()

    def is_new_sub_session_id(self, new_session: Session) -> bool:
        return self.sub_session_id != new_session.sub_session_id

    def is_new_session_num(self, new_session: Session) -> bool:
        return self.session_num != new_session.session_num

    def estimate_laps_left(self) -> int | None:
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

        leader_lap_time_offset = leader_car.lap_dist * leaders_best_lap.lap_time_s
        leader_lap_time_remaining = leaders_best_lap.lap_time_s - leader_lap_time_offset
        if self.session_time_remain < leader_lap_time_remaining:
            return 1

        return (
            int(
                (self.session_time_remain + leader_lap_time_offset)
                / leaders_best_lap.lap_time_s
            )
            + 1
        )

    def detect_session_change(self, new_session: Session) -> None:
        if self.is_new_session_num(new_session) or self.is_new_sub_session_id(
            new_session
        ):
            self.events.append(
                SessionChanged(
                    old_session_uid=self.session_uid,
                    new_session_uid=new_session.session_uid,
                )
            )

    def detect_flag_changes(self, new_session: Session) -> None:
        if SessionFlag.did_flags_change(new_session.session_flags, self.session_flags):
            self.events.append(
                FlagsChanged(
                    old_flags=self.session_flags, cur_flags=new_session.session_flags
                )
            )

    def handle_frame(self, frame: Snapshot, new_session: Session) -> None:
        self.events = []

        self.detect_session_change(new_session)
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
