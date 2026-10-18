import json
from collections.abc import Iterator
from copy import copy
from pathlib import Path

import yaml

from soma.exceptions import CorruptRecordingsError
from soma.irsdk_vars import SESSION_TICK
from soma.snapshot import Snapshot


class Loader:
    def __init__(self, recording_path: Path) -> None:
        self.recording_path = recording_path
        self.yaml_dir = recording_path / "yaml_history"
        with open(self.yaml_dir / "index.json") as f:
            self._yaml_history_index: dict[str, str] = json.load(f)

    def lines(self) -> Iterator[str]:
        with open(self.recording_path / "frames.txt") as f:
            for line in f:
                yield line.strip("\n")

    def snapshots(self) -> Iterator[Snapshot]:
        local_yaml_history_index = copy(self._yaml_history_index)
        latest_session_yaml: dict = {}

        for line in self.lines():
            frame = json.loads(line)
            tick_as_str = str(frame[SESSION_TICK])
            if tick_as_str in local_yaml_history_index:
                session_yaml_file: Path = (
                    self.yaml_dir / local_yaml_history_index[tick_as_str]
                )
                session_yaml_bytes = session_yaml_file.read_bytes().decode("cp1252")
                session_yaml: dict = yaml.safe_load(session_yaml_bytes)

                latest_session_yaml = session_yaml
                del local_yaml_history_index[tick_as_str]

            yield Snapshot(frame=frame, session_yaml=latest_session_yaml)

        if len(local_yaml_history_index.keys()) != 0:
            raise CorruptRecordingsError(
                "YAML history should have been emptied by the time all frames are loaded."
                "There is a mismatch somewhere, each YAML tick should exist as a frame in frames.txt\n"
                "\n".join(
                    [f"missing: {tick}" for tick in self._yaml_history_index.keys()]
                )
            )
