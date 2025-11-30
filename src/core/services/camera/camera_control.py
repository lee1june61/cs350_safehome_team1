"""Camera control utilities (pan/zoom/tilt, enable/disable)."""

from __future__ import annotations

from typing import Optional

from src.controllers.camera_controller import CameraController
from src.devices.cameras.safehome_camera import SafeHomeCamera


class CameraControlService:
    """Wraps PTZ and enable/disable operations."""

    def __init__(self, controller: CameraController):
        self._controller = controller

    def pan(self, camera_id: int, direction: str):
        control = (
            CameraController.CONTROL_PAN_RIGHT
            if direction.upper() == "R"
            else CameraController.CONTROL_PAN_LEFT
        )
        success = self._controller.control_single_camera(camera_id, control)
        if success:
            cam = self._get_camera(camera_id)
            return {"success": True, "pan": cam.get_pan_angle() if cam else None}
        return {"success": False, "message": "Camera not found"}

    def zoom(self, camera_id: int, direction: str):
        control = (
            CameraController.CONTROL_ZOOM_IN
            if direction.lower() == "in"
            else CameraController.CONTROL_ZOOM_OUT
        )
        success = self._controller.control_single_camera(camera_id, control)
        if success:
            cam = self._get_camera(camera_id)
            return {"success": True, "zoom": cam.get_zoom_level() if cam else None}
        return {"success": False, "message": "Camera not found"}

    def tilt(self, camera, direction: str):
        if not camera:
            return {"success": False, "message": "Camera not found"}
        if hasattr(camera, "tilt_up") and hasattr(camera, "tilt_down"):
            success = camera.tilt_up() if direction == "up" else camera.tilt_down()
            return {"success": success, "tilt": getattr(camera, "tilt_angle", None)}
        return {"success": False, "message": "Tilt not supported"}

    def enable(self, camera_id: int):
        if self._controller.enable_camera(camera_id):
            return {"success": True}
        return {"success": False, "message": "Camera not found"}

    def disable(self, camera_id: int):
        if self._controller.disable_camera(camera_id):
            return {"success": True}
        return {"success": False, "message": "Camera not found"}

    def _get_camera(self, cam_id: int) -> Optional[SafeHomeCamera]:
        try:
            return self._controller.get_camera_by_id(cam_id)
        except Exception:
            return None


