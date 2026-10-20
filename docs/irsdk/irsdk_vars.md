# pyirsdk telemetry variables

From pyirsdk's [vars.txt](https://github.com/kutu/pyirsdk/blob/master/vars.txt). Not the full list:
some cars expose extra variables (brake bias, wing adjustment, etc.).

| Variable | Description | Unit |
|---|---|---|
| `AirDensity` | Density of air at start/finish line | kg/m^3 |
| `AirPressure` | Pressure of air at start/finish line | Pa |
| `AirTemp` | Temperature of air at start/finish line | C |
| `Brake` | 0=brake released to 1=max pedal force | % |
| `BrakeABSactive` | true if abs is currently reducing brake force pressure |  |
| `BrakeRaw` | Raw brake input 0=brake released to 1=max pedal force | % |
| `CamCameraNumber` | Active camera number |  |
| `CamCameraState` | State of camera system | irsdk_CameraState |
| `CamCarIdx` | Active camera's focus car index |  |
| `CamGroupNumber` | Active camera group number |  |
| `CarDistAhead` | Distance to first car in front of player in meters | m |
| `CarDistBehind` | Distance to first car behind player in meters | m |
| `CarIdxBestLapNum` | Cars best lap number |  |
| `CarIdxBestLapTime` | Cars best lap time | s |
| `CarIdxClass` | Cars class id by car index |  |
| `CarIdxClassPosition` | Cars class position in race by car index |  |
| `CarIdxEstTime` | Estimated time to reach current location on track | s |
| `CarIdxF2Time` | Race time behind leader or fastest lap time otherwise | s |
| `CarIdxFastRepairsUsed` | How many fast repairs each car has used |  |
| `CarIdxGear` | -1=reverse 0=neutral 1..n=current gear by car index |  |
| `CarIdxLap` | Laps started by car index |  |
| `CarIdxLapCompleted` | Laps completed by car index |  |
| `CarIdxLapDistPct` | Percentage distance around lap by car index | % |
| `CarIdxLastLapTime` | Cars last lap time | s |
| `CarIdxOnPitRoad` | On pit road between the cones by car index |  |
| `CarIdxP2P_Count` | Push2Pass count of usage (or remaining in Race) |  |
| `CarIdxP2P_Status` | Push2Pass active or not |  |
| `CarIdxPaceFlags` | Pacing status flags for each car | irsdk_PaceFlags |
| `CarIdxPaceLine` | What line cars are pacing in or -1 if not pacing |  |
| `CarIdxPaceRow` | What row cars are pacing in or -1 if not pacing |  |
| `CarIdxPosition` | Cars position in race by car index |  |
| `CarIdxQualTireCompound` | Cars Qual tire compound |  |
| `CarIdxQualTireCompoundLocked` | Cars Qual tire compound is locked-in |  |
| `CarIdxRPM` | Engine rpm by car index | revs/min |
| `CarIdxSessionFlags` | Session flags for each player | irsdk_Flags |
| `CarIdxSteer` | Steering wheel angle by car index | rad |
| `CarIdxTireCompound` | Cars current tire compound |  |
| `CarIdxTrackSurface` | Track surface type by car index | irsdk_TrkLoc |
| `CarIdxTrackSurfaceMaterial` | Track surface material type by car index | irsdk_TrkSurf |
| `CarLeftRight` | Notify if car is to the left or right of driver | irsdk_CarLeftRight |
| `ChanAvgLatency` | Communications average latency | s |
| `ChanClockSkew` | Communications server clock skew | s |
| `ChanLatency` | Communications latency | s |
| `ChanPartnerQuality` | Partner communications quality | % |
| `ChanQuality` | Communications quality | % |
| `Clutch` | 0=disengaged to 1=fully engaged | % |
| `ClutchRaw` | Raw clutch input 0=disengaged to 1=fully engaged | % |
| `CpuUsageBG` | Percent of available time bg thread took with a 1 sec avg | % |
| `CpuUsageFG` | Percent of available time fg thread took with a 1 sec avg | % |
| `DCDriversSoFar` | Number of team drivers who have run a stint |  |
| `DCLapStatus` | Status of driver change lap requirements |  |
| `dcPitSpeedLimiterToggle` | Track if pit speed limiter system is enabled |  |
| `dcStarter` | In car trigger car starter |  |
| `dcToggleWindshieldWipers` | In car turn wipers on or off |  |
| `dcTriggerWindshieldWipers` | In car momentarily turn on wipers |  |
| `DisplayUnits` | Default units for the user interface 0 = english 1 = metric |  |
| `dpFastRepair` | Pitstop fast repair set |  |
| `dpFuelAddKg` | Pitstop fuel add amount | kg |
| `dpFuelAutoFillActive` | Pitstop auto fill fuel next stop flag |  |
| `dpFuelAutoFillEnabled` | Pitstop auto fill fuel system enabled |  |
| `dpFuelFill` | Pitstop fuel fill flag |  |
| `dpLFTireChange` | Pitstop lf tire change request |  |
| `dpLFTireColdPress` | Pitstop lf tire cold pressure adjustment | Pa |
| `dpLRTireChange` | Pitstop lr tire change request |  |
| `dpLRTireColdPress` | Pitstop lr tire cold pressure adjustment | Pa |
| `dpRFTireChange` | Pitstop rf tire change request |  |
| `dpRFTireColdPress` | Pitstop rf cold tire pressure adjustment | Pa |
| `dpRRTireChange` | Pitstop rr tire change request |  |
| `dpRRTireColdPress` | Pitstop rr cold tire pressure adjustment | Pa |
| `dpWindshieldTearoff` | Pitstop windshield tearoff |  |
| `DriverMarker` | Driver activated flag |  |
| `Engine0_RPM` | Engine0Engine rpm | revs/min |
| `EngineWarnings` | Bitfield for warning lights | irsdk_EngineWarnings |
| `EnterExitReset` | Indicate action the reset key will take 0 enter 1 exit 2 reset |  |
| `FastRepairAvailable` | How many fast repairs left 255 is unlimited |  |
| `FastRepairUsed` | How many fast repairs used so far |  |
| `FogLevel` | Fog level at start/finish line | % |
| `FrameRate` | Average frames per second | fps |
| `FrontTireSetsAvailable` | How many front tire sets are remaining 255 is unlimited |  |
| `FrontTireSetsUsed` | How many front tire sets used so far |  |
| `FuelLevel` | Liters of fuel remaining | l |
| `FuelLevelPct` | Percent fuel remaining | % |
| `FuelPress` | Engine fuel pressure | bar |
| `FuelUsePerHour` | Engine fuel used instantaneous | kg/h |
| `Gear` | -1=reverse 0=neutral 1..n=current gear |  |
| `GpuUsage` | Percent of available time gpu took with a 1 sec avg | % |
| `HandbrakeRaw` | Raw handbrake input 0=handbrake released to 1=max force | % |
| `IsDiskLoggingActive` | 0=disk based telemetry file not being written 1=being written |  |
| `IsDiskLoggingEnabled` | 0=disk based telemetry turned off 1=turned on |  |
| `IsGarageVisible` | 1=Garage screen is visible |  |
| `IsInGarage` | 1=Car in garage physics running |  |
| `IsOnTrack` | 1=Car on track physics running with player in car |  |
| `IsOnTrackCar` | 1=Car on track physics running |  |
| `IsReplayPlaying` | 0=replay not playing 1=replay playing |  |
| `Lap` | Laps started count |  |
| `LapBestLap` | Players best lap number |  |
| `LapBestLapTime` | Players best lap time | s |
| `LapBestNLapLap` | Player last lap in best N average lap time |  |
| `LapBestNLapTime` | Player best N average lap time | s |
| `LapCompleted` | Laps completed count |  |
| `LapCurrentLapTime` | Estimate of players current lap time as shown in F3 box | s |
| `LapDeltaToBestLap` | Delta time for best lap | s |
| `LapDeltaToBestLap_DD` | Rate of change of delta time for best lap | s/s |
| `LapDeltaToBestLap_OK` | Delta time for best lap is valid |  |
| `LapDeltaToOptimalLap` | Delta time for optimal lap | s |
| `LapDeltaToOptimalLap_DD` | Rate of change of delta time for optimal lap | s/s |
| `LapDeltaToOptimalLap_OK` | Delta time for optimal lap is valid |  |
| `LapDeltaToSessionBestLap` | Delta time for session best lap | s |
| `LapDeltaToSessionBestLap_DD` | Rate of change of delta time for session best lap | s/s |
| `LapDeltaToSessionBestLap_OK` | Delta time for session best lap is valid |  |
| `LapDeltaToSessionLastlLap` | Delta time for session last lap | s |
| `LapDeltaToSessionLastlLap_DD` | Rate of change of delta time for session last lap | s/s |
| `LapDeltaToSessionLastlLap_OK` | Delta time for session last lap is valid |  |
| `LapDeltaToSessionOptimalLap` | Delta time for session optimal lap | s |
| `LapDeltaToSessionOptimalLap_DD` | Rate of change of delta time for session optimal lap | s/s |
| `LapDeltaToSessionOptimalLap_OK` | Delta time for session optimal lap is valid |  |
| `LapDist` | Meters traveled from S/F this lap | m |
| `LapDistPct` | Percentage distance around lap | % |
| `LapLasNLapSeq` | Player num consecutive clean laps completed for N average |  |
| `LapLastLapTime` | Players last lap time | s |
| `LapLastNLapTime` | Player last N average lap time | s |
| `LatAccel` | Lateral acceleration (including gravity) | m/s^2 |
| `LatAccel_ST` | Lateral acceleration (including gravity) at 360 Hz | m/s^2 |
| `LeftTireSetsAvailable` | How many left tire sets are remaining 255 is unlimited |  |
| `LeftTireSetsUsed` | How many left tire sets used so far |  |
| `LFbrakeLinePress` | LF brake line pressure | bar |
| `LFcoldPressure` | LF tire cold pressure as set in the garage | kPa |
| `LFodometer` | LF distance tire traveled since being placed on car | m |
| `LFshockDefl` | LF shock deflection | m |
| `LFshockDefl_ST` | LF shock deflection at 360 Hz | m |
| `LFshockVel` | LF shock velocity | m/s |
| `LFshockVel_ST` | LF shock velocity at 360 Hz | m/s |
| `LFtempCL` | LF tire left carcass temperature | C |
| `LFtempCM` | LF tire middle carcass temperature | C |
| `LFtempCR` | LF tire right carcass temperature | C |
| `LFTiresAvailable` | How many left front tires are remaining 255 is unlimited |  |
| `LFTiresUsed` | How many left front tires used so far |  |
| `LFwearL` | LF tire left percent tread remaining | % |
| `LFwearM` | LF tire middle percent tread remaining | % |
| `LFwearR` | LF tire right percent tread remaining | % |
| `LoadNumTextures` | True if the car_num texture will be loaded |  |
| `LongAccel` | Longitudinal acceleration (including gravity) | m/s^2 |
| `LongAccel_ST` | Longitudinal acceleration (including gravity) at 360 Hz | m/s^2 |
| `LRbrakeLinePress` | LR brake line pressure | bar |
| `LRcoldPressure` | LR tire cold pressure as set in the garage | kPa |
| `LRodometer` | LR distance tire traveled since being placed on car | m |
| `LRshockDefl` | LR shock deflection | m |
| `LRshockDefl_ST` | LR shock deflection at 360 Hz | m |
| `LRshockVel` | LR shock velocity | m/s |
| `LRshockVel_ST` | LR shock velocity at 360 Hz | m/s |
| `LRtempCL` | LR tire left carcass temperature | C |
| `LRtempCM` | LR tire middle carcass temperature | C |
| `LRtempCR` | LR tire right carcass temperature | C |
| `LRTiresAvailable` | How many left rear tires are remaining 255 is unlimited |  |
| `LRTiresUsed` | How many left rear tires used so far |  |
| `LRwearL` | LR tire left percent tread remaining | % |
| `LRwearM` | LR tire middle percent tread remaining | % |
| `LRwearR` | LR tire right percent tread remaining | % |
| `ManifoldPress` | Engine manifold pressure | bar |
| `ManualBoost` | Hybrid manual boost state |  |
| `ManualNoBoost` | Hybrid manual no boost state |  |
| `MemPageFaultSec` | Memory page faults per second |  |
| `MemSoftPageFaultSec` | Memory soft page faults per second |  |
| `OilLevel` | Engine oil level | l |
| `OilPress` | Engine oil pressure | bar |
| `OilTemp` | Engine oil temperature | C |
| `OkToReloadTextures` | True if it is ok to reload car textures at this time |  |
| `OnPitRoad` | Is the player car on pit road between the cones |  |
| `P2P_Count` | Push2Pass count of usage (or remaining in Race) on your car |  |
| `P2P_Status` | Push2Pass active or not on your car |  |
| `PaceMode` | Are we pacing or not | irsdk_PaceMode |
| `Pitch` | Pitch orientation | rad |
| `PitchRate` | Pitch rate | rad/s |
| `PitchRate_ST` | Pitch rate at 360 Hz | rad/s |
| `PitOptRepairLeft` | Time left for optional repairs if repairs are active | s |
| `PitRepairLeft` | Time left for mandatory pit repairs if repairs are active | s |
| `PitsOpen` | True if pit stop is allowed for the current player |  |
| `PitstopActive` | Is the player getting pit stop service |  |
| `PitSvFlags` | Bitfield of pit service checkboxes | irsdk_PitSvFlags |
| `PitSvFuel` | Pit service fuel add amount | l or kWh |
| `PitSvLFP` | Pit service left front tire pressure | kPa |
| `PitSvLRP` | Pit service left rear tire pressure | kPa |
| `PitSvRFP` | Pit service right front tire pressure | kPa |
| `PitSvRRP` | Pit service right rear tire pressure | kPa |
| `PitSvTireCompound` | Pit service pending tire compound |  |
| `PlayerCarClass` | Player car class id |  |
| `PlayerCarClassPosition` | Players class position in race |  |
| `PlayerCarDriverIncidentCount` | Teams current drivers incident count for this session |  |
| `PlayerCarDryTireSetLimit` | Players dry tire set limit |  |
| `PlayerCarIdx` | Players carIdx |  |
| `PlayerCarInPitStall` | Players car is properly in their pitstall |  |
| `PlayerCarMyIncidentCount` | Players own incident count for this session |  |
| `PlayerCarPitSvStatus` | Players car pit service status bits | irsdk_PitSvStatus |
| `PlayerCarPosition` | Players position in race |  |
| `PlayerCarPowerAdjust` | Players power adjust | % |
| `PlayerCarSLBlinkRPM` | Shift light blink rpm | revs/min |
| `PlayerCarSLFirstRPM` | Shift light first light rpm | revs/min |
| `PlayerCarSLLastRPM` | Shift light last light rpm | revs/min |
| `PlayerCarSLShiftRPM` | Shift light shift rpm | revs/min |
| `PlayerCarTeamIncidentCount` | Players team incident count for this session |  |
| `PlayerCarTowTime` | Players car is being towed if time is greater than zero | s |
| `PlayerCarWeightPenalty` | Players weight penalty | kg |
| `PlayerFastRepairsUsed` | Players car number of fast repairs used |  |
| `PlayerIncidents` | Log incidents that the player recieved | irsdk_IncidentFlags |
| `PlayerTireCompound` | Players car current tire compound |  |
| `PlayerTrackSurface` | Players car track surface type | irsdk_TrkLoc |
| `PlayerTrackSurfaceMaterial` | Players car track surface material type | irsdk_TrkSurf |
| `Precipitation` | Precipitation at start/finish line | % |
| `PushToPass` | Push to pass button state |  |
| `PushToTalk` | Push to talk button state |  |
| `RaceLaps` | Laps completed in race |  |
| `RadioTransmitCarIdx` | The car index of the current person speaking on the radio |  |
| `RadioTransmitFrequencyIdx` | The frequency index of the current person speaking on the radio |  |
| `RadioTransmitRadioIdx` | The radio index of the current person speaking on the radio |  |
| `RearTireSetsAvailable` | How many rear tire sets are remaining 255 is unlimited |  |
| `RearTireSetsUsed` | How many rear tire sets used so far |  |
| `RelativeHumidity` | Relative Humidity at start/finish line | % |
| `ReplayFrameNum` | Integer replay frame number (60 per second) |  |
| `ReplayFrameNumEnd` | Integer replay frame number from end of tape |  |
| `ReplayPlaySlowMotion` | 0=not slow motion 1=replay is in slow motion |  |
| `ReplayPlaySpeed` | Replay playback speed |  |
| `ReplaySessionNum` | Replay session number |  |
| `ReplaySessionTime` | Seconds since replay session start | s |
| `RFbrakeLinePress` | RF brake line pressure | bar |
| `RFcoldPressure` | RF tire cold pressure as set in the garage | kPa |
| `RFodometer` | RF distance tire traveled since being placed on car | m |
| `RFshockDefl` | RF shock deflection | m |
| `RFshockDefl_ST` | RF shock deflection at 360 Hz | m |
| `RFshockVel` | RF shock velocity | m/s |
| `RFshockVel_ST` | RF shock velocity at 360 Hz | m/s |
| `RFtempCL` | RF tire left carcass temperature | C |
| `RFtempCM` | RF tire middle carcass temperature | C |
| `RFtempCR` | RF tire right carcass temperature | C |
| `RFTiresAvailable` | How many right front tires are remaining 255 is unlimited |  |
| `RFTiresUsed` | How many right front tires used so far |  |
| `RFwearL` | RF tire left percent tread remaining | % |
| `RFwearM` | RF tire middle percent tread remaining | % |
| `RFwearR` | RF tire right percent tread remaining | % |
| `RightTireSetsAvailable` | How many right tire sets are remaining 255 is unlimited |  |
| `RightTireSetsUsed` | How many right tire sets used so far |  |
| `Roll` | Roll orientation | rad |
| `RollRate` | Roll rate | rad/s |
| `RollRate_ST` | Roll rate at 360 Hz | rad/s |
| `RPM` | Engine rpm | revs/min |
| `RRbrakeLinePress` | RR brake line pressure | bar |
| `RRcoldPressure` | RR tire cold pressure as set in the garage | kPa |
| `RRodometer` | RR distance tire traveled since being placed on car | m |
| `RRshockDefl` | RR shock deflection | m |
| `RRshockDefl_ST` | RR shock deflection at 360 Hz | m |
| `RRshockVel` | RR shock velocity | m/s |
| `RRshockVel_ST` | RR shock velocity at 360 Hz | m/s |
| `RRtempCL` | RR tire left carcass temperature | C |
| `RRtempCM` | RR tire middle carcass temperature | C |
| `RRtempCR` | RR tire right carcass temperature | C |
| `RRTiresAvailable` | How many right rear tires are remaining 255 is unlimited |  |
| `RRTiresUsed` | How many right rear tires used so far |  |
| `RRwearL` | RR tire left percent tread remaining | % |
| `RRwearM` | RR tire middle percent tread remaining | % |
| `RRwearR` | RR tire right percent tread remaining | % |
| `SessionFlags` | Session flags | irsdk_Flags |
| `SessionJokerLapsRemain` | Joker laps remaining to be taken |  |
| `SessionLapsRemain` | Old laps left till session ends use SessionLapsRemainEx |  |
| `SessionLapsRemainEx` | New improved laps left till session ends |  |
| `SessionLapsTotal` | Total number of laps in session |  |
| `SessionNum` | Session number |  |
| `SessionOnJokerLap` | Player is currently completing a joker lap |  |
| `SessionState` | Session state | irsdk_SessionState |
| `SessionTick` | Current update number |  |
| `SessionTime` | Seconds since session start | s |
| `SessionTimeOfDay` | Time of day in seconds | s |
| `SessionTimeRemain` | Seconds left till session ends | s |
| `SessionTimeTotal` | Total number of seconds in session | s |
| `SessionUniqueID` | Session ID |  |
| `Shifter` | Log inputs from the players shifter control |  |
| `ShiftGrindRPM` | RPM of shifter grinding noise | RPM |
| `ShiftIndicatorPct` | DEPRECATED use DriverCarSLBlinkRPM instead | % |
| `ShiftPowerPct` | Friction torque applied to gears when shifting or grinding | % |
| `Skies` | Skies (0=clear/1=p cloudy/2=m cloudy/3=overcast) |  |
| `SolarAltitude` | Sun angle above horizon in radians | rad |
| `SolarAzimuth` | Sun angle clockwise from north in radians | rad |
| `Speed` | GPS vehicle speed | m/s |
| `SteeringFFBEnabled` | Force feedback is enabled |  |
| `SteeringWheelAngle` | Steering wheel angle | rad |
| `SteeringWheelAngleMax` | Steering wheel max angle | rad |
| `SteeringWheelLimiter` | Force feedback limiter strength limits impacts and oscillation | % |
| `SteeringWheelMaxForceNm` | Value of strength or max force slider in Nm for FFB | N*m |
| `SteeringWheelPctDamper` | Force feedback % max damping | % |
| `SteeringWheelPctIntensity` | Force feedback % max intensity | % |
| `SteeringWheelPctSmoothing` | Force feedback % max smoothing | % |
| `SteeringWheelPctTorque` | Force feedback % max torque on steering shaft unsigned | % |
| `SteeringWheelPctTorqueSign` | Force feedback % max torque on steering shaft signed | % |
| `SteeringWheelPctTorqueSignStops` | Force feedback % max torque on steering shaft signed stops | % |
| `SteeringWheelPeakForceNm` | Peak torque mapping to direct input units for FFB | N*m |
| `SteeringWheelTorque` | Output torque on steering shaft | N*m |
| `SteeringWheelTorque_ST` | Output torque on steering shaft at 360 Hz | N*m |
| `SteeringWheelUseLinear` | True if steering wheel force is using linear mode |  |
| `Throttle` | 0=off throttle to 1=full throttle | % |
| `ThrottleRaw` | Raw throttle input 0=off throttle to 1=full throttle | % |
| `TireLF_RumblePitch` | Players LF Tire Sound rumblestrip pitch | Hz |
| `TireLR_RumblePitch` | Players LR Tire Sound rumblestrip pitch | Hz |
| `TireRF_RumblePitch` | Players RF Tire Sound rumblestrip pitch | Hz |
| `TireRR_RumblePitch` | Players RR Tire Sound rumblestrip pitch | Hz |
| `TireSetsAvailable` | How many tire sets are remaining 255 is unlimited |  |
| `TireSetsUsed` | How many tire sets used so far |  |
| `TrackTemp` | Deprecated set to TrackTempCrew | C |
| `TrackTempCrew` | Temperature of track measured by crew around track | C |
| `TrackWetness` | How wet is the average track surface | irsdk_TrackWetness |
| `VelocityX` | X velocity | m/s |
| `VelocityX_ST` | X velocity at 360 Hz | m/s |
| `VelocityY` | Y velocity | m/s |
| `VelocityY_ST` | Y velocity at 360 Hz | m/s |
| `VelocityZ` | Z velocity | m/s |
| `VelocityZ_ST` | Z velocity at 360 Hz | m/s |
| `VertAccel` | Vertical acceleration (including gravity) | m/s^2 |
| `VertAccel_ST` | Vertical acceleration (including gravity) at 360 Hz | m/s^2 |
| `VidCapActive` | True if video currently being captured |  |
| `VidCapEnabled` | True if video capture system is enabled |  |
| `Voltage` | Engine voltage | V |
| `WaterLevel` | Engine coolant level | l |
| `WaterTemp` | Engine coolant temp | C |
| `WeatherDeclaredWet` | The steward says rain tires can be used |  |
| `WindDir` | Wind direction at start/finish line | rad |
| `WindVel` | Wind velocity at start/finish line | m/s |
| `Yaw` | Yaw orientation | rad |
| `YawNorth` | Yaw orientation relative to north | rad |
| `YawRate` | Yaw rate | rad/s |
| `YawRate_ST` | Yaw rate at 360 Hz | rad/s |

