"""
Base utilities shared across SafeHomeCamera mixins.
"""
from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from ...virtual_devices.device_camera import DeviceCamera


class SafeHomeCameraBase:
    """Shared state and helpers for SafeHomeCamera mixins."""

    MIN_ZOOM = 1
    MAX_ZOOM = 9
    MIN_PAN = -5
    MAX_PAN = 5
    _ASSET_DIR = Path(__file__).resolve().parents[2] / "resources" / "images"
    _DEVICE_ASSET_LOCK = threading.RLock()

    def __init__(self, camera_id: int, x_coord: int, y_coord: int) -> None:
        self.camera_id: int = camera_id
        self.location: List[int] = [x_coord, y_coord]
        self.pan_angle: int = 0
        self.zoom_level: int = 2
        self.password: Optional[str] = None
        self.enabled: bool = False

        self._has_password: bool = False
        self._device: DeviceCamera = DeviceCamera()
        self._lock: threading.RLock = threading.RLock()
        self._asset_dir: Path = self._ASSET_DIR

        self._initialize_device(camera_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _initialize_device(self, camera_id: int) -> None:
        """Configure the underlying virtual device."""
        with self._DEVICE_ASSET_LOCK:
            with self._temporary_asset_directory():
                self._device.set_id(camera_id)

    @contextmanager
    def _temporary_asset_directory(self):
        """
        Temporarily switch the working directory to the virtual_device assets
        directory so that DeviceCamera can discover camera images.
        """
        original_cwd = Path.cwd()
        try:
            os.chdir(self._asset_dir)
            yield
        finally:
            os.chdir(original_cwd)

