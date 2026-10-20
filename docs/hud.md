# HUD replacement

Goal: race with the HUD off. Each element below becomes a voice call that either **speaks up**
on a trigger or is **asked** for (a router question). An element is done when you've raced with
it hidden and didn't miss it.

Mode is my first guess; priority and "done" are yours.

| HUD element | Source | Mode | Priority | Done |
| --- | --- | --- | --- | --- |
| Flags (yellow, blue, black, white, checkered) | `SessionFlags` (bitfield) | speaks up | | |
| Car alongside | `CarLeftRight` | speaks up (spotter) | | |
| Incidents | `PlayerCarMyIncidentCount` | speaks up on change | | |
| Position (overall, class) | `PlayerCarPosition`, `PlayerCarClassPosition` | speaks up on change? asked | | |
| Laps left | `SessionLapsRemainEx` | asked; milestones speak up | | |
| Time left | `SessionTimeRemain` | asked; milestones speak up | | |
| Gap ahead / behind | his crossings (`soma/car.py`) | asked; caught call speaks up | | |
| Lap time, best lap | `LapLastLapTime`, `LapBestLapTime` | asked | | |
| Delta to best | `LapDeltaToSessionBestLap` | asked? | | |
| Fuel | `FuelLevel` + his burn model | asked; warning speaks up | | |
| Tyre wear | `LFwearM` etc. (updates in the pits only?) | asked | | |
| Repairs | damage: `EngineWarnings` 0x80 / 0x100; time: `PitRepairLeft`, `PitOptRepairLeft` (0 on track, 10-20) | speaks up on damage | | |
| Engine warnings (water temp, oil pressure) | `EngineWarnings` (bitfield) | speaks up | | |
| Track / air temp | `TrackTempCrew`, `AirTemp` | asked | | |

## DRE calls not covered above

<!-- calls DRE makes that you'd miss; add as you notice them -->
