from pathlib import Path

import pytest

from soma.driver import Driver
from soma.irsdk_vars import SESSION_TICK
from soma.loader import Loader, Snapshot


@pytest.fixture
def recordings_path() -> Path:
    return Path(__file__).parent / "recordings"


@pytest.fixture
def valid_loader(recordings_path: Path) -> Loader:
    return Loader(recordings_path / "valid")


@pytest.fixture
def valid_snapshots_dict(valid_loader: Loader) -> dict[int, Snapshot]:
    return {s[SESSION_TICK]: s for s in valid_loader.snapshots()}


@pytest.fixture
def valid_driver_dict(valid_snapshots_dict: dict[int, Snapshot]) -> dict[int, Driver]:
    return Driver.drivers_from_frame(valid_snapshots_dict[600])
