import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml

from soma.exceptions import CorruptRecordingsError
from soma.irsdk_vars import SESSION_TICK


@dataclass
class Snapshot:
    frame: dict
    session_yaml: dict


class Loader:
    def __init__(self, recordings_path: Path) -> None:
        self.recordings_path = recordings_path
        self.latest_session_yaml: dict = {}
        self.yaml_dir = recordings_path / "yaml_history"
        with open(self.yaml_dir / "index.json") as f:
            self.yaml_history_index: dict[str, str] = json.load(f)

    def lines(self) -> Iterator[str]:
        with open(self.recordings_path / "frames.txt") as f:
            for line in f:
                yield line.strip("\n")

    def snapshots(self) -> Iterator[Snapshot]:
        for line in self.lines():
            frame = json.loads(line)
            tick_as_str = str(frame[SESSION_TICK])
            if tick_as_str in self.yaml_history_index:
                session_yaml_file: Path = (
                    self.yaml_dir / self.yaml_history_index[tick_as_str]
                )
                session_yaml_bytes = session_yaml_file.read_bytes().decode("cp1252")
                session_yaml = yaml.safe_load(session_yaml_bytes)

                self.latest_session_yaml = session_yaml
                del self.yaml_history_index[tick_as_str]

            yield Snapshot(frame=frame, session_yaml=self.latest_session_yaml)

        if self.yaml_history_index is not {}:
            raise CorruptRecordingsError(
                "YAML history should have been emptied by the time all frames are loaded. There is a mismatch somewhere, each YAML tick should exist as a frame in frames.txt"
                "\n".join(
                    [f"missing: {tick}" for tick in self.yaml_history_index.keys()]
                )
            )
