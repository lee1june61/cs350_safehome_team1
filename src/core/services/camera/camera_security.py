"""Camera password and thumbnail helpers."""

from __future__ import annotations

from typing import Dict

from src.controllers.camera_controller import CameraController
from src.devices.cameras.safehome_camera import SafeHomeCamera


class CameraSecurityService:
    """Manages passwords and thumbnail views."""

    def __init__(self, controller: CameraController):
        self._controller = controller

    def set_password(
        self, camera: SafeHomeCamera, cam_id: int, old_password: str, new_password: str
    ):
        if camera.has_password() and not camera.verify_password(old_password):
            return {"success": False, "message": "Old password incorrect"}
        if self._controller.set_camera_password(cam_id, new_password):
            return {"success": True}
        return {"success": False, "message": "Unable to set password"}

    def delete_password(self, camera: SafeHomeCamera, cam_id: int, old_password: str):
        if camera.has_password() and not camera.verify_password(old_password):
            return {"success": False, "message": "Password incorrect"}
        if self._controller.delete_camera_password(cam_id):
            return {"success": True}
        return {"success": False, "message": "Unable to delete password"}

    def verify_password(self, cam_id: int, password: str, camera: SafeHomeCamera):
        is_valid = self._controller.validate_camera_password(cam_id, password)
        if not is_valid:
            return {"success": False, "message": "Wrong password"}
        has_password = camera.has_password() if camera else False
        return {"success": True, "has_password": has_password}

    def thumbnails(self) -> Dict[str, any]:
        thumbnails = {}
        for cam_id, view in self._controller.display_thumbnail_view():
            thumbnails[f"C{cam_id}"] = view
        return {"success": True, "data": thumbnails}


