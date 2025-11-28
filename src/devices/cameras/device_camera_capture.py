"""
Frame capture logic for DeviceCamera.
"""
from __future__ import annotations

import time
from typing import Optional

from .device_camera_base import DeviceCameraBase


class DeviceCameraCaptureMixin(DeviceCameraBase):
    """Simulate frame generation."""

    def capture_frame(self) -> Optional[bytes]:
        if not self._enabled:
            return None

        self._last_capture_time = time.time()
        frame_data = (
            f"CAMERA_FRAME|"
            f"ID={self._camera_id}|"
            f"LOC={self._location}|"
            f"PAN={self._pan}|"
            f"TILT={self._tilt}|"
            f"ZOOM={self._zoom}|"
            f"TIME={self._last_capture_time}"
        )
        return frame_data.encode("utf-8")

    def get_view(self) -> Optional[bytes]:
        """InterfaceCamera alias for capture_frame."""
        return self.capture_frame()

