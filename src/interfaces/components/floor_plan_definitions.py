"""
Device definitions for the FloorPlan component.
"""

from typing import List

# Device positions from floorplan.png analysis (image 607x373)
# Coordinates are normalized (0.0 to 1.0)
# Calculated from pixel coordinates: (pixel_x / 607, pixel_y / 373)
# (device_id, (x, y, type))
DEVICES = {
    # Cameras (gray triangles with C labels)
    "C1": (0.334, 0.316, "camera"),  # (203, 118)
    "C2": (0.507, 0.568, "camera"),  # (308, 212)
    "C3": (0.750, 0.799, "camera"),  # (455, 298)
    # Window Sensors (red rectangles)
    "S1": (0.058, 0.241, "sensor"),      # (35, 90)
    "S3": (0.058, 0.684, "sensor"),      # (35, 255)
    "S4": (0.741, 0.113, "sensor"),      # (450, 42)
    "S6": (0.959, 0.737, "sensor"),      # (582, 275)
    # Door Sensors (teal dots)
    "S2": (0.486, 0.121, "door_sensor"), # (295, 45)
    "S5": (0.222, 0.925, "door_sensor"), # (135, 345)
    # Motion Sensors (blue dots with M labels)
    "M1": (0.115, 0.375, "motion"),  # (70, 140)
    "M2": (0.470, 0.509, "motion"),  # (285, 190)
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
