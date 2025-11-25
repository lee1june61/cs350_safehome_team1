"""
Custom exceptions for SafeHome system.
"""


class SafeHomeException(Exception):
    """Base exception for SafeHome system."""

    pass


class AuthenticationError(SafeHomeException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(SafeHomeException):
    """Raised when user lacks required permissions."""

    pass


class DeviceNotFoundError(SafeHomeException):
    """Raised when a device cannot be found."""

    pass


class DeviceError(SafeHomeException):
    """Raised when a device operation fails."""

    pass


class SensorError(DeviceError):
    """Raised when a sensor operation fails."""

    pass


class CameraError(DeviceError):
    """Raised when a camera operation fails."""

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


class ConfigurationError(SafeHomeException):
    """Raised when configuration is invalid."""

    pass


class StorageError(SafeHomeException):
    """Raised when storage operation fails."""

    pass


class SystemLockedException(SafeHomeException):
    """Raised when system is locked due to failed login attempts."""

    def __init__(self, lock_time_remaining: int):
        self.lock_time_remaining = lock_time_remaining
        super().__init__(f"System locked. Try again in {lock_time_remaining} seconds.")
