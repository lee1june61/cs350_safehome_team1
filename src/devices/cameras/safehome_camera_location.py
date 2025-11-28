"""
Location/identity helpers for SafeHomeCamera.
"""
from __future__ import annotations

from typing import List

from ...utils.exceptions import CameraValidationError
from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraLocationMixin(SafeHomeCameraBase):
    """Manage coordinates and identifiers."""

    def set_location(self, new_location: List[int]) -> None:
        with self._lock:
            if not isinstance(new_location, list) or len(new_location) != 2:
                raise CameraValidationError(
                    "Location must be a list of [x, y] coordinates"
                )
            self.location = new_location.copy()

    def set_id(self, new_id: int) -> bool:
        with self._lock:
            if new_id <= 0:
                raise CameraValidationError("Camera ID must be positive")
            self.camera_id = new_id
            self._initialize_device(new_id)
            return True

    def get_location(self) -> List[int]:
        with self._lock:
            return self.location.copy()