## Session info (YAML)

Separate from the telemetry variables above. iRacing keeps a YAML document in the same shared
memory and rewrites it occasionally (driver joins, session change, results), bumping the
`SessionInfoUpdate` telemetry variable each time. `ir[key]` checks telemetry names first, then
falls back to a top-level YAML section, so `ir['DriverInfo']` returns a parsed dict even though
`DriverInfo` is not in `ir.var_headers_names`. Names overlap confusingly: `ir['SessionInfo']` is
YAML, `SessionTime` / `SessionNum` are telemetry.

Keys below were captured from a live offline AI session (2026-10-13, FIA F4 at Ledenon, weekend of
practice → qualify → race, sampled during practice). `[]` marks a list. Not exhaustive: other
session types and series may add keys.

iRacing doesn't document these keys; the descriptions are ours, inferred from names and observed
values, and "Unknown" means just that. Values with a unit are strings with the unit appended
(`TrackLength: 3.0807 km`), so parse before doing math; the Unit column shows that suffix, or the
implied unit for bare numbers.

Not listed:

- `CarSetup`: car-specific setup sheet (tires, chassis, ...); keys differ per car. Has
  `UpdateCount`.
- `QualifyResultsInfo.Results`: empty (`None`) in this session.

Observed in the same session, worth knowing:

