"""Optional control panel feature mixin."""

from __future__ import annotations

from typing import Dict, Any


class ControlPanelOptionalFeatures:
    """Default no-op implementations for optional features."""

    def show_camera_view(self, camera_id: int, frame_data: bytes):
        """Display camera view if supported."""
        return None

    def update_sensor_status(self, sensor_id: int, is_triggered: bool):
        """Update individual sensor status indicator."""
        return None

    def clear_display(self):
        """Clear all messages from display."""
        return None

    def set_backlight(self, brightness: float):
        """Set display backlight brightness."""
        return None



