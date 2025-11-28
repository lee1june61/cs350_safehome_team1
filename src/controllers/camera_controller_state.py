"""
Enable/disable responsibilities for CameraController.
"""
from __future__ import annotations

from typing import List

from .camera_controller_base import CameraControllerBase


class CameraControllerStateMixin(CameraControllerBase):
    """Bulk and single camera state toggles."""

    def enable_cameras(self, camera_id_list: List[int]) -> List[bool]:
        with self._lock:
            results: List[bool] = []
            for camera_id in camera_id_list:
                camera = self._cameras.get(camera_id)
                if camera is None:
                    results.append(False)
                    continue
                results.append(bool(camera.enable()))
            return results

    def disable_cameras(self, camera_id_list: List[int]) -> List[bool]:
        with self._lock:
            results: List[bool] = []
            for camera_id in camera_id_list:
                camera = self._cameras.get(camera_id)
                if camera is None:
                    results.append(False)
                    continue
                results.append(bool(camera.disable()))
            return results

    def enable_camera(self, camera_id: int) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return False
            return bool(camera.enable())

    def disable_camera(self, camera_id: int) -> bool:
        with self._lock:
            camera = self._cameras.get(camera_id)
            if camera is None:
                return False
            return bool(camera.disable())

    def enable_all_camera(self) -> int:
        with self._lock:
            count = 0
            for camera in self.camera_list:
                if hasattr(camera, "enable") and camera.enable():
                    count += 1
            return count

    def disable_all_camera(self) -> int:
        with self._lock:
            count = 0
            for camera in self.camera_list:
                if hasattr(camera, "disable") and camera.disable():
                    count += 1
            return count

    # Backward compatible aliases for SDS naming differences
    def enable_all_cameras(self) -> int:
        return self.enable_all_camera()

    def disable_all_cameras(self) -> int:
        return self.disable_all_camera()

