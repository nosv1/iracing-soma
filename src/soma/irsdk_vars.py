# Key names for irsdk lookups. See docs/irsdk/irsdk_vars.md.

# --- Telemetry variables (per tick) ---

# 0=brake released to 1=max pedal force (0-1 fraction, despite the % unit)
BRAKE = "Brake"
# True if abs is currently reducing brake force pressure
BRAKE_ABS_ACTIVE = "BrakeABSactive"
# Raw brake input 0=brake released to 1=max pedal force (0-1 fraction)
BRAKE_RAW = "BrakeRaw"
# Laps completed by car index; per session (resets each session), -1 until the car
# first crosses the line (a rolling start goes -1 -> 0 at the green, with a pct wrap)
CAR_IDX_LAP_COMPLETED = "CarIdxLapCompleted"
# Cars last lap time (s); -1 if no timed lap yet
CAR_IDX_LAST_LAP_TIME = "CarIdxLastLapTime"
# Percentage distance around lap by car index (0-1 fraction, despite the % unit)
CAR_IDX_LAP_DIST_PCT = "CarIdxLapDistPct"
# On pit road between the cones by car index
CAR_IDX_ON_PIT_ROAD = "CarIdxOnPitRoad"
# Cars position in race by car index
CAR_IDX_POSITION = "CarIdxPosition"
# Track surface type by car index (irsdk.TrkLoc: -1 not in world .. 3 on track)
CAR_IDX_TRACK_SURFACE = "CarIdxTrackSurface"
# Temperature of air at start/finish line (C)
AIR_TEMP = "AirTemp"
# Notify if car is to the left or right of driver (irsdk.CarLeftRight)
CAR_LEFT_RIGHT = "CarLeftRight"
# Percent of available time fg thread took with a 1 sec avg (%)
CPU_USAGE_FG = "CpuUsageFG"
# Bitfield for warning lights (irsdk.EngineWarnings): 0x0001 water temp,
# 0x0004 oil pressure, 0x0080 / 0x0100 mandatory / optional repairs needed
ENGINE_WARNINGS = "EngineWarnings"
# How many fast repairs left; 255 is unlimited
FAST_REPAIR_AVAILABLE = "FastRepairAvailable"
# How many fast repairs used so far
FAST_REPAIR_USED = "FastRepairUsed"
# Liters of fuel remaining (l)
FUEL_LEVEL = "FuelLevel"
# Average frames per second (fps)
FRAME_RATE = "FrameRate"
# Percent of available time gpu took with a 1 sec avg (%)
GPU_USAGE = "GpuUsage"
# 1=Car on track physics running with player in car
IS_ON_TRACK = "IsOnTrack"
# Players best lap time (s)
LAP_BEST_LAP_TIME = "LapBestLapTime"
# Estimate of players current lap time as shown in F3 box (s)
LAP_CURRENT_LAP_TIME = "LapCurrentLapTime"
# Delta time for best lap (s)
LAP_DELTA_TO_BEST_LAP = "LapDeltaToBestLap"
# Delta time for best lap is valid
LAP_DELTA_TO_BEST_LAP_OK = "LapDeltaToBestLap_OK"
# Delta time for optimal lap (s)
LAP_DELTA_TO_OPTIMAL_LAP = "LapDeltaToOptimalLap"
# Delta time for optimal lap is valid
LAP_DELTA_TO_OPTIMAL_LAP_OK = "LapDeltaToOptimalLap_OK"
# Delta time for session best lap (s)
LAP_DELTA_TO_SESSION_BEST_LAP = "LapDeltaToSessionBestLap"
# Delta time for session best lap is valid
LAP_DELTA_TO_SESSION_BEST_LAP_OK = "LapDeltaToSessionBestLap_OK"
# Delta time for session last lap (s); "Lastl" is iRacing's spelling
LAP_DELTA_TO_SESSION_LAST_LAP = "LapDeltaToSessionLastlLap"
# Delta time for session last lap is valid
LAP_DELTA_TO_SESSION_LAST_LAP_OK = "LapDeltaToSessionLastlLap_OK"
# Players last lap time (s)
LAP_LAST_LAP_TIME = "LapLastLapTime"
# LF tire middle percent tread remaining (0-1 fraction, despite the % unit; 1.0 = fresh)
LF_WEAR_M = "LFwearM"
# Longitudinal acceleration, including gravity (m/s^2)
LONG_ACCEL = "LongAccel"
# Engine oil pressure (bar)
OIL_PRESS = "OilPress"
# Time left for optional repairs if repairs are active (s)
PIT_OPT_REPAIR_LEFT = "PitOptRepairLeft"
# Time left for mandatory pit repairs if repairs are active (s). Stayed 0 on track and
# on pit road with damage (10-20); use ENGINE_WARNINGS 0x0080 to detect damage
PIT_REPAIR_LEFT = "PitRepairLeft"
# Players class position in race
PLAYER_CAR_CLASS_POSITION = "PlayerCarClassPosition"
# Players carIdx
PLAYER_CAR_IDX = "PlayerCarIdx"
# Players own incident count for this session
PLAYER_CAR_MY_INCIDENT_COUNT = "PlayerCarMyIncidentCount"
# Players position in race
PLAYER_CAR_POSITION = "PlayerCarPosition"
# Session flags (irsdk.Flags)
SESSION_FLAGS = "SessionFlags"
# New improved laps left till session ends; 32767 seen in a timed practice
SESSION_LAPS_REMAIN_EX = "SessionLapsRemainEx"
# Session number
SESSION_NUM = "SessionNum"
# Session state (irsdk.SessionState)
SESSION_STATE = "SessionState"
# Current update number
SESSION_TICK = "SessionTick"
# Seconds since session start (s)
SESSION_TIME = "SessionTime"
# Seconds left till session ends (s)
SESSION_TIME_REMAIN = "SessionTimeRemain"
# GPS vehicle speed (m/s)
SPEED = "Speed"
# 0=off throttle to 1=full throttle (0-1 fraction, despite the % unit)
THROTTLE = "Throttle"
# Temperature of track measured by crew around track (C)
TRACK_TEMP_CREW = "TrackTempCrew"
# Engine coolant temp (C)
WATER_TEMP = "WaterTemp"

