import logging

import pytest

from soma.handler import handle_events, handle_frame
from soma.loader import Loader
from soma.session import Session
from soma.speaker import Speaker

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


@pytest.mark.parametrize(
    "idx, expected", [(0, [0.388, 4.388]), (1, [0.769231, 4.615385])]
)
def test_lap_timestamps(laps_session: Session, idx: int, expected: list[float]) -> None:
    assert len(laps_session.cars[0].laps) == 2 and len(laps_session.cars[1].laps) == 2
    actual_timestamps = []
    for lap in laps_session.cars[idx].laps:
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


def test_caught_call(laps_p3_loader: Loader, speaker: Speaker) -> None:
    try:
        session: Session | None = None
        for snapshot in laps_p3_loader.snapshots():
            session = handle_frame(session, snapshot)
            handle_events(session, speaker)
    finally:
        speaker.stop()
