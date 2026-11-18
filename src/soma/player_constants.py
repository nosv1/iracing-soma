from dataclasses import dataclass, field


@dataclass(frozen=True)
class RaceDistanceMilestoneAsLap:
    laps_remaining: int


@dataclass(frozen=True)
class RaceDistanceMilestoneAsPercentRemaining:
    percent_remaining: float


@dataclass(frozen=True)
class PlayerConstants:
    race_milestones: list[
        RaceDistanceMilestoneAsLap | RaceDistanceMilestoneAsPercentRemaining
    ] = field(default_factory=list)
