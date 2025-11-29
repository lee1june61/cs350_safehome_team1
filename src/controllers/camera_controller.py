"""Camera Controller Module."""
from __future__ import annotations

from .camera_controller_base import CameraControllerBase
from .camera_controller_control import CameraControllerControlMixin
from .camera_controller_display import CameraControllerDisplayMixin
from .camera_controller_info import CameraControllerInfoMixin
from .camera_controller_registry import CameraControllerRegistryMixin
from .camera_controller_security import CameraControllerSecurityMixin
from .camera_controller_state import CameraControllerStateMixin


class CameraController(
    CameraControllerDisplayMixin,
    CameraControllerControlMixin,
    CameraControllerSecurityMixin,
    CameraControllerStateMixin,
    CameraControllerInfoMixin,
    CameraControllerRegistryMixin,
    CameraControllerBase,
):
    """
    Controller for managing multiple SafeHomeCamera instances.

    The class composition stays the same as before, but each responsibility now
    lives in a dedicated mixin module to keep files short and cohesive.
    """

    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> bool:
        """Legacy initialization hook for compatibility tests."""
        return True