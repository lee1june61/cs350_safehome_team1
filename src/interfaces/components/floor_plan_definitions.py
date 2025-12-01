"""
Device definitions for the FloorPlan component.
"""

from typing import List

# Device positions from floorplan.png (coordinates as fraction 0-1)
# Derived from physical measurements on a 16.06cm × 9.87cm print
# Coordinates normalized using measured_x / 16.06, measured_y / 9.87
DEVICES = {
    # Window Sensors (red S markers)
    "S1": (0.042, 0.272, "sensor"),
    "S2": (0.139, 0.075, "sensor"),
    "S3": (0.044, 0.686, "sensor"),
    "S4": (0.798, 0.078, "sensor"),
    "S5": (0.951, 0.231, "sensor"),
    "S6": (0.950, 0.691, "sensor"),
    # Door Sensors (blue S markers)
    "S1_blue": (0.500, 0.068, "door_sensor"),
    "S2_blue": (0.162, 0.938, "door_sensor"),
    # Motion Sensors (green M markers)
    "M1": (0.108, 0.273, "motion"),
    "M2": (0.340, 0.500, "motion"),
    # Cameras (black C markers)
    "C1": (0.221, 0.185, "camera"),
    "C2": (0.438, 0.609, "camera"),
    "C3": (0.775, 0.827, "camera"),
}


def get_devices(dtype: str = None) -> List[str]:
    """Returns a list of device IDs, optionally filtered by type."""
    if dtype:
        return [d for d, (_, _, t) in DEVICES.items() if t == dtype]
    return list(DEVICES.keys())


def get_sensors() -> List[str]:
    """Returns a list of sensor device IDs (type 'sensor', 'motion', or 'door_sensor')."""
    return [
        d
        for d, (_, _, t) in DEVICES.items()
        if t in ("sensor", "motion", "door_sensor")
    ]
