"""
Lifecycle helpers for SafeHomeCamera.
"""
from __future__ import annotations

from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraLifecycleMixin(SafeHomeCameraBase):
    """Enable/disable, getters, and cleanup routines."""

    def enable(self) -> bool:
        with self._lock:
            self.enabled = True
            return True

    def disable(self) -> bool:
        with self._lock:
            self.enabled = False
            return True

    def is_enabled(self) -> bool:
        with self._lock:
            return self.enabled

    def get_id(self) -> int:
        with self._lock:
            return self.camera_id

    def get_pan_angle(self) -> int:
        with self._lock:
            return self.pan_angle

    def get_zoom_level(self) -> int:
        with self._lock:
            return self.zoom_level

    def get_zoom_setting(self) -> int:
        return self.get_zoom_level()

    def cleanup(self) -> None:
        with self._lock:
            if self._device:
                self._device.stop()

    def __del__(self) -> None:
        try:
            self.cleanup()
        except Exception:
            pass

    def __repr__(self) -> str:
        with self._lock:
            return (
                f"SafeHomeCamera(id={self.camera_id}, "
                f"location={self.location}, "
                f"enabled={self.enabled}, "
                f"pan={self.pan_angle}, "
                f"zoom={self.zoom_level})"
            )

