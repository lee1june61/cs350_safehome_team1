"""Layout configuration for device positions."""


class DevicePositions:
    """Device positions on floor plan - exact coordinates from image."""

    # Window/Door Sensors (red squares)
    WINDOW_DOOR_SENSORS = [
        (1, "S₁ (Window)", 60, 50, False),
        (2, "S₂", 150, 380, False),
        (3, "S₃ (KIT Window)", 50, 250, True),
        (4, "S₄ (DR Window)", 560, 40, False),
        (5, "S₅ (LR Window)", 600, 135, True),
        (6, "S₆ (LR Corner)", 600, 280, False),
        (7, "S'₂ (KIT Door)", 200, 300, False),
    ]

    # Motion Sensors (blue squares with M)
    MOTION_SENSORS = [
        (11, "M₁ (DR)", 60, 100, True),
        (12, "M₂ (KIT)", 200, 190, False),
    ]

    # Cameras (green circles with C)
    CAMERAS = [
        (21, "C₁ (Entry)", 325, 110, True),
        (22, "C₂ (Stairs)", 325, 230, True),
        (23, "C₃ (LR)", 520, 240, True),
    ]
