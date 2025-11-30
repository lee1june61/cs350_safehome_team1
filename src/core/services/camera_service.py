"""Camera orchestration helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

from ...controllers.camera_controller import CameraController
from ...devices.cameras.safehome_camera import SafeHomeCamera
from ..logging.system_logger import SystemLogger
from .camera.camera_query import CameraQueryService
from .camera.camera_control import CameraControlService
from .camera.camera_security import CameraSecurityService


class CameraService:
    """Handles camera initialization, view, controls, and passwords."""

    def __init__(self, controller: CameraController, logger: SystemLogger):
        self._controller = controller
        self._logger = logger
        self._camera_lookup: Dict[str, int] = {}
        self._camera_labels: Dict[int, str] = {}
        self._query = CameraQueryService(controller, self._camera_labels)
        self._control = CameraControlService(controller)
        self._security = CameraSecurityService(controller)

    # ------------------------------------------------------------------ #
    def initialize_defaults(self, camera_data: List[Dict]):
        for cam in camera_data:
            cam_name = cam.get("id")
            if not cam_name:
                continue
            x_coord = int(cam.get("x", 0))
            y_coord = int(cam.get("y", 0))
            controller_id = self._controller.add_camera(x_coord, y_coord)
            if controller_id is None:
                continue
            label = cam.get("location", cam_name)
            self._camera_lookup[cam_name] = controller_id
            self._camera_labels[controller_id] = label
            camera = self._controller.get_camera_by_id(controller_id)
            if camera:
                camera.enable()

    # ------------------------------------------------------------------ #
    def list_cameras(self):
        return self._query.list_cameras()

    def get_camera(self, camera_id: str):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        camera = self._safe_get_camera(cam_id)
        if not camera:
            return {"success": False, "message": "Camera not found"}
        return self._query.get_camera(cam_id, camera)

    def get_camera_view(self, camera_id: str):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        return self._query.get_camera_view(cam_id)

    def pan_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        return self._control.pan(cam_id, direction)

    def zoom_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        return self._control.zoom(cam_id, direction)

    def tilt_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        cam = self._safe_get_camera(cam_id)
        return self._control.tilt(cam, direction) if cam else {"success": False, "message": "Camera not found"}

    def enable_camera(self, camera_id="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        return self._control.enable(cam_id)

    def disable_camera(self, camera_id="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        return self._control.disable(cam_id)

    def set_password(self, camera_id="", old_password="", password="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        cam = self._safe_get_camera(cam_id)
        if cam is None:
            return {"success": False, "message": "Camera not found"}
        return self._security.set_password(cam, cam_id, old_password, password)

    def delete_password(self, camera_id="", old_password="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        cam = self._safe_get_camera(cam_id)
        if cam is None:
            return {"success": False, "message": "Camera not found"}
        return self._security.delete_password(cam, cam_id, old_password)

    def verify_password(self, camera_id="", password="", **_):
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        cam = self._safe_get_camera(cam_id)
        if cam is None:
            return {"success": False, "message": "Camera not found"}
        return self._security.verify_password(cam_id, password, cam)

    def get_thumbnails(self):
        return self._security.thumbnails()

    def camera_info(self):
        return self._controller.get_all_camera_info()

    # ------------------------------------------------------------------ #
    def _normalize_camera_id(self, camera_id: str) -> Optional[int]:
        if isinstance(camera_id, int):
            return camera_id
        if not camera_id:
            return None
        normalized = str(camera_id).strip().upper()
        if normalized.startswith("C"):
            normalized = normalized[1:]
        try:
            return int(normalized)
        except (TypeError, ValueError):
            return None

    def _safe_get_camera(self, cam_id: int) -> Optional[SafeHomeCamera]:
        try:
            return self._controller.get_camera_by_id(cam_id)
        except Exception:
            return None

    @property
    def labels(self) -> Dict[int, str]:
        return self._camera_labels


