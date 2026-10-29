import pytest

from soma.car import Car
from soma.lap import Lap


def create_laps(car: Car, start_lap: int, num_laps: int) -> dict[int, list[Lap]]:
    laps: dict[int, list[Lap]] = {car.session_num: []}
    session_time = 100
    for lap_number in range(start_lap, num_laps + 1):
        lap_time = 90
        session_time = lap_time + session_time
        laps[car.session_num].append(
            Lap(
                car_idx=car.idx,
                session_number=car.session_num,
                lap_number=lap_number,
                lap_time_s=lap_time,
                session_time=session_time,
                estimated_timestamp=session_time,
            )
        )
    return laps


def create_car(idx: int, position: int) -> Car:
    car = Car(
        session_time=0,
        session_num=3,
        idx=idx,
        position=position,
        lap_dist=0,
        event_laps_completed=0,
        laps={},
        events=[],
    )
    return car


def test_delta_gap_no_laps_either_car() -> None:
    pytest.fail("TODO: no laps this session, either car -> None")


def test_delta_gap_self_has_no_laps() -> None:
    pytest.fail("TODO: other has laps, self has none -> None, not KeyError")


def test_delta_gap_unequal_lap_counts() -> None:
    car_1_3_car = create_car(idx=1, position=1)
    car_1_3_car.laps = create_laps(car=car_1_3_car, start_lap=1, num_laps=3)
    car_2_2_car = create_car(idx=2, position=2)
    car_2_2_car.laps = create_laps(car=car_2_2_car, start_lap=1, num_laps=2)
    assert car_1_3_car.get_last_shared_completed_lap(car_2_2_car) == 2