- `CarIdx*` arrays have **72** slots (not 64). Pace car was `CarIdx` 64 (`PaceCarIdx`).
- `CarIdxPosition` / `CarIdxClassPosition`: `0` for empty slots 20–63, `-1` for slots 64–71 (incl.
  the pace car), 1-based for scored cars. A car with `CarIdxTrackSurface` -1 (not in world) kept
  its position.
- YAML `ResultsPositions[].ClassPosition` was `0` for P1, so it looks **0-based**, unlike
  `Position` and the telemetry `CarIdxClassPosition`. Verify in a multiclass race.
- `CarIdxLapDistPct`, `CarIdxLap`, `CarIdxTrackSurface` are `-1` for empty slots and for cars not
  in the world (player in garage).

Observed 2026-10-19 (`recordings/20261019-175649`), iRacing moving the player from the practice
server to the race server while connected:

- `SessionID` (325244009 → 325242874), `SubSessionID` (89493421 → 89494186) and `EventType`
  (Practice → Race) all changed. `SessionTick` reset (83673 → 59711) and `PlayerCarIdx` changed
  (35 → 18).
- `EventType` is the server's event, not the current session: the race server says `Race`
  during its own Practice. Current session = `SessionInfo.Sessions[SessionNum].SessionType`.
- Session lineup is per event: practice server had one session (0 Practice); race server had
  0 Practice, 1 Lone Qualify, 2 Race. `SessionNum` is an index, not a fixed meaning.
