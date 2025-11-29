"""Default configuration data for the SafeHome core system."""

from typing import Dict, List, Tuple

# Device data matching floorplan.png (C=Camera, S=Sensor, M=Motion)
SENSORS: List[Dict] = [
    {"id": "S1", "type": "WINDOW", "location": "DR Top", "armed": False},
    {"id": "S2", "type": "DOOR", "location": "DR Left", "armed": False},
    {"id": "S3", "type": "WINDOW", "location": "KIT Left", "armed": False},
    {"id": "S4", "type": "WINDOW", "location": "LR Top", "armed": False},
    {"id": "S5", "type": "DOOR", "location": "LR Right Top", "armed": False},
    {"id": "S6", "type": "WINDOW", "location": "LR Right Bottom", "armed": False},
    {"id": "M1", "type": "MOTION", "location": "DR", "armed": False},
    {"id": "M2", "type": "MOTION", "location": "Hallway", "armed": False},
]

SAFETY_ZONES: List[Dict] = [
    {"id": 1, "name": "Front Zone", "sensors": ["S1", "S2", "M1"], "armed": False},
    {"id": 2, "name": "Kitchen Zone", "sensors": ["S3"], "armed": False},
    {
        "id": 3,
        "name": "Living Room",
        "sensors": ["S4", "S5", "S6", "M2"],
        "armed": False,
    },
]

# Default mode configurations (which sensors are active in each mode)
MODE_CONFIGS: Dict[str, List[str]] = {
    "HOME": ["S1", "S2", "S5", "S6"],  # Perimeter only
    "AWAY": ["S1", "S2", "S3", "S4", "S5", "S6", "M1", "M2"],  # All sensors
    "OVERNIGHT": ["S1", "S2", "S3", "S4", "S5", "S6"],  # All except motion
    "EXTENDED": ["S1", "S2", "S3", "S4", "S5", "S6", "M1", "M2"],  # All sensors
    "GUEST": ["S1", "S2", "S5", "S6"],  # Same as HOME
}

CAMERAS: List[Dict] = [
    {"id": "C1", "location": "Front Entry", "x": 220, "y": 185},
    {"id": "C2", "location": "Living Room", "x": 438, "y": 609},
    {"id": "C3", "location": "Back Patio", "x": 775, "y": 827},
]

SENSOR_COORDS: Dict[str, Tuple[int, int]] = {
    "S1": (35, 90),
    "S2": (115, 36),
    "S3": (35, 255),
    "S4": (450, 42),
    "S5": (582, 140),
    "S6": (582, 275),
    "M1": (70, 140),
    "M2": (285, 190),
}

__all__ = [
    "SENSORS",
    "SAFETY_ZONES",
    "MODE_CONFIGS",
    "CAMERAS",
    "SENSOR_COORDS",
]


