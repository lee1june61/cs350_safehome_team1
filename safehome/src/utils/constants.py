"""
SafeHome system constants and enumerations.
"""

# System Settings
DEFAULT_ALARM_DELAY = 30  # seconds
DEFAULT_SYSTEM_LOCK_TIME = 300  # 5 minutes
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 20
MAX_LOGIN_ATTEMPTS = 3

# Camera Settings
DEFAULT_CAMERA_FPS = 1  # frame per second
MAX_RECORDING_DURATION = 3600  # 1 hour
THUMBNAIL_SIZE = (320, 240)

# Sensor Settings
SENSOR_POLL_INTERVAL = 1.0  # seconds
BATTERY_LOW_THRESHOLD = 20  # percent

# Database
DB_NAME = "safehome.db"
LOG_RETENTION_DAYS = 90

# Network
MONITORING_SERVICE_PHONE = "911"
DEFAULT_WEB_PORT = 8080
