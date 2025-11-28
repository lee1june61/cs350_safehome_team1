"""
Display and thumbnail helpers for CameraController.
"""
from __future__ import annotations

from typing import Any, List, Optional, Tuple

from .camera_controller_base import CameraControllerBase


class CameraControllerDisplayMixin(CameraControllerBase):
    """Fetch frames from underlying devices."""

    def display_single_view(self, camera_id: int) -> Optional[Any]:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return None
            if hasattr(camera, "is_enabled") and not camera.is_enabled():
                return None
            try:
                return camera.display_view()
            except Exception as exc:  # pragma: no cover - logging path
                print(f"Error displaying view from camera {camera_id}: {exc}")
                return None

    def display_thumbnail_view(self) -> List[Tuple[int, Optional[Any]]]:
        with self._lock:
            thumbnails: List[Tuple[int, Optional[Any]]] = []
            for camera in self.camera_list:
                if not hasattr(camera, "is_enabled") or not camera.is_enabled():
                    continue
                camera_id = camera.get_id()
                try:
                    view = camera.display_view()
                except Exception:
                    view = None
                thumbnails.append((camera_id, view))
            return thumbnails

