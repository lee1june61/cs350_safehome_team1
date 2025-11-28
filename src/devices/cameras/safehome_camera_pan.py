"""
Pan helpers for SafeHomeCamera.
"""
from __future__ import annotations

from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraPanMixin(SafeHomeCameraBase):
    """Pan left/right logic."""

    def pan_left(self) -> bool:
        with self._lock:
            if not self.enabled or self.pan_angle <= self.MIN_PAN:
                return False
            if self._device.pan_left():
                self.pan_angle -= 1
                return True
            return False

    def pan_right(self) -> bool:
        with self._lock:
            if not self.enabled or self.pan_angle >= self.MAX_PAN:
                return False
            if self._device.pan_right():
                self.pan_angle += 1
                return True
            return False

