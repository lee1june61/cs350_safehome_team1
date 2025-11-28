"""Floor plan device positions and constants."""

# Device positions from floorplan.png (coordinates as fraction 0-1)
DEVICES = {
    # Cameras (gray triangles with C labels)
    'C1': (0.28, 0.23, 'camera'),
    'C2': (0.52, 0.49, 'camera'),
    'C3': (0.77, 0.69, 'camera'),
    # Window/Door Sensors (red dots with S labels)
    'S1': (0.10, 0.05, 'sensor'),
    'S2': (0.07, 0.92, 'sensor'),
    'S3': (0.07, 0.48, 'sensor'),
    'S4': (0.84, 0.05, 'sensor'),
    'S5': (0.97, 0.31, 'sensor'),
    'S6': (0.97, 0.66, 'sensor'),
    # Motion Sensors (blue/black dots with M labels)
    'M1': (0.04, 0.20, 'motion'),
    'M2': (0.44, 0.44, 'motion'),
}

DEVICE_COLORS = {
    'camera': '#9b59b6',  # Purple
    'sensor': '#e74c3c',  # Red
    'motion': '#3498db',  # Blue
}