- On the first frame after the switch the YAML still described the practice server; the race
  server's YAML arrived 54 ticks (~1 s) later.

### WeekendInfo

| Variable | Description | Unit |
|---|---|---|
| `Encoding` | Text encoding of the YAML strings, e.g. ISO_8859_1 |  |
| `TrackName` | Internal track name, e.g. ledenon |  |
| `TrackID` | iRacing track id |  |
| `TrackLength` | Track length as measured by the sim | km |
| `TrackLengthOfficial` | Published track length | km |
| `TrackDisplayName` | Full track name for display |  |
| `TrackDisplayShortName` | Short track name for display |  |
| `TrackConfigName` | Track layout name, empty if only one layout |  |
| `TrackCity` | Track city |  |
| `TrackState` | Track state or region |  |
| `TrackCountry` | Track country |  |
| `TrackAltitude` | Track altitude | m |
| `TrackLatitude` | Track latitude (YAML labels it m; value is degrees) | deg |
| `TrackLongitude` | Track longitude (YAML labels it m; value is degrees) | deg |
| `TrackNorthOffset` | Rotation of track coordinates from north | rad |
| `TrackNumTurns` | Number of corners |  |
| `TrackPitSpeedLimit` | Pit lane speed limit | kph |
| `TrackPaceSpeed` | Pace car speed under caution | kph |
| `TrackNumPitStalls` | Number of pit stalls |  |
| `TrackType` | Track type, e.g. road course, oval |  |
| `TrackDirection` | Lap direction, e.g. neutral |  |
| `TrackWeatherType` | Weather model, e.g. Static |  |
| `TrackSkies` | Sky condition at session start |  |
| `TrackSurfaceTemp` | Track surface temperature at session start | C |
| `TrackSurfaceTempCrew` | Track surface temperature as reported to the crew | C |
| `TrackAirTemp` | Air temperature at session start | C |
| `TrackAirPressure` | Air pressure at session start | Hg |
| `TrackAirDensity` | Air density at session start | kg/m^3 |
| `TrackWindVel` | Wind speed at session start | m/s |
| `TrackWindDir` | Wind direction at session start | rad |
| `TrackRelativeHumidity` | Relative humidity at session start | % |
| `TrackFogLevel` | Fog level at session start | % |
| `TrackPrecipitation` | Precipitation at session start | % |
| `TrackCleanup` | 1 if rubber/marbles reset between sessions |  |
| `TrackDynamicTrack` | 1 if track state evolves during the session |  |
| `TrackVersion` | Track asset version |  |
| `SeriesID` | Series id, 0 offline |  |
| `SeasonID` | Season id, 0 offline |  |
| `SessionID` | Session id, 0 offline |  |
| `SubSessionID` | Subsession id (the results id online), 0 offline |  |
| `LeagueID` | League id, 0 if not a league session |  |
| `LeagueSeasonID` | League season id |  |
| `Official` | 1 if the session counts officially |  |
| `RaceWeek` | Week of the season |  |
| `EventType` | Event type, e.g. Race, Practice, Test |  |
| `Category` | Racing category, e.g. Road, Oval, Formula |  |
| `SimMode` | Sim mode, e.g. full |  |
| `TeamRacing` | 1 if team (multi-driver) event |  |
| `MinDrivers` | Minimum drivers per team |  |
| `MaxDrivers` | Maximum drivers per team |  |
| `DCRuleSet` | Driver change rules |  |
| `QualifierMustStartRace` | 1 if a qualifier must start the race |  |
| `NumCarClasses` | Number of car classes in the session |  |
| `NumCarTypes` | Number of car models in the session (pace car counts) |  |
| `HeatRacing` | 1 if heat-race format |  |
| `AltAssetTag` | Unknown |  |
| `BuildType` | Sim build type |  |
| `BuildTarget` | Sim build target |  |
| `BuildVersion` | Sim build version |  |
| `RaceFarm` | Server farm the session runs on, empty offline |  |
| `WeekendOptions.NumStarters` | Number of starters |  |
| `WeekendOptions.StartingGrid` | Grid layout, e.g. single file |  |
| `WeekendOptions.QualifyScoring` | How qualifying is scored, e.g. best lap |  |
| `WeekendOptions.CourseCautions` | Caution rule, e.g. local, full |  |
| `WeekendOptions.StandingStart` | 1 if standing start |  |
| `WeekendOptions.ShortParadeLap` | 1 if short parade lap |  |
| `WeekendOptions.Restarts` | Restart rule |  |
| `WeekendOptions.WeatherType` | Weather model chosen for the event |  |
| `WeekendOptions.Skies` | Sky setting chosen for the event |  |
| `WeekendOptions.WindDirection` | Wind direction setting, compass point |  |
| `WeekendOptions.WindSpeed` | Wind speed setting | km/h |
| `WeekendOptions.WeatherTemp` | Air temperature setting | C |
| `WeekendOptions.RelativeHumidity` | Humidity setting | % |
| `WeekendOptions.FogLevel` | Fog setting | % |
| `WeekendOptions.TimeOfDay` | In-sim start time of day |  |
| `WeekendOptions.Date` | In-sim date |  |
| `WeekendOptions.EarthRotationSpeedupFactor` | Time-of-day speedup factor |  |
| `WeekendOptions.Unofficial` | 1 if unofficial |  |
| `WeekendOptions.CommercialMode` | Licence mode, e.g. consumer |  |
| `WeekendOptions.NightMode` | Night setting, e.g. variable |  |
| `WeekendOptions.IsFixedSetup` | 1 if fixed-setup event |  |
| `WeekendOptions.StrictLapsChecking` | Lap validity rule |  |
| `WeekendOptions.HasOpenRegistration` | 1 if open registration |  |
| `WeekendOptions.HardcoreLevel` | Unknown; possibly driving-aid restriction level |  |
| `WeekendOptions.NumJokerLaps` | Required joker laps (rallycross) |  |
| `WeekendOptions.IncidentLimit` | Incident points before disqualification |  |
| `WeekendOptions.IncidentWarningInitialLimit` | Incident points before first warning |  |
| `WeekendOptions.IncidentWarningSubsequentLimit` | Incident points between later warnings |  |
| `WeekendOptions.FastRepairsLimit` | Fast repairs allowed |  |
| `WeekendOptions.GreenWhiteCheckeredLimit` | Green-white-checkered attempts allowed |  |
| `TelemetryOptions.TelemetryDiskFile` | Path of the .ibt being written, empty if disk logging is off |  |

