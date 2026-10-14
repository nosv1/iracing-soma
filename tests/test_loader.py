from pathlib import Path

import pytest

from soma.exceptions import CorruptRecordingsError
from soma.irsdk_vars import DRIVER_INFO, DRIVERS, SESSION_TICK, USER_NAME
from soma.loader import Loader, Snapshot

RECORDINGS = Path(__file__).parent / "recordings"


@pytest.fixture
def valid_loader() -> Loader:
    return Loader(RECORDINGS / "valid")


@pytest.fixture
def valid_snapshots_dict(valid_loader: Loader) -> dict[int, Snapshot]:
    return {s[SESSION_TICK]: s for s in valid_loader.snapshots()}


def test_yaml_decoded_correctly(valid_snapshots_dict: dict[int, Snapshot]):
    # confirm �nders Nilsson is loaded to Ånders Nilsson
    snapshot = valid_snapshots_dict[600]
    assert snapshot[DRIVER_INFO][DRIVERS][1][USER_NAME] == "Ånders Nilsson"


def test_all_tick_numbers_loaded(valid_snapshots_dict: dict[int, Snapshot]):
    expected_tick_numbers = set(range(600, 654 + 1, 6))
    assert valid_snapshots_dict.keys() == expected_tick_numbers


def test_yaml_switched_over_correctly(valid_snapshots_dict: dict[int, Snapshot]):
    prev_snapshot = valid_snapshots_dict[624]
    assert len(prev_snapshot[DRIVER_INFO][DRIVERS]) == 2

    new_snapshot = valid_snapshots_dict[630]
    assert len(new_snapshot[DRIVER_INFO][DRIVERS]) == 3


def test_tick_without_frame() -> None:
    with pytest.raises(CorruptRecordingsError):
        loader = Loader(RECORDINGS / "yaml_tick_without_frame")
        list(loader.snapshots())
