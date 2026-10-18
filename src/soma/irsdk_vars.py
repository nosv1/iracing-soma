# Key names for irsdk lookups. See docs/irsdk/irsdk_vars.md.

# --- Telemetry variables (per tick) ---

# Laps completed by car index
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
# Percent of available time fg thread took with a 1 sec avg (%)
CPU_USAGE_FG = "CpuUsageFG"
# Average frames per second (fps)
FRAME_RATE = "FrameRate"
# Percent of available time gpu took with a 1 sec avg (%)
GPU_USAGE = "GpuUsage"
# 1=Car on track physics running with player in car
IS_ON_TRACK = "IsOnTrack"
# Players carIdx
PLAYER_CAR_IDX = "PlayerCarIdx"
# Current update number
SESSION_TICK = "SessionTick"
# Seconds since session start (s)
SESSION_TIME = "SessionTime"
# Session number
SESSION_NUM = "SessionNum"
# GPS vehicle speed (m/s)
SPEED = "Speed"

# --- Session info (YAML) ---

# Section: driver/car metadata, incl. the Drivers list
DRIVER_INFO = "DriverInfo"
# DriverInfo.Drivers: one entry per car in the session
DRIVERS = "Drivers"
# DriverInfo.Drivers[].CarIdx: car index; key into all CarIdx* telemetry arrays
CAR_IDX = "CarIdx"
# Driver display name
USER_NAME = "UserName"
