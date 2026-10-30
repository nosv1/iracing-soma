from soma.car import Car
from soma.lap import Lap
from soma.track_surface import TrackSurface


def create_laps(
    car: Car, start_lap: int, num_laps: int, lap_time_offset: int
) -> dict[int, dict[int, Lap]]:
    laps: dict[int, dict[int, Lap]] = {car.session_num: {}}
    session_time = 100
    for lap_number in range(start_lap, start_lap + num_laps):
        lap_time = 90 + lap_time_offset
        session_time = lap_time + session_time
        lap = Lap(
            car_idx=car.idx,
            session_number=car.session_num,
            lap_number=lap_number,
            lap_time_s=lap_time,
            session_time=session_time,
            estimated_timestamp=session_time,
        )
        laps[car.session_num][lap_number] = lap
        car.prev_session_lap_num = lap.lap_number
    return laps


def create_car(idx: int, position: int) -> Car:
    car = Car(
        session_time=0,
        session_num=3,
        track_surface=TrackSurface(3),
        idx=idx,
        position=position,
        lap_dist=0,
        event_laps_completed=0,
        prev_session_lap_num=0,
        laps={},
        events=[],
    )
    return car


def test_delta_gap_no_laps_either_car() -> None:
    car_1 = create_car(idx=1, position=1)
    car_2 = create_car(idx=2, position=2)
    assert car_2.get_gap_to(car_1) is None
    assert car_1.get_gap_to(car_2) is None


def test_delta_gap_self_has_no_laps() -> None:
    car_1 = create_car(idx=1, position=1)
    car_1.laps = create_laps(
        car=car_1, start_lap=1, num_laps=3, lap_time_offset=car_1.idx
    )
    car_2 = create_car(idx=2, position=2)
    assert car_2.get_gap_to(car_1) is None
    assert car_1.get_gap_to(car_2) is None


def test_delta_gap_unequal_lap_counts() -> None:
    car_1_3 = create_car(idx=1, position=1)
    car_1_3.laps = create_laps(
        car=car_1_3, start_lap=1, num_laps=3, lap_time_offset=car_1_3.idx
    )
    car_2_2 = create_car(idx=2, position=2)
    car_2_2.laps = create_laps(
        car=car_2_2, start_lap=1, num_laps=2, lap_time_offset=car_2_2.idx
    )
    assert car_1_3.get_delta_gap_after_lap(car_2_2) == -1


def test_delta_gap_other_missing_previous_lap() -> None:
    car_1_3 = create_car(idx=1, position=1)
    car_1_3.laps = create_laps(
        car=car_1_3, start_lap=6, num_laps=4, lap_time_offset=car_1_3.idx
    )
    car_2_2 = create_car(idx=2, position=2)
    car_2_2.laps = create_laps(
        car=car_2_2, start_lap=6, num_laps=4, lap_time_offset=car_2_2.idx
    )
    del car_2_2.laps[car_2_2.session_num][8]
    assert car_1_3.get_delta_gap_after_lap(car_2_2) is None


def test_not_in_world_frame_leaves_car_unchanged() -> None:
    # recording: none; build cars with create_car
    car = create_car(1, 1)
    car.track_surface = TrackSurface(TrackSurface.ON_TRACK)
    new_car = create_car(1, 1)
    new_car.track_surface = TrackSurface(TrackSurface.NOT_IN_WORLD)

    new_car.lap_dist = car.lap_dist + 1
    new_car.event_laps_completed = car.event_laps_completed + 1
    new_car.session_time = car.session_time + 1
    car.update_car(new_car)

    assert car.lap_dist == new_car.lap_dist - 1
    assert car.event_laps_completed == new_car.event_laps_completed - 1
    assert car.session_time == new_car.session_time - 1
