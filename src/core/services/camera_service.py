"""Camera orchestration helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

from ...controllers.camera_controller import CameraController
from ...devices.cameras.safehome_camera import SafeHomeCamera
from ..logging.system_logger import SystemLogger
from .camera import CameraQueryService, CameraControlService, CameraSecurityService, CameraInitService


class CameraService:
    """Handles camera initialization, view, controls, and passwords."""

    def __init__(self, controller: CameraController, logger: SystemLogger):
        self._controller = controller
        self._camera_lookup: Dict[str, int] = {}
        self._camera_labels: Dict[int, str] = {}
        self._init = CameraInitService(controller, self._camera_lookup, self._camera_labels)
        self._query = CameraQueryService(controller, self._camera_labels)
        self._control = CameraControlService(controller)
        self._security = CameraSecurityService(controller, self._camera_labels)

    def initialize_defaults(self, camera_data: List[Dict]):
        self._init.initialize(camera_data)

    def list_cameras(self):
        return self._query.list_cameras()

    def get_camera(self, camera_id: str):
        cam_id = self._normalize(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        cam = self._safe_get_camera(cam_id)
        return self._query.get_camera(cam_id, cam) if cam else {"success": False, "message": "Camera not found"}

    def get_camera_view(self, camera_id: str):
        cam_id = self._normalize(camera_id)
        return self._query.get_camera_view(cam_id) if cam_id else {"success": False, "message": "Invalid camera ID"}

    def pan_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize(camera_id)
        return self._control.pan(cam_id, direction) if cam_id else self._invalid_id()

    def zoom_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize(camera_id)
        return self._control.zoom(cam_id, direction) if cam_id else self._invalid_id()

    def tilt_camera(self, camera_id="", direction="", **_):
        cam_id = self._normalize(camera_id)
        if cam_id is None:
            return self._invalid_id()
        cam = self._safe_get_camera(cam_id)
        return self._control.tilt(cam, direction) if cam else {"success": False, "message": "Camera not found"}

    def enable_camera(self, camera_id="", **_):
        cam_id = self._normalize(camera_id)
        return self._control.enable(cam_id) if cam_id else self._invalid_id()

    def disable_camera(self, camera_id="", **_):
        cam_id = self._normalize(camera_id)
        return self._control.disable(cam_id) if cam_id else self._invalid_id()

    def set_password(self, camera_id="", old_password="", password="", **_):
        cam_id, cam = self._resolve(camera_id)
        return self._security.set_password(cam, cam_id, old_password, password) if cam else {"success": False, "message": cam_id or "Camera not found"}

    def delete_password(self, camera_id="", old_password="", **_):
        cam_id, cam = self._resolve(camera_id)
        return self._security.delete_password(cam, cam_id, old_password) if cam else {"success": False, "message": cam_id or "Camera not found"}

    def verify_password(self, camera_id="", password="", **_):
        cam_id, cam = self._resolve(camera_id)
        return self._security.verify_password(cam_id, password, cam) if cam else {"success": False, "message": cam_id or "Camera not found"}

    def get_thumbnails(self):
        return self._security.thumbnails()

    def camera_info(self):
        return self._controller.get_all_camera_info()

    @property
    def labels(self) -> Dict[int, str]:
        return self._camera_labels

    def _normalize(self, camera_id) -> Optional[int]:
        if isinstance(camera_id, int):
            return camera_id
        if not camera_id:
            return None
        normalized = str(camera_id).strip().upper().lstrip("C")
        try:
            return int(normalized)
        except (TypeError, ValueError):
            return None

    def _safe_get_camera(self, cam_id: int) -> Optional[SafeHomeCamera]:
        try:
            return self._controller.get_camera_by_id(cam_id)
        except Exception:
            return None

    def _resolve(self, camera_id: str):
        cam_id = self._normalize(camera_id)
        return ("Invalid camera ID", None) if cam_id is None else (cam_id, self._safe_get_camera(cam_id))

    def _invalid_id(self):
        return {"success": False, "message": "Invalid camera ID"}
