from dataclasses import dataclass
from typing import Any


@dataclass
class Snapshot:
    frame: dict[str, Any]
    session_yaml: dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        if key in self.session_yaml:
            return self.session_yaml[key]
        if key in self.frame:
            return self.frame[key]
        raise KeyError(key)
