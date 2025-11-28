"""
Validation helpers for SafeHomeCamera.
"""
from __future__ import annotations

from ...utils.exceptions import CameraValidationError
from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraValidationMixin(SafeHomeCameraBase):
    """State validation logic."""

    def validate(self) -> bool:
        with self._lock:
            if self.camera_id <= 0:
                raise CameraValidationError("Camera ID must be positive")

            if not isinstance(self.location, list) or len(self.location) != 2:
                raise CameraValidationError("Location must be a list of [x, y]")

            if not (self.MIN_PAN <= self.pan_angle <= self.MAX_PAN):
                raise CameraValidationError(
                    f"Pan angle must be between {self.MIN_PAN} and {self.MAX_PAN}"
                )

            if not (self.MIN_ZOOM <= self.zoom_level <= self.MAX_ZOOM):
                raise CameraValidationError(
                    f"Zoom level must be between {self.MIN_ZOOM} and {self.MAX_ZOOM}"
                )

            return True

    def save_info(self) -> bool:
        with self._lock:
            self.validate()
            return True

