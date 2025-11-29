"""Camera-related command implementations."""

from __future__ import annotations

from typing import Dict, Any

from ..services.camera_service import CameraService


class CameraHandler:
    """Delegates camera requests to the camera service."""

    def __init__(self, camera_service: CameraService):
        self._camera_service = camera_service

    def get_cameras(self, **_) -> Dict[str, Any]:
        return self._camera_service.list_cameras()

    def get_camera(self, camera_id="", **_) -> Dict[str, Any]:
        return self._camera_service.get_camera(camera_id)

    def get_camera_view(self, camera_id="", **_) -> Dict[str, Any]:
        return self._camera_service.get_camera_view(camera_id)

    def camera_pan(self, camera_id="", direction="", **_) -> Dict[str, Any]:
        return self._camera_service.pan_camera(camera_id=camera_id, direction=direction)

    def camera_zoom(self, camera_id="", direction="", **_) -> Dict[str, Any]:
        return self._camera_service.zoom_camera(camera_id=camera_id, direction=direction)

    def camera_tilt(self, camera_id="", direction="", **_) -> Dict[str, Any]:
        return self._camera_service.tilt_camera(camera_id=camera_id, direction=direction)

    def enable_camera(self, camera_id="", **_) -> Dict[str, Any]:
        return self._camera_service.enable_camera(camera_id=camera_id)

    def disable_camera(self, camera_id="", **_) -> Dict[str, Any]:
        return self._camera_service.disable_camera(camera_id=camera_id)

    def set_camera_password(
        self, camera_id="", old_password="", password="", **_
    ) -> Dict[str, Any]:
        return self._camera_service.set_password(
            camera_id=camera_id, old_password=old_password, password=password
        )

    def delete_camera_password(self, camera_id="", old_password="", **_) -> Dict[str, Any]:
        return self._camera_service.delete_password(
            camera_id=camera_id, old_password=old_password
        )

    def verify_camera_password(self, camera_id="", password="", **_) -> Dict[str, Any]:
        return self._camera_service.verify_password(
            camera_id=camera_id, password=password
        )

    def get_thumbnails(self, **_) -> Dict[str, Any]:
        return self._camera_service.get_thumbnails()


