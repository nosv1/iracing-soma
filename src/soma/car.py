from dataclasses import dataclass, field

from soma.event import Event
from soma.irsdk_vars import (
    CAR_IDX_LAP_COMPLETED,
    CAR_IDX_LAP_DIST_PCT,
    CAR_IDX_POSITION,
    SESSION_NUM,
    SESSION_TIME,
)
from soma.lap import Lap
from soma.loader import Snapshot


@dataclass
class CarDeltaGap:
    car_idx: int
    delta_gap: float


@dataclass
class Car:
    session_time: float
    session_num: int
    idx: int
    position: int
    lap_dist: float
    # number of laps completed across sessions for the same event
    event_laps_completed: int
    # {session_num: [Lap]}
    laps: dict[int, list[Lap]] = field(default_factory=dict)
    # list of events for the current frame
    # cleared then appended to in handle frame
    events: list[Event] = field(default_factory=list)

    @property
    def lap_num(self) -> int:
        """ returns current lap number of current session"""
        if self.session_num in self.laps:
            return len(self.laps[self.session_num]) + 1
        return 1

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Car)
        return self.idx == other.idx

    @classmethod
    def from_frame(cls, frame: Snapshot, idx: int, position: int) -> Car:
        return Car(
            session_time=frame[SESSION_TIME],
            session_num=frame[SESSION_NUM],
            idx=idx,
            position=position,
            lap_dist=frame[CAR_IDX_LAP_DIST_PCT][idx],
            event_laps_completed=frame[CAR_IDX_LAP_COMPLETED][idx],
        )

    @classmethod
    def cars_from_frame(cls, frame: Snapshot) -> dict[int, Car]:
        cars: dict[int, Car] = {}
        for i, position in enumerate(frame[CAR_IDX_POSITION]):
            if position <= 0:
                continue
            cars[i] = cls.from_frame(frame, i, position)
        return cars

    def update_car(self, new_car: Car) -> None:
        self.session_time = new_car.session_time
        self.session_num = new_car.session_num
        self.position = new_car.position
        self.lap_dist = new_car.lap_dist
        self.event_laps_completed = new_car.event_laps_completed

    def get_last_shared_completed_lap(self, other: Car) -> int:
        if self.session_num not in other.laps:
            return 0

        if self.session_num not in self.laps:
            return 0

        return min(len(self.laps[self.session_num]), len(other.laps[self.session_num]))

    def get_delta_gap_after_lap(self, other: Car) -> float | None:
        """\\+ delta gap -> gap grew,  \\- delta gap -> gap decreased
        this is relative to self, gap growing could be good or bad depending if
        current interval is - or + (leading or following),
        simply if this returns a positive number, the cars got further apart
        """
        lap_to_compare = self.get_last_shared_completed_lap(other)
        if lap_to_compare <= 1:
            return None

        lap_idx_to_compare = lap_to_compare - 1

        gap_before = (
            self.laps[self.session_num][lap_idx_to_compare - 1].estimated_timestamp
            - other.laps[self.session_num][lap_idx_to_compare - 1].estimated_timestamp
        )
        gap_after = (
            self.laps[self.session_num][lap_idx_to_compare].estimated_timestamp
            - other.laps[self.session_num][lap_idx_to_compare].estimated_timestamp
        )

        return gap_after - gap_before

    def get_delta_gaps_ahead(
        self, cars_dict: dict[int, Car], positions_idx_map: dict[int, int]
    ) -> list[CarDeltaGap]:
        """returns sorted list of CarDeltaGap in order of largest negative
        number to smallest negative number"""
        delta_gaps: list[CarDeltaGap] = []
        # loop positions ahead of player
        for pos in range(1, self.position):
            car_ahead = cars_dict[positions_idx_map[pos]]
            delta_gap = self.get_delta_gap_after_lap(car_ahead)
            if delta_gap is None:
                continue
            delta_gaps.append(CarDeltaGap(car_idx=car_ahead.idx, delta_gap=delta_gap))
        # sorted largest neg to smallest neg
        # (could be into positive if car ahead increased gap)
        delta_gaps.sort(key=lambda dg: dg.delta_gap)
        return delta_gaps

    def get_gap_to(self, other: Car) -> float | None:
        lap_to_compare = self.get_last_shared_completed_lap(other)
        if lap_to_compare <= 1:
            return None

        lap_idx_to_compare = lap_to_compare - 1

        return (
            self.laps[self.session_num][lap_idx_to_compare].estimated_timestamp
            - other.laps[self.session_num][lap_idx_to_compare].estimated_timestamp
        )

    def did_finish_lap(self, old_car: Car) -> bool:
        return (
            old_car.event_laps_completed >= 0
            and old_car.event_laps_completed < self.event_laps_completed
            and old_car.lap_dist > self.lap_dist
        )

    def handle_new_lap(self, frame: Snapshot, new_car: Car) -> None:
        self.events.append(Event.CAR_NEW_LAP)

        prev_lap: Lap | None = None
        if self.session_num not in self.laps:
            self.laps[self.session_num] = []
        else:
            prev_lap = self.laps[self.session_num][-1]

        estimated_lap_timestamp = Lap.estimate_lap_timestamp(
            session_time=new_car.session_time,
            prev_session_time=self.session_time,
            lap_dist=new_car.lap_dist,
            prev_lap_dist=self.lap_dist,
        )
        if prev_lap is not None:
            estimated_lap_time = Lap.estimate_lap_time_s(
                prev_lap.estimated_timestamp, estimated_lap_timestamp
            )
        else:
            estimated_lap_time = None

        self.laps[self.session_num].append(
            Lap.from_frame(frame, self.idx, estimated_lap_timestamp, estimated_lap_time)
        )

    def handle_frame(self, frame: Snapshot, new_car: Car):
        self.events = []

        if new_car.did_finish_lap(self):
            self.handle_new_lap(frame, new_car)

        self.update_car(new_car)
