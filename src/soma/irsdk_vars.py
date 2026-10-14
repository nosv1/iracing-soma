# Key names for irsdk lookups. See docs/irsdk/irsdk_vars.md.

# --- Telemetry variables (per tick) ---

# Cars position in race by car index
CAR_IDX_POSITION = "CarIdxPosition"
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
