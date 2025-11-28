"""
SafeHome Camera Module
======================
Main camera logic class for the SafeHome security system.
"""
from __future__ import annotations

from .safehome_camera_base import SafeHomeCameraBase
from .safehome_camera_display import SafeHomeCameraDisplayMixin
from .safehome_camera_lifecycle import SafeHomeCameraLifecycleMixin
from .safehome_camera_location import SafeHomeCameraLocationMixin
from .safehome_camera_pan import SafeHomeCameraPanMixin
from .safehome_camera_password import SafeHomeCameraPasswordMixin
from .safehome_camera_tilt import SafeHomeCameraTiltMixin
from .safehome_camera_validation import SafeHomeCameraValidationMixin
from .safehome_camera_zoom import SafeHomeCameraZoomMixin


class SafeHomeCamera(
    SafeHomeCameraDisplayMixin,
    SafeHomeCameraZoomMixin,
    SafeHomeCameraPanMixin,
    SafeHomeCameraTiltMixin,
    SafeHomeCameraLocationMixin,
    SafeHomeCameraPasswordMixin,
    SafeHomeCameraLifecycleMixin,
    SafeHomeCameraValidationMixin,
    SafeHomeCameraBase,
):
    """
    Main camera class for the SafeHome system.

    Responsibilities are split into mixins to keep files short while preserving
    the original public API surface.
    """

    def __init__(self, camera_id: int, x_coord: int, y_coord: int) -> None:
        super().__init__(camera_id, x_coord, y_coord)

