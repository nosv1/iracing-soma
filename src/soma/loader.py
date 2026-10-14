from pathlib import Path


class Snapshot:
    def __init__(self) -> None:
        pass


class Loader:
    def __init__(self, recordings_path: Path) -> None:
        self.recordings_path = recordings_path
        self.f = open(recordings_path, "r")
