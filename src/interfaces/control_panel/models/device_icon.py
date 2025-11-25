"""Device icon data model."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DeviceIcon:
    """Device icon representation on floor plan.

    Following the DeviceIcon class design from SDS document.
    """

    device_id: int
    device_type: str  # "window_door", "motion", "camera"
    x: int
    y: int
    name: str = ""
    is_armed: bool = False
    is_enabled: bool = True
    is_hovered: bool = False
    is_selected: bool = False
    canvas_id: Optional[int] = None
    label_id: Optional[int] = None

    def contains_point(self, x: int, y: int, icon_size: int = 30) -> bool:
        """Check if point is inside icon bounds.

        Args:
            x: X coordinate to check
            y: Y coordinate to check
            icon_size: Size of the icon for boundary checking

        Returns:
            True if point is within icon bounds
        """
        return (
            self.x - icon_size <= x <= self.x + icon_size
            and self.y - icon_size <= y <= self.y + icon_size
        )

    @property
    def is_sensor(self) -> bool:
        """Check if device is a sensor (window_door or motion)."""
        return self.device_type in ["window_door", "motion"]

    @property
    def is_camera(self) -> bool:
        """Check if device is a camera."""
        return self.device_type == "camera"
