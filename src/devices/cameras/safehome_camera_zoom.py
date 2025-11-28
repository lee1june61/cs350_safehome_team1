"""
Zoom helpers for SafeHomeCamera.
"""
from __future__ import annotations

from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraZoomMixin(SafeHomeCameraBase):
    """Zoom in/out logic."""

    def zoom_in(self) -> bool:
        with self._lock:
            if not self.enabled or self.zoom_level >= self.MAX_ZOOM:
                return False
            if self._device.zoom_in():
                self.zoom_level += 1
                return True
            return False

    def zoom_out(self) -> bool:
        with self._lock:
            if not self.enabled or self.zoom_level <= self.MIN_ZOOM:
                return False
            if self._device.zoom_out():
                self.zoom_level -= 1
                return True
            return False

