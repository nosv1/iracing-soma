from dataclasses import dataclass

from soma.irsdk_vars import (
    CAR_IDX_LAP_COMPLETED,
    CAR_IDX_LAST_LAP_TIME,
    SESSION_NUM,
    SESSION_TIME,
)
from soma.snapshot import Snapshot


@dataclass
class Lap:
    car_idx: int
    session_number: int
    lap_number: int
    # Lap time is estimated - however, its confirmed median difference was
    # 0.0000 s at 10hz and this avoids having to wait for iracing to publish
    # the last lap time
    lap_time_s: float | None
    session_time: float  # timestamp of the tick when this lap was discovered
    estimated_timestamp: float  # interpolated timestamp based on cur and prev frames

    @classmethod
    def from_frame(
        cls,
        frame: Snapshot,
        car_idx: int,
        estimated_lap_timestamp: float,
        estimated_lap_time_s: float | None,
    ) -> Lap:
        # estimated lap time confirmed median difference is 0.0000 s at 10hz
        return Lap(
            car_idx=car_idx,
            session_number=frame[SESSION_NUM],
            lap_number=frame[CAR_IDX_LAP_COMPLETED][car_idx],
            lap_time_s=estimated_lap_time_s,
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

    @classmethod
    def estimate_lap_time_s(
        cls, prev_lap_estimated_timestamp: float, estimated_lap_timestamp: float
    ):
        return estimated_lap_timestamp - prev_lap_estimated_timestamp
