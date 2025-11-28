"""
PTZ helpers for DeviceCamera.
"""
from __future__ import annotations

from .device_camera_base import DeviceCameraBase


class DeviceCameraPTZMixin(DeviceCameraBase):
    """Pan/Tilt/Zoom setters with bounds checking."""

    def set_pan(self, angle: int) -> bool:
        if not self._enabled:
            return False
        if self.PAN_MIN <= angle <= self.PAN_MAX:
            self._pan = angle
            return True
        return False

    def set_tilt(self, angle: int) -> bool:
        if not self._enabled:
            return False
        if self.TILT_MIN <= angle <= self.TILT_MAX:
            self._tilt = angle
            return True
        return False

    def set_zoom(self, level: int) -> bool:
        if not self._enabled:
            return False
        if self.ZOOM_MIN <= level <= self.ZOOM_MAX:
            self._zoom = level
            return True
        return False

    # InterfaceCamera operations ----------------------------------------------------
    def pan_left(self) -> bool:
        return self.set_pan(self._pan - 1)

    def pan_right(self) -> bool:
        return self.set_pan(self._pan + 1)

    def zoom_in(self) -> bool:
        return self.set_zoom(self._zoom + 1)

    def zoom_out(self) -> bool:
        return self.set_zoom(self._zoom - 1)

