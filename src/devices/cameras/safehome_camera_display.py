"""
Display helpers for SafeHomeCamera.
"""
from __future__ import annotations

from ...utils.exceptions import CameraDisabledError
from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraDisplayMixin(SafeHomeCameraBase):
    """Expose display_view logic."""

    def display_view(self):
        with self._lock:
            if not self.enabled:
                raise CameraDisabledError(
                    f"Camera {self.camera_id} is disabled. Enable it first."
                )
            return self._device.get_view()

