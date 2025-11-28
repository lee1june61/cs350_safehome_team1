"""
Camera control command dispatching.
"""
from __future__ import annotations

from .camera_controller_base import CameraControllerBase


class CameraControllerControlMixin(CameraControllerBase):
    """Translate SDS control IDs into SafeHomeCamera operations."""

    def control_single_camera(self, camera_id: int, control_id: int) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return False
            if hasattr(camera, "is_enabled") and not camera.is_enabled():
                return False

            action = None
            if control_id == self.CONTROL_ZOOM_IN and hasattr(camera, "zoom_in"):
                action = camera.zoom_in
            elif control_id == self.CONTROL_ZOOM_OUT and hasattr(camera, "zoom_out"):
                action = camera.zoom_out
            elif control_id == self.CONTROL_PAN_LEFT and hasattr(camera, "pan_left"):
                action = camera.pan_left
            elif control_id == self.CONTROL_PAN_RIGHT and hasattr(camera, "pan_right"):
                action = camera.pan_right
            if action:
                return bool(action())
            raise ValueError(f"Unknown control ID: {control_id}")

