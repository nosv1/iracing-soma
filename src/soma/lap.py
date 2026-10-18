from dataclasses import dataclass

from soma.irsdk_vars import CAR_IDX_LAP_COMPLETED, CAR_IDX_LAST_LAP_TIME, SESSION_TIME
from soma.snapshot import Snapshot


@dataclass
class Lap:
    car_idx: int
    lap_number: int
    lap_time_s: float
    session_time: float  # timestamp of the tick when this lap was discovered
    estimated_timestamp: float  # interpolated timestamp based on cur and prev frames

    @classmethod
    def from_frame(
        cls, frame: Snapshot, car_idx: int, estimated_lap_timestamp: float
    ) -> Lap:
        return Lap(
            car_idx=car_idx,
            lap_number=frame[CAR_IDX_LAP_COMPLETED][car_idx],
            lap_time_s=frame[CAR_IDX_LAST_LAP_TIME][car_idx],
            session_time=frame[SESSION_TIME],
            estimated_timestamp=estimated_lap_timestamp,
        )

    @classmethod
    def estimate_lap_timestamp(
        cls,
        session_time: float,
        prev_session_time: float,
        lap_dist: float,
        prev_lap_dist: float,
    ) -> float:
        tick_dur = session_time - prev_session_time
        tick_dist = lap_dist + (1 - prev_lap_dist)
        time_per_dist = tick_dur / tick_dist
        elapsed_time_to_0 = time_per_dist * lap_dist
        return session_time - elapsed_time_to_0
