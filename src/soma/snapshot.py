from dataclasses import dataclass


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
