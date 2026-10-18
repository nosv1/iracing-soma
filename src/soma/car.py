from dataclasses import dataclass, field

from soma.event import Event
from soma.irsdk_vars import (
    CAR_IDX_LAP_COMPLETED,
    CAR_IDX_LAP_DIST_PCT,
    CAR_IDX_POSITION,
    SESSION_TIME,
)
from soma.lap import Lap
from soma.loader import Snapshot


@dataclass
class Car:
    session_time: float
    idx: int
    position: int
    lap_dist: float
    # number of laps completed across sessions for the same event
    event_laps_completed: int
    # running list of laps
    laps: list[Lap] = field(default_factory=list)
    # list of events for the current frame
    # cleared then appended to in handle frame
    events: list[Event] = field(default_factory=list)

    @classmethod
    def from_frame(cls, frame: Snapshot, idx: int, position: int) -> Car:
        return Car(
            session_time=frame[SESSION_TIME],
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
        self.position = new_car.position
        self.lap_dist = new_car.lap_dist
        self.event_laps_completed = new_car.event_laps_completed

    def get_delta_gap_after_lap(self, other: Car) -> float | None:
        """+ delta gap -> gap grew,  - delta gap -> gap decreased
        this is relative to self, gap growing could be good or bad depending if
        current interval is - or + (leading or following),
        simply if this returns a positive number, the cars got further apart
        """
        lap_idx_to_compare = min(len(self.laps), len(other.laps)) - 1

        if lap_idx_to_compare == -1:
            return None

        gap_before = (
            self.laps[lap_idx_to_compare - 1].estimated_timestamp
            - other.laps[lap_idx_to_compare - 1].estimated_timestamp
        )
        gap_after = (
            self.laps[lap_idx_to_compare].estimated_timestamp
            - other.laps[lap_idx_to_compare].estimated_timestamp
        )

        return gap_after - gap_before

    def did_start_new_lap(self, old_car: Car) -> bool:
        return (
            old_car.event_laps_completed < self.event_laps_completed
            and old_car.lap_dist > self.lap_dist
        )

    def handle_new_lap(self, frame: Snapshot, new_car: Car) -> None:
        self.events.append(Event.CAR_NEW_LAP)
        self.laps.append(
            Lap.from_frame(
                frame,
                self.idx,
                Lap.estimate_lap_timestamp(
                    session_time=new_car.session_time,
                    prev_session_time=self.session_time,
                    lap_dist=new_car.lap_dist,
                    prev_lap_dist=self.lap_dist,
                ),
            )
        )

    def handle_frame(self, frame: Snapshot, new_car: Car):
        self.events = []

        if new_car.did_start_new_lap(self):
            self.handle_new_lap(frame, new_car)

        self.update_car(new_car)
