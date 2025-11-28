"""
Base class for DeviceCamera mixins.
"""
from __future__ import annotations

from typing import Optional

from ..interfaces import InterfaceCamera


class DeviceCameraBase(InterfaceCamera):
    """Shared DeviceCamera state."""

    PAN_MIN = -180
    PAN_MAX = 180
    TILT_MIN = -90
    TILT_MAX = 90
    ZOOM_MIN = 0
    ZOOM_MAX = 100

    def __init__(self, location: str, camera_id: int):
        self._location = location
        self._camera_id = camera_id
        self._pan = 0
        self._tilt = 0
        self._zoom = 0
        self._enabled = True
        self._last_capture_time = 0
        self._password: Optional[str] = None

    def get_location(self) -> str:
        return self._location

    def get_pan(self) -> int:
        return self._pan

    def get_tilt(self) -> int:
        return self._tilt

    def get_zoom(self) -> int:
        return self._zoom

    def get_camera_id(self) -> int:
        return self._camera_id

    # InterfaceCamera compatibility -------------------------------------------------
    def set_id(self, camera_id: int) -> None:
        """Update the underlying identifier (SDS alias)."""
        self._camera_id = camera_id

    def get_id(self) -> int:
        """Alias required by InterfaceCamera."""
        return self._camera_id

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self) -> bool:
        return self._enabled

    def set_password(self, password: str):
        self._password = password

    def clear_password(self):
        self._password = None

