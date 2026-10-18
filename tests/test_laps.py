import pytest

from soma.handler import handle_frame
from soma.loader import Loader
from soma.session import Session


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


def test_sorted_delta_gaps(laps_p2_loader: Loader) -> None:
    session: Session | None = None
    for snapshot in laps_p2_loader.snapshots():
        session = handle_frame(session, snapshot)
