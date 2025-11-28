"""Floor plan device positions and constants."""

# Device positions from floorplan.png (coordinates as fraction 0-1)
# Calculated from physical measurements on 16.06cm × 9.87cm image
# Coordinates normalized using measured_x / 16.06, measured_y / 9.87
DEVICES = {
    # ---------------------------------------------------------
    # Window Sensors (빨간색 S - 실측 좌표)
    # ---------------------------------------------------------
    # 1: 0.68cm(x) / 2.68cm(y)
    "S1": (0.042, 0.272, "sensor"),
    # 2: 2.23cm(x) / 0.74cm(y)
    "S2": (0.139, 0.075, "sensor"),
    # 3: 0.71cm(x) / 6.77cm(y)
    "S3": (0.044, 0.686, "sensor"),
    # 4: 12.81cm(x) / 0.77cm(y)
    "S4": (0.798, 0.078, "sensor"),
    # 5: 15.28cm(x) / 2.28cm(y)
    "S5": (0.951, 0.231, "sensor"),
    # 6: 15.26cm(x) / 6.82cm(y)
    "S6": (0.950, 0.691, "sensor"),
    # ---------------------------------------------------------
    # Door Sensors (파란색 S - 실측 좌표)
    # ---------------------------------------------------------
    # 1: 8.03cm(x) / 0.67cm(y)
    "S1_blue": (0.500, 0.068, "door_sensor"),
    # 2: 2.6cm(x) / 9.26cm(y)
    "S2_blue": (0.162, 0.938, "door_sensor"),
    # ---------------------------------------------------------
    # Motion Sensors (초록색 M - 실측 좌표)
    # ---------------------------------------------------------
    # 1: 1.73cm(x) / 2.69cm(y)
    "M1": (0.108, 0.273, "motion"),
    # 2: 5.46cm(x) / 4.93cm(y)
    "M2": (0.340, 0.500, "motion"),
    # ---------------------------------------------------------
    # Cameras (검은색 C - 실측 좌표)
    # ---------------------------------------------------------
    # 1: 3.55cm(x) / 1.83cm(y)
    "C1": (0.221, 0.185, "camera"),
    # 2: 7.03cm(x) / 6.01cm(y)
    "C2": (0.438, 0.609, "camera"),
    # 3: 12.44cm(x) / 8.16cm(y)
    "C3": (0.775, 0.827, "camera"),
}

DEVICE_COLORS = {
    "camera": "#9b59b6",  # Purple
    "sensor": "#e74c3c",  # Red (Window Sensor)
    "motion": "#3498db",  # Blue (Motion Sensor)
    "door_sensor": "#3498db",  # Blue (Door Sensor)
}