### SessionInfo

| Variable | Description | Unit |
|---|---|---|
| `CurrentSessionNum` | Index into Sessions of the current session (same as telemetry SessionNum) |  |
| `Sessions[].SessionNum` | Session index |  |
| `Sessions[].SessionLaps` | Lap limit, or unlimited |  |
| `Sessions[].SessionTime` | Time limit, or unlimited | sec |
| `Sessions[].SessionNumLapsToAvg` | Laps averaged for qualifying results |  |
| `Sessions[].SessionType` | Session type, e.g. Practice, Open Qualify, Race |  |
| `Sessions[].SessionTrackRubberState` | Starting rubber level |  |
| `Sessions[].SessionName` | Session display name |  |
| `Sessions[].SessionSubType` | Session subtype |  |
| `Sessions[].SessionSkipped` | 1 if session was skipped |  |
| `Sessions[].SessionRunGroupsUsed` | 1 if run groups were used |  |
| `Sessions[].SessionEnforceTireCompoundChange` | 1 if a tyre compound change is required |  |
| `Sessions[].ResultsPositions[].Position` | Overall position, 1-based |  |
| `Sessions[].ResultsPositions[].ClassPosition` | Class position; 0 for P1 observed, so looks 0-based |  |
| `Sessions[].ResultsPositions[].CarIdx` | Car index |  |
| `Sessions[].ResultsPositions[].Lap` | Lap the scoring time was set on |  |
| `Sessions[].ResultsPositions[].Time` | Scoring time (best lap in practice/qualify) | s |
| `Sessions[].ResultsPositions[].FastestLap` | Lap number of fastest lap |  |
| `Sessions[].ResultsPositions[].FastestTime` | Fastest lap time | s |
| `Sessions[].ResultsPositions[].LastTime` | Last lap time | s |
| `Sessions[].ResultsPositions[].LapsLed` | Laps led |  |
| `Sessions[].ResultsPositions[].LapsComplete` | Laps completed |  |
| `Sessions[].ResultsPositions[].JokerLapsComplete` | Joker laps completed |  |
| `Sessions[].ResultsPositions[].LapsDriven` | Laps driven by this driver (team events) |  |
| `Sessions[].ResultsPositions[].Incidents` | Incident points |  |
| `Sessions[].ResultsPositions[].ReasonOutId` | Retirement reason code, 0 = running |  |
| `Sessions[].ResultsPositions[].ReasonOutStr` | Retirement reason, e.g. Running |  |
| `Sessions[].ResultsFastestLap[].CarIdx` | Car index with the session's fastest lap |  |
| `Sessions[].ResultsFastestLap[].FastestLap` | Lap number of the fastest lap |  |
| `Sessions[].ResultsFastestLap[].FastestTime` | Fastest lap time | s |
| `Sessions[].ResultsAverageLapTime` | Average lap time, -1 if not set | s |
| `Sessions[].ResultsNumCautionFlags` | Number of cautions |  |
| `Sessions[].ResultsNumCautionLaps` | Laps under caution |  |
| `Sessions[].ResultsNumLeadChanges` | Lead changes |  |
| `Sessions[].ResultsLapsComplete` | Laps completed by the leader, -1 if not set |  |
| `Sessions[].ResultsOfficial` | 1 once results are official |  |

