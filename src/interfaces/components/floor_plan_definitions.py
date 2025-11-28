"""
Device definitions for the FloorPlan component.
"""

# Device positions from floorplan.png analysis (image ~605x305)
# Coordinates are normalized (0.0 to 1.0)
# (device_id, (x, y, type))
DEVICES = {
    # Cameras (gray triangles with C labels)
    'C1': (0.28, 0.23, 'camera'),   # DR room - inside triangle
    'C2': (0.52, 0.49, 'camera'),   # Center/hallway - near stairs
    'C3': (0.77, 0.69, 'camera'),   # LR room - inside triangle
    # Window/Door Sensors (red dots with S labels)
    'S1': (0.10, 0.05, 'sensor'),   # Top-left corner, above DR
    'S2': (0.07, 0.92, 'sensor'),   # Bottom-left, below KIT
    'S3': (0.07, 0.48, 'sensor'),   # Left side, KIT area
    'S4': (0.84, 0.05, 'sensor'),   # Top-right, above LR
    'S5': (0.97, 0.31, 'sensor'),   # Right side upper
    'S6': (0.97, 0.66, 'sensor'),   # Right side lower
    # Motion Sensors (blue/black dots with M labels)
    'M1': (0.04, 0.20, 'motion'),   # Left side, DR area
    'M2': (0.44, 0.44, 'motion'),   # Center hallway
}


def get_devices(dtype: str = None) -> List[str]:
    """Returns a list of device IDs, optionally filtered by type."""
    if dtype:
        return [d for d, (_, _, t) in DEVICES.items() if t == dtype]
    return list(DEVICES.keys())

def get_sensors() -> List[str]:
    """Returns a list of sensor device IDs (type 'sensor' or 'motion')."""
    return [d for d, (_, _, t) in DEVICES.items() if t in ('sensor', 'motion')]
