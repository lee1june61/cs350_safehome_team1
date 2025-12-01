"""Default configuration data for the SafeHome core system."""

from typing import Dict, List, Tuple

# Device data matching floorplan.png (C=Camera, S=Sensor, M=Motion)
SENSORS: List[Dict] = [
    {"id": "S1", "type": "WINDOW", "location": "DR Top Window", "armed": False},
    {"id": "S2", "type": "WINDOW", "location": "DR Left Window", "armed": False},
    {"id": "S3", "type": "WINDOW", "location": "KIT Left Window", "armed": False},
    {"id": "S4", "type": "WINDOW", "location": "LR Top Window", "armed": False},
    {"id": "S5", "type": "WINDOW", "location": "LR Right Top Window", "armed": False},
    {"id": "S6", "type": "WINDOW", "location": "LR Right Bottom Window", "armed": False},
    {"id": "S1_blue", "type": "DOOR", "location": "Front Door", "armed": False},
    {"id": "S2_blue", "type": "DOOR", "location": "Patio Door", "armed": False},
    {"id": "M1", "type": "MOTION", "location": "DR", "armed": False},
    {"id": "M2", "type": "MOTION", "location": "Hallway", "armed": False},
]

SAFETY_ZONES: List[Dict] = [
    {
        "id": 1,
        "name": "Front Zone",
        "sensors": ["S1", "S2", "S1_blue", "M1"],
        "armed": False,
    },
    {
        "id": 2,
        "name": "Kitchen Zone",
        "sensors": ["S3", "S2_blue"],
        "armed": False,
    },
    {
        "id": 3,
        "name": "Living Room",
        "sensors": ["S4", "S5", "S6", "M2"],
        "armed": False,
    },
]

# Default mode configurations (which sensors are active in each mode)
MODE_CONFIGS: Dict[str, List[str]] = {
    "HOME": ["S1", "S2", "S5", "S6", "S1_blue", "S2_blue"],  # Perimeter only
    "AWAY": [
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
        "S1_blue",
        "S2_blue",
        "M1",
        "M2",
    ],  # All sensors
    "OVERNIGHT": ["S1", "S2", "S3", "S4", "S5", "S6", "S1_blue", "S2_blue"],  # All except motion
    "EXTENDED": [
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
        "S1_blue",
        "S2_blue",
        "M1",
        "M2",
    ],  # All sensors
    "GUEST": ["S1", "S2", "S5", "S6", "S1_blue", "S2_blue"],  # Same as HOME
}

CAMERAS: List[Dict] = [
    {"id": "C1", "location": "Front Entry", "x": 220, "y": 185},
    {"id": "C2", "location": "Living Room", "x": 438, "y": 609},
    {"id": "C3", "location": "Back Patio", "x": 775, "y": 827},
]

SENSOR_COORDS: Dict[str, Tuple[int, int]] = {
    "S1": (26, 101),
    "S2": (84, 28),
    "S3": (27, 256),
    "S4": (485, 29),
    "S5": (578, 86),
    "S6": (577, 258),
    "S1_blue": (304, 25),
    "S2_blue": (98, 350),
    "M1": (66, 102),
    "M2": (206, 186),
}

__all__ = [
    "SENSORS",
    "SAFETY_ZONES",
    "MODE_CONFIGS",
    "CAMERAS",
    "SENSOR_COORDS",
]