### CameraInfo

| Variable | Description | Unit |
|---|---|---|
| `Groups[].GroupNum` | Camera group number |  |
| `Groups[].GroupName` | Camera group name, e.g. Nose |  |
| `Groups[].Cameras[].CameraNum` | Camera number within the group |  |
| `Groups[].Cameras[].CameraName` | Camera name |  |
| `Groups[].IsScenic` | True for scenic (non-car) camera groups |  |

### RadioInfo

| Variable | Description | Unit |
|---|---|---|
| `SelectedRadioNum` | Active radio |  |
| `Radios[].RadioNum` | Radio number |  |
| `Radios[].HopCount` | Unknown |  |
| `Radios[].NumFrequencies` | Number of frequencies |  |
| `Radios[].TunedToFrequencyNum` | Frequency currently tuned |  |
| `Radios[].ScanningIsOn` | 1 if scanning |  |
| `Radios[].Frequencies[].FrequencyNum` | Frequency number |  |
| `Radios[].Frequencies[].FrequencyName` | Frequency name, e.g. @ALLTEAMS |  |
| `Radios[].Frequencies[].Priority` | Scan priority |  |
| `Radios[].Frequencies[].CarIdx` | Owning car index, -1 if none |  |
| `Radios[].Frequencies[].EntryIdx` | Owning entry index, -1 if none |  |
| `Radios[].Frequencies[].ClubID` | Owning club id, 0 if none |  |
| `Radios[].Frequencies[].CanScan` | 1 if included in scanning |  |
| `Radios[].Frequencies[].CanSquawk` | 1 if you can transmit on it |  |
| `Radios[].Frequencies[].Muted` | 1 if muted |  |
| `Radios[].Frequencies[].IsMutable` | 1 if it can be muted |  |
| `Radios[].Frequencies[].IsDeletable` | 1 if it can be removed |  |

