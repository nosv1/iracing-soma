from collections.abc import Iterator
from pathlib import Path

import pytest
from piper import PiperVoice

from soma.driver import Driver
from soma.handler import handle_frame
from soma.irsdk_vars import SESSION_TICK
from soma.loader import Loader, Snapshot
from soma.session import Session
from soma.speaker import Speaker


def get_idx_snapshot_dict(loader: Loader) -> dict[int, Snapshot]:
    return {s[SESSION_TICK]: s for s in loader.snapshots()}


@pytest.fixture(scope="module")
def recordings_path() -> Path:
    return Path(__file__).parent / "recordings"


@pytest.fixture(scope="module")
def speaker() -> Speaker:
    cur_dir = Path(__file__).parent / ".."
    voices_dir = cur_dir / "voices"
    voice_path = voices_dir / "en_GB-southern_english_female-low.onnx"
    speaker = Speaker(voice=PiperVoice.load(voice_path))
    return speaker


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
def laps_p2_loader(recordings_path: Path) -> Loader:
    return Loader(recordings_path / "laps_p2")


@pytest.fixture(scope="module")
def laps_p3_loader(recordings_path: Path) -> Loader:
    return Loader(recordings_path / "laps_p3")


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


############       ROLLING START       ############


@pytest.fixture(scope="module")
def rolling_start_session(recordings_path: Path) -> Session:
    session: Session | None = None
    for snapshot in Loader(recordings_path / "rolling_start").snapshots():
        session = handle_frame(session, snapshot)
    assert session is not None
    return session
