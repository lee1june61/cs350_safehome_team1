"""
Security helpers for DeviceCamera.
"""
from __future__ import annotations

from .device_camera_base import DeviceCameraBase


class DeviceCameraSecurityMixin(DeviceCameraBase):
    """Password verification logic."""

    def verify_password(self, password: str) -> bool:
        if self._password is None:
            return True
        return self._password == password

