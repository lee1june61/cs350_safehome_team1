"""Shared state and helpers for CameraController."""

from __future__ import annotations

import threading
from typing import Dict, List, Sequence

from ..devices.cameras.safehome_camera import SafeHomeCamera


class CameraControllerBase:
    """Holds shared state for all controller mixins."""

    CONTROL_ZOOM_IN = 1
    CONTROL_ZOOM_OUT = 2
    CONTROL_PAN_LEFT = 3
    CONTROL_PAN_RIGHT = 4

    MIN_COORD = 0
    MAX_COORD = 1000

    def __init__(self) -> None:
        self.next_camera_id: int = 1
        self.total_camera_number: int = 0
        self._camera_list: List[SafeHomeCamera] = []
        self._cameras: Dict[int, SafeHomeCamera] = {}
        self._lock: threading.RLock = threading.RLock()

    @property
    def camera_list(self) -> List[SafeHomeCamera]:
        """Expose the underlying camera collection (SDS contract)."""
        return self._camera_list

    @camera_list.setter
    def camera_list(self, cameras: Sequence[SafeHomeCamera]) -> None:
        with self._lock:
            self._camera_list = list(cameras)
            self._rebuild_indexes()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _register_camera(self, camera: SafeHomeCamera) -> None:
        self._camera_list.append(camera)
        self._cameras[camera.get_id()] = camera
        self.total_camera_number = len(self._camera_list)

    def _remove_camera(self, camera_id: int) -> SafeHomeCamera | None:
        camera = self._cameras.pop(camera_id, None)
        if camera is None:
            return None
        self._camera_list = [
            cam for cam in self._camera_list if cam.get_id() != camera_id
        ]
        self.total_camera_number = len(self._camera_list)
        return camera

    def _rebuild_indexes(self) -> None:
        self._cameras = {}
        max_id = 0
        for camera in self._camera_list:
            if not hasattr(camera, "get_id"):
                continue
            camera_id = camera.get_id()
            self._cameras[camera_id] = camera
            max_id = max(max_id, camera_id)
        self.total_camera_number = len(self._camera_list)
        self.next_camera_id = max(max_id + 1, self.next_camera_id)

    def _is_valid_location(self, x_coord: int, y_coord: int) -> bool:
        return self._coord_in_bounds(x_coord) and self._coord_in_bounds(y_coord)

    def _coord_in_bounds(self, coord: int) -> bool:
        return self.MIN_COORD <= coord <= self.MAX_COORD
