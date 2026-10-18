from collections.abc import Iterator
from pathlib import Path

import pytest

from soma.driver import Driver
from soma.handler import handle_frame
from soma.irsdk_vars import SESSION_TICK
from soma.loader import Loader, Snapshot
from soma.session import Session


def get_idx_snapshot_dict(loader: Loader) -> dict[int, Snapshot]:
    return {s[SESSION_TICK]: s for s in loader.snapshots()}


@pytest.fixture(scope="module")
def recordings_path() -> Path:
    return Path(__file__).parent / "recordings"


############       VALID FIXTURES       ############


@pytest.fixture
def valid_loader(recordings_path: Path) -> Loader:
    return Loader(recordings_path / "valid")


@pytest.fixture
def valid_snapshots_dict(valid_loader: Loader) -> dict[int, Snapshot]:
    return get_idx_snapshot_dict(valid_loader)


@pytest.fixture
def valid_driver_dict(valid_snapshots_dict: dict[int, Snapshot]) -> dict[int, Driver]:
    return Driver.drivers_from_frame(valid_snapshots_dict[600])


############       LAPS FIXTURES       ############


@pytest.fixture(scope="module")
def laps_loader(recordings_path: Path) -> Loader:
    return Loader(recordings_path / "laps")


@pytest.fixture(scope="module")
def snapshots_with_laps_iterator(laps_loader: Loader) -> Iterator[Snapshot]:
    return laps_loader.snapshots()


@pytest.fixture(scope="module")
def laps_session(snapshots_with_laps_iterator: Iterator[Snapshot]) -> Session:
    session: Session | None = None
    for snapshot in snapshots_with_laps_iterator:
        session = handle_frame(session, snapshot)
    assert session is not None
    return session
