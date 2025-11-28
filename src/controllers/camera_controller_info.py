"""
Information and cleanup helpers for CameraController.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .camera_controller_base import CameraControllerBase


class CameraControllerInfoMixin(CameraControllerBase):
    """Info queries plus lifecycle hooks."""

    def get_all_camera_info(self) -> List[Dict[str, Any]]:
        with self._lock:
            camera_info_list = []
            for camera in self.camera_list:
                info = {
                    "id": camera.get_id(),
                    "location": camera.get_location(),
                    "enabled": camera.is_enabled(),
                    "pan": camera.get_pan_angle(),
                    "zoom": camera.get_zoom_level(),
                    "has_password": camera.has_password(),
                }
                camera_info_list.append(info)
            return camera_info_list

    def cleanup(self) -> None:
        with self._lock:
            for camera in list(self._cameras.values()):
                if hasattr(camera, "cleanup"):
                    camera.cleanup()
            self._cameras.clear()
            self._camera_list.clear()
            self.total_camera_number = 0
            self.next_camera_id = 1

    def __del__(self) -> None:
        try:
            self.cleanup()
        except Exception:
            pass

    def __repr__(self) -> str:
        with self._lock:
            return (
                f"CameraController(total_cameras={self.total_camera_number}, "
                f"next_id={self.next_camera_id})"
            )