# --- Session info (YAML) ---

# Section: driver/car metadata, incl. the Drivers list
DRIVER_INFO = "DriverInfo"
# DriverInfo.Drivers: one entry per car in the session
DRIVERS = "Drivers"
# DriverInfo.Drivers[].CarIdx: car index; key into all CarIdx* telemetry arrays
CAR_IDX = "CarIdx"
# Driver display name
USER_NAME = "UserName"

# Section: event/server metadata
WEEKEND_INFO = "WeekendInfo"
# WeekendInfo.SessionID: session id, 0 offline; changed on practice -> race server
SESSION_ID = "SessionID"
# WeekendInfo.SubSessionID: the results id online, 0 offline; changed on server switch
SUB_SESSION_ID = "SubSessionID"
# WeekendInfo.EventType: kind of event the server runs (Practice, Race, ...), not the
# current session: the race server says Race during its own practice
EVENT_TYPE = "EventType"

# Section: the event's session lineup
SESSION_INFO = "SessionInfo"
# SessionInfo.CurrentSessionNum: index into Sessions, same as telemetry SessionNum.
# YAML can lag telemetry (54 ticks on the 10-19 server switch): index with SESSION_NUM
CURRENT_SESSION_NUM = "CurrentSessionNum"
# SessionInfo.Sessions: one entry per session; index with telemetry SessionNum
SESSIONS = "Sessions"
# SessionInfo.Sessions[].SessionType: Practice, Lone Qualify, Race, ...
SESSION_TYPE = "SessionType"
# SessionInfo.Sessions[].SessionName: display name, e.g. PRACTICE, QUALIFY, RACE
SESSION_NAME = "SessionName"
# Sessions[].SessionNum shares its key with telemetry SESSION_NUM above
