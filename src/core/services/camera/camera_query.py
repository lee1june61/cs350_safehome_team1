"""Query-focused camera helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

from src.controllers.camera_controller import CameraController


class CameraQueryService:
    """Provides camera list/detail/view operations."""

    def __init__(self, controller: CameraController, labels: Dict[int, str]):
        self._controller = controller
        self._labels = labels

    def list_cameras(self) -> Dict[str, List[Dict]]:
        cameras = []
        for cam in self._controller.get_all_camera_info():
            cam_id = cam.get("id")
            if cam_id is None:
                continue
            label = self._labels.get(cam_id, f"C{cam_id}")
            cameras.append(
                {
                    "id": f"C{cam_id}",
                    "location": label,
                    "coords": cam.get("location"),
                    "enabled": cam.get("enabled", False),
                    "pan": cam.get("pan"),
                    "zoom": cam.get("zoom"),
                    "has_password": cam.get("has_password"),
                }
            )
        return {"success": True, "data": cameras}

    def get_camera(self, cam_id: int, camera) -> Dict[str, any]:
        coords = camera.get_location()
        label = self._labels.get(cam_id, f"C{cam_id}")
        data = {
            "id": f"C{camera.get_id()}",
            "location": label,
            "coords": coords,
            "enabled": camera.is_enabled(),
            "pan": camera.get_pan_angle(),
            "zoom": camera.get_zoom_level(),
            "has_password": camera.has_password(),
        }
        return {"success": True, "data": data}

    def get_camera_view(self, cam_id: int):
        view = self._controller.display_single_view(cam_id)
        if view is None:
            return {"success": False, "message": "Camera not available"}
        return {"success": True, "view": view}

    def camera_info(self):
        return self._controller.get_all_camera_info()


