import logging

import pytest

from soma.event_fact import CaughtFact
from soma.handler import handle_events, handle_frame
from soma.loader import Loader
from soma.session import Session

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


@pytest.mark.parametrize(
    "idx, expected", [(0, [0.388, 4.388]), (1, [0.769231, 4.615385])]
)
def test_lap_timestamps(laps_session: Session, idx: int, expected: list[float]) -> None:
    car_0 = laps_session.cars[0]
    car_1 = laps_session.cars[1]
    assert (
        len(car_0.laps[car_0.session_num]) == 2
        and len(car_1.laps[car_1.session_num]) == 2
    )
    actual_timestamps = []
    for lap in laps_session.cars[idx].laps[laps_session.cars[idx].session_num]:
        actual_timestamps.append(lap.estimated_timestamp)
    assert actual_timestamps == pytest.approx(expected)


def test_delta_gap_after_lap(laps_session: Session) -> None:
    assert pytest.approx(0.153846) == pytest.approx(
        laps_session.cars[0].get_delta_gap_after_lap(laps_session.cars[1]), abs=1e-6
    )


def test_sorted_delta_gaps(laps_p3_loader: Loader) -> None:
    session: Session | None = None
    for snapshot in laps_p3_loader.snapshots():
        session = handle_frame(session, snapshot)
        if session.session_tick == 990:
            sorted_delta_gaps = session.cars[
                session.player_car_idx
            ].get_delta_gaps_ahead(session.cars, session.positions)
            assert -0.4 == pytest.approx(sorted_delta_gaps[0].delta_gap)
            assert session.cars[sorted_delta_gaps[0].car_idx].position == 2
            break


def test_caught_call(laps_p3_loader: Loader) -> None:
    session: Session | None = None
    tick_990_caught_fact: CaughtFact | None = None
    for snapshot in laps_p3_loader.snapshots():
        session = handle_frame(session, snapshot)
        event_facts = handle_events(session)
        if session.session_tick == 990:
            assert len(event_facts) == 1
            assert isinstance(event_facts[0], CaughtFact)
            tick_990_caught_fact = event_facts[0]
            break

    assert isinstance(tick_990_caught_fact, CaughtFact)
    assert tick_990_caught_fact.pos == 2
    assert tick_990_caught_fact.gain_s_as_positive == pytest.approx(0.4)
    assert tick_990_caught_fact.gap_fact.pos == 2
    assert tick_990_caught_fact.gap_fact.gap_s_as_positive == pytest.approx(0.58)


def test_lap_time_from_crossings(laps_session: Session) -> None:
    car_0_laps = laps_session.cars[0].laps[0]
    car_1_laps = laps_session.cars[1].laps[0]
    assert car_0_laps[1].lap_time_s == pytest.approx(4.0)
    assert car_1_laps[1].lap_time_s == pytest.approx(50 / 13)


def test_first_lap_has_no_lap_time(rolling_start_session: Session) -> None:
    player_race_laps = rolling_start_session.player_car.laps[
        rolling_start_session.player_car.session_num
    ]
    assert player_race_laps[0].lap_time_s is None
