import json
from collections.abc import Iterator
from copy import copy
from dataclasses import dataclass
from pathlib import Path

import yaml

from soma.exceptions import CorruptRecordingsError
from soma.irsdk_vars import SESSION_TICK


@dataclass
class Snapshot:
    frame: dict
    session_yaml: dict

    def __getitem__(self, key):
        if key in self.session_yaml:
            return self.session_yaml[key]
        if key in self.frame:
            return self.frame[key]
        raise KeyError(key)


class Loader:
    def __init__(self, recordings_path: Path) -> None:
        self.recordings_path = recordings_path
        self.yaml_dir = recordings_path / "yaml_history"
        with open(self.yaml_dir / "index.json") as f:
            self._yaml_history_index: dict[str, str] = json.load(f)

    def lines(self) -> Iterator[str]:
        with open(self.recordings_path / "frames.txt") as f:
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
                "YAML history should have been emptied by the time all frames are loaded. "
                "There is a mismatch somewhere, each YAML tick should exist as a frame in frames.txt\n"
                "\n".join(
                    [f"missing: {tick}" for tick in self._yaml_history_index.keys()]
                )
            )
