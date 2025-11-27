"""
CameraController registry-related responsibilities.
"""
from __future__ import annotations

from typing import List, Optional

from ..devices.cameras.safehome_camera import SafeHomeCamera
from ..utils.exceptions import CameraNotFoundError
from .camera_controller_base import CameraControllerBase


class CameraControllerRegistryMixin(CameraControllerBase):
    """Create, delete, and fetch cameras."""

    def add_camera(self, x_coord: int, y_coord: int) -> Optional[int]:
        with self._lock:
            if not self._is_valid_location(x_coord, y_coord):
                return None
            camera_id = self.next_camera_id
            camera = SafeHomeCamera(camera_id, x_coord, y_coord)
            camera.validate()
            self._register_camera(camera)
            self.next_camera_id += 1
            return camera_id

    def delete_camera(self, camera_id: int) -> bool:
        with self._lock:
            camera = self._remove_camera(camera_id)
            if camera is None:
                return False
            if hasattr(camera, "cleanup"):
                camera.cleanup()
            return True

    def get_camera_by_id(self, camera_id: int) -> SafeHomeCamera:
        with self._lock:
            if camera_id not in self._cameras:
                raise CameraNotFoundError(f"Camera with ID {camera_id} not found")
            return self._cameras[camera_id]

    def get_all_cameras(self) -> List[SafeHomeCamera]:
        with self._lock:
            return list(self.camera_list)

    def get_total_camera_number(self) -> int:
        with self._lock:
            return self.total_camera_number

