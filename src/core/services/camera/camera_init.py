"""Camera initialization helpers."""

from __future__ import annotations

from typing import Dict, List


class CameraInitService:
    """Handles camera initialization from configuration."""

    def __init__(self, controller, camera_lookup: Dict[str, int], camera_labels: Dict[int, str]):
        self._controller = controller
        self._lookup = camera_lookup
        self._labels = camera_labels

    def initialize(self, camera_data: List[Dict]):
        for cam in camera_data:
            cam_name = cam.get("id")
            if not cam_name:
                continue
            controller_id = self._controller.add_camera(
                int(cam.get("x", 0)), int(cam.get("y", 0))
            )
            if controller_id is None:
                continue
            label = cam.get("location", cam_name)
            self._lookup[cam_name] = controller_id
            self._labels[controller_id] = label
            camera = self._controller.get_camera_by_id(controller_id)
            if camera:
                camera.enable()

