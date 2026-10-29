import pytest


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
