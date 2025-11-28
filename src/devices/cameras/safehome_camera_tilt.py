"""
Tilt helpers for SafeHomeCamera.
"""
from __future__ import annotations

from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraTiltMixin(SafeHomeCameraBase):
    """Tilt up/down logic."""

    MIN_TILT = -5
    MAX_TILT = 5

    def tilt_up(self) -> bool:
        with self._lock:
            if not self.enabled or self.tilt_angle >= self.MAX_TILT:
                return False
            if hasattr(self._device, 'set_tilt'):
                new_tilt = self.tilt_angle + 1
                if self._device.set_tilt(new_tilt):
                    self.tilt_angle = new_tilt
                    return True
            else:
                # Fallback: manage tilt directly if device doesn't support it
                self.tilt_angle += 1
                return True
            return False

    def tilt_down(self) -> bool:
        with self._lock:
            if not self.enabled or self.tilt_angle <= self.MIN_TILT:
                return False
            if hasattr(self._device, 'set_tilt'):
                new_tilt = self.tilt_angle - 1
                if self._device.set_tilt(new_tilt):
                    self.tilt_angle = new_tilt
                    return True
            else:
                # Fallback: manage tilt directly if device doesn't support it
                self.tilt_angle -= 1
                return True
            return False

