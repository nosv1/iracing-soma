from dataclasses import dataclass


@dataclass(frozen=True)
class RaceDistanceMilestoneAsLap:
    laps_remaining: int


@dataclass(frozen=True)
class RaceDistanceMilestoneAsPercentRemaining:
    percent_remaining: float


@dataclass
class PlayerConstants:
    race_milestones: list[
        RaceDistanceMilestoneAsLap | RaceDistanceMilestoneAsPercentRemaining
    ]
