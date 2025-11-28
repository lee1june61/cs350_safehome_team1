"""
Camera device implementation using mixin composition.
"""
from __future__ import annotations

from .device_camera_base import DeviceCameraBase
from .device_camera_capture import DeviceCameraCaptureMixin
from .device_camera_ptz import DeviceCameraPTZMixin
from .device_camera_security import DeviceCameraSecurityMixin


class DeviceCamera(
    DeviceCameraCaptureMixin,
    DeviceCameraPTZMixin,
    DeviceCameraSecurityMixin,
    DeviceCameraBase,
):
    """Virtual camera device with PTZ capabilities."""

    def __init__(self, location: str, camera_id: int):
        super().__init__(location, camera_id)

