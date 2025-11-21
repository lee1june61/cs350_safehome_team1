"""
SafeHome Camera Module
======================
This module provides camera functionality for the SafeHome security system.

Classes:
    InterfaceCamera: Abstract base class for camera devices
    DeviceCamera: Low-level hardware abstraction (simulation)
    SafeHomeCamera: Main camera logic class
    CameraController: Camera collection manager

Exceptions:
    CameraError: Base exception for camera errors
    CameraNotFoundError: Camera not found
    CameraDisabledError: Camera is disabled
    CameraPasswordError: Password error
    CameraValidationError: Validation error

Usage:
    from safehome.devices.cameras import CameraController, SafeHomeCamera
    
    # Create a camera controller
    controller = CameraController()
    
    # Add cameras
    cam_id = controller.add_camera(100, 200)
    
    # Control cameras
    controller.enable_cameras([cam_id])
    controller.control_single_camera(cam_id, CameraController.CONTROL_ZOOM_IN)
"""

from __future__ import annotations

from .interface_camera import InterfaceCamera
from .device_camera import DeviceCamera
from .safehome_camera import SafeHomeCamera
from .camera_controller import CameraController
from .exceptions import (
    CameraError,
    CameraNotFoundError,
    CameraDisabledError,
    CameraLimitError,
    CameraPasswordError,
    CameraValidationError,
)

__all__ = [
    # Classes
    'InterfaceCamera',
    'DeviceCamera',
    'SafeHomeCamera',
    'CameraController',
    # Exceptions
    'CameraError',
    'CameraNotFoundError',
    'CameraDisabledError',
    'CameraLimitError',
    'CameraPasswordError',
    'CameraValidationError',
]

__version__ = '1.0.0'
__author__ = 'SafeHome Development Team'