### DriverInfo

| Variable | Description | Unit |
|---|---|---|
| `DriverCarIdx` | Your car index (same as telemetry PlayerCarIdx) |  |
| `DriverUserID` | Your iRacing customer id |  |
| `PaceCarIdx` | Pace car's car index |  |
| `DriverIsAdmin` | 1 if you are session admin |  |
| `DriverHeadPosX` | Driver eye position in car, X | m |
| `DriverHeadPosY` | Driver eye position in car, Y | m |
| `DriverHeadPosZ` | Driver eye position in car, Z | m |
| `DriverCarIsElectric` | 1 if your car is electric |  |
| `DriverCarIdleRPM` | Idle RPM | revs/min |
| `DriverCarRedLine` | Redline RPM | revs/min |
| `DriverCarEngCylinderCount` | Engine cylinder count |  |
| `DriverCarFuelKgPerLtr` | Fuel density | kg/l |
| `DriverCarFuelMaxLtr` | Fuel tank capacity | l |
| `DriverCarMaxFuelPct` | Fraction of tank allowed (BoP) |  |
| `DriverCarGearNumForward` | Forward gears |  |
| `DriverCarGearNeutral` | Neutral gear number |  |
| `DriverCarGearReverse` | Reverse gears |  |
| `DriverGearboxType` | Gearbox type, e.g. Sequential |  |
| `DriverGearboxControlType` | Gearbox control type |  |
| `DriverCarShiftAid` | Shift aid setting |  |
| `DriverCarSLFirstRPM` | Shift light: first light RPM | revs/min |
| `DriverCarSLShiftRPM` | Shift light: shift-point RPM | revs/min |
| `DriverCarSLLastRPM` | Shift light: last light RPM | revs/min |
| `DriverCarSLBlinkRPM` | Shift light: blink RPM | revs/min |
| `DriverCarVersion` | Car asset version |  |
| `DriverPitTrkPct` | Your pit stall position as fraction of lap (same scale as CarIdxLapDistPct) | % |
| `DriverCarEstLapTime` | Sim's estimated lap time for your car here | s |
| `DriverSetupName` | Loaded setup file |  |
| `DriverSetupIsModified` | 1 if setup changed since load |  |
| `DriverSetupLoadTypeName` | Setup source, e.g. user |  |
| `DriverSetupPassedTech` | 1 if setup passed tech |  |
| `DriverIncidentCount` | Your incident points |  |
| `DriverBrakeCurvingFactor` | Unknown; brake pedal curve setting? |  |
| `DriverTires[].TireIndex` | Tyre compound index |  |
| `DriverTires[].TireCompoundType` | Tyre compound name, e.g. Hard |  |
| `Drivers[].CarIdx` | Car index; key into all CarIdx* telemetry arrays |  |
| `Drivers[].UserName` | Driver display name |  |
| `Drivers[].AbbrevName` | Abbreviated name |  |
| `Drivers[].Initials` | Initials |  |
| `Drivers[].UserID` | Driver customer id |  |
| `Drivers[].TeamID` | Team id, 0 if none |  |
| `Drivers[].TeamName` | Team name (driver name if no team) |  |
| `Drivers[].CarNumber` | Car number as string (may have leading zeros) |  |
| `Drivers[].CarNumberRaw` | Car number as integer |  |
| `Drivers[].CarPath` | Internal car name |  |
| `Drivers[].CarClassID` | Car class id |  |
| `Drivers[].CarID` | Car model id |  |
| `Drivers[].CarIsPaceCar` | 1 for the pace car |  |
| `Drivers[].CarIsAI` | 1 if AI driver |  |
| `Drivers[].CarIsElectric` | 1 if electric |  |
| `Drivers[].CarScreenName` | Car display name |  |
| `Drivers[].CarScreenNameShort` | Short car display name |  |
| `Drivers[].CarCfg` | Car config index, -1 if none |  |
| `Drivers[].CarCfgName` | Car config name |  |
| `Drivers[].CarCfgCustomPaintExt` | Custom paint suffix for config |  |
| `Drivers[].CarClassShortName` | Class short name, empty in single-class |  |
| `Drivers[].CarClassRelSpeed` | Relative speed of class (for ordering classes) |  |
| `Drivers[].CarClassLicenseLevel` | Licence level required for class |  |
| `Drivers[].CarClassMaxFuelPct` | Class fuel limit (BoP) | % |
| `Drivers[].CarClassWeightPenalty` | Class weight penalty (BoP) | kg |
| `Drivers[].CarClassPowerAdjust` | Class power adjustment (BoP) | % |
| `Drivers[].CarClassDryTireSetLimit` | Dry tyre sets allowed | % |
| `Drivers[].CarClassColor` | Class colour as integer RGB |  |
| `Drivers[].CarClassEstLapTime` | Sim's estimated lap time for the class here | s |
| `Drivers[].IRating` | iRating |  |
| `Drivers[].LicLevel` | Licence level |  |
| `Drivers[].LicSubLevel` | Licence sublevel (safety rating x100) |  |
| `Drivers[].LicString` | Licence for display, e.g. A 3.50 |  |
| `Drivers[].LicColor` | Licence colour |  |
| `Drivers[].IsSpectator` | 1 if spectating |  |
| `Drivers[].CarDesignStr` | Car paint pattern and colours |  |
| `Drivers[].HelmetDesignStr` | Helmet pattern and colours |  |
| `Drivers[].SuitDesignStr` | Suit pattern and colours |  |
| `Drivers[].BodyType` | Driver body model |  |
| `Drivers[].FaceType` | Driver face model |  |
| `Drivers[].HelmetType` | Helmet model |  |
| `Drivers[].CarNumberDesignStr` | Car number font and colours |  |
| `Drivers[].CarSponsor_1` | Sponsor decal id |  |
| `Drivers[].CarSponsor_2` | Sponsor decal id |  |
| `Drivers[].CurDriverIncidentCount` | Incident points of the current driver |  |
| `Drivers[].TeamIncidentCount` | Incident points of the team |  |

### SplitTimeInfo

| Variable | Description | Unit |
|---|---|---|
| `Sectors[].SectorNum` | Sector number |  |
| `Sectors[].SectorStartPct` | Sector start as fraction of lap | % |
