"""
Password management responsibilities for CameraController.
"""

from __future__ import annotations

from .camera_controller_base import CameraControllerBase


class CameraControllerSecurityMixin(CameraControllerBase):
    """Set, clear, and validate camera passwords."""

    def set_camera_password(self, camera_id: int, password: str) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return False
            return bool(camera.set_password(password))

    def delete_camera_password(self, camera_id: int) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None or not camera.has_password():
                return False
            if hasattr(camera, "delete_password"):
                return bool(camera.delete_password())
            return bool(camera.clear_password())

    def validate_camera_password(self, camera_id: int, password: str) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return False
            if not camera.has_password():
                return True
            return camera.get_password() == password
