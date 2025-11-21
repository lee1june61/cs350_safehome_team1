"""
Camera Module Exceptions
=========================
Custom exception classes for the camera module.
"""

from __future__ import annotations


class CameraError(Exception):
    """Base exception for camera-related errors."""
    pass


class CameraNotFoundError(CameraError):
    """Raised when a camera with the specified ID is not found."""
    pass


class CameraDisabledError(CameraError):
    """Raised when attempting to use a disabled camera."""
    pass


class CameraLimitError(CameraError):
    """Raised when camera control limits are reached."""
    pass


class CameraPasswordError(CameraError):
    """Raised when password validation fails."""
    pass


class CameraValidationError(CameraError):
    """Raised when camera validation fails."""
    pass

