"""
SafeHome Camera Module
======================
Main camera logic class for the SafeHome security system.

This class implements the InterfaceCamera and manages a single camera's
state including location, pan angle, zoom level, password protection,
and enabled/disabled status.
"""

from __future__ import annotations

import threading
from typing import Optional, Tuple, Any

from .interface_camera import InterfaceCamera
from .device_camera import DeviceCamera
from .exceptions import (
    CameraDisabledError,
    CameraPasswordError,
    CameraValidationError
)


class SafeHomeCamera(InterfaceCamera):
    """
    Main camera class for the SafeHome system.
    
    This class implements the complete logic for a single camera, managing
    its state and delegating hardware operations to a DeviceCamera instance.
    
    Attributes:
        camera_id (int): Unique identifier for this camera
        location (Tuple[int, int]): (x, y) coordinates of the camera location
        pan_angle (int): Current pan angle of the camera (-5 to +5)
        zoom_setting (int): Current zoom level of the camera (1 to 9)
        password (Optional[str]): The password for this camera (if any)
        enabled (bool): Whether this camera is currently enabled
    """
    
    # Class constants
    MIN_ZOOM = 1
    MAX_ZOOM = 9
    MIN_PAN = -5
    MAX_PAN = 5
    
    def __init__(self, camera_id: int, x_coord: int, y_coord: int) -> None:
        """
        Initialize a SafeHome camera.
        
        Args:
            camera_id (int): Unique identifier for this camera
            x_coord (int): X coordinate of the camera location
            y_coord (int): Y coordinate of the camera location
        """
        # Public attributes
        self.camera_id: int = camera_id
        self.location: Tuple[int, int] = (x_coord, y_coord)
        self.pan_angle: int = 0
        self.zoom_setting: int = 2
        self.password: Optional[str] = None
        self.enabled: bool = False
        
        # Private attributes
        self._has_password: bool = False
        self._device: DeviceCamera = DeviceCamera(camera_id)
        self._lock: threading.RLock = threading.RLock()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def validate(self) -> bool:
        """
        Validate camera state and configuration.
        
        Returns:
            bool: True if validation passes
        
        Raises:
            CameraValidationError: If validation fails
        """
        with self._lock:
            if self.camera_id <= 0:
                raise CameraValidationError("Camera ID must be positive")
            
            if not isinstance(self.location, tuple) or len(self.location) != 2:
                raise CameraValidationError("Location must be a tuple of (x, y)")
            
            if not (self.MIN_PAN <= self.pan_angle <= self.MAX_PAN):
                raise CameraValidationError(
                    f"Pan angle must be between {self.MIN_PAN} and {self.MAX_PAN}"
                )
            
            if not (self.MIN_ZOOM <= self.zoom_setting <= self.MAX_ZOOM):
                raise CameraValidationError(
                    f"Zoom setting must be between {self.MIN_ZOOM} and {self.MAX_ZOOM}"
                )
            
            return True
    
    # ------------------------------------------------------------------
    # Display methods
    # ------------------------------------------------------------------
    
    def display_view(self) -> Any:
        """
        Get the current camera view/frame.
        
        Returns:
            Any: The current camera frame from the device
        
        Raises:
            CameraDisabledError: If camera is disabled
        """
        with self._lock:
            if not self.enabled:
                raise CameraDisabledError(
                    f"Camera {self.camera_id} is disabled. Enable it first."
                )
            return self._device.get_frame()
    
    # ------------------------------------------------------------------
    # Zoom control methods
    # ------------------------------------------------------------------
    
    def zoom_in(self) -> bool:
        """
        Zoom in the camera view.
        
        Returns:
            bool: True if zoom was successful, False if at maximum zoom
        """
        with self._lock:
            if not self.enabled:
                return False
            if self.zoom_setting >= self.MAX_ZOOM:
                return False
            if self._device.zoom_in():
                self.zoom_setting += 1
                return True
            return False
    
    def zoom_out(self) -> bool:
        """
        Zoom out the camera view.
        
        Returns:
            bool: True if zoom was successful, False if at minimum zoom
        """
        with self._lock:
            if not self.enabled:
                return False
            if self.zoom_setting <= self.MIN_ZOOM:
                return False
            if self._device.zoom_out():
                self.zoom_setting -= 1
                return True
            return False
    
    # ------------------------------------------------------------------
    # Pan control methods
    # ------------------------------------------------------------------
    
    def pan_left(self) -> bool:
        """
        Pan the camera to the left.
        
        Returns:
            bool: True if pan was successful, False if at leftmost position
        """
        with self._lock:
            if not self.enabled:
                return False
            if self.pan_angle <= self.MIN_PAN:
                return False
            if self._device.pan_left():
                self.pan_angle -= 1
                return True
            return False
    
    def pan_right(self) -> bool:
        """
        Pan the camera to the right.
        
        Returns:
            bool: True if pan was successful, False if at rightmost position
        """
        with self._lock:
            if not self.enabled:
                return False
            if self.pan_angle >= self.MAX_PAN:
                return False
            if self._device.pan_right():
                self.pan_angle += 1
                return True
            return False
    
    # ------------------------------------------------------------------
    # Password management methods
    # ------------------------------------------------------------------
    
    def set_password(self, password: str) -> None:
        """
        Set a password for this camera.
        
        Args:
            password (str): The password to set. Must not be empty.
        
        Raises:
            CameraPasswordError: If password is empty or None
        """
        with self._lock:
            if not password:
                raise CameraPasswordError("Password cannot be empty")
            self.password = password
            self._has_password = True
    
    def get_password(self) -> Optional[str]:
        """
        Get the camera's password.
        
        Returns:
            Optional[str]: The camera's password, or None if no password is set
        """
        with self._lock:
            return self.password
    
    def has_password(self) -> bool:
        """
        Check if the camera has a password set.
        
        Returns:
            bool: True if camera has a password, False otherwise
        """
        with self._lock:
            return self._has_password
    
    # ------------------------------------------------------------------
    # Enable/Disable methods
    # ------------------------------------------------------------------
    
    def enable(self) -> None:
        """Enable the camera (turn it on)."""
        with self._lock:
            self.enabled = True
    
    def disable(self) -> None:
        """Disable the camera (turn it off)."""
        with self._lock:
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """
        Check if the camera is currently enabled.
        
        Returns:
            bool: True if camera is enabled, False otherwise
        """
        with self._lock:
            return self.enabled
    
    # ------------------------------------------------------------------
    # Getter methods
    # ------------------------------------------------------------------
    
    def get_id(self) -> int:
        """
        Get the camera's unique identifier.
        
        Returns:
            int: The camera's ID
        """
        with self._lock:
            return self.camera_id
    
    def get_location(self) -> Tuple[int, int]:
        """
        Get the camera's location coordinates.
        
        Returns:
            Tuple[int, int]: A tuple of (x, y) coordinates
        """
        with self._lock:
            return self.location
    
    def get_pan_angle(self) -> int:
        """
        Get the current pan angle of the camera.
        
        Returns:
            int: The current pan angle (-5 to +5)
        """
        with self._lock:
            return self.pan_angle
    
    def get_zoom_setting(self) -> int:
        """
        Get the current zoom setting of the camera.
        
        Returns:
            int: The current zoom level (1 to 9)
        """
        with self._lock:
            return self.zoom_setting
    
    # ------------------------------------------------------------------
    # Cleanup methods
    # ------------------------------------------------------------------
    
    def cleanup(self) -> None:
        """
        Cleanup camera resources.
        This method should be called when the camera is no longer needed.
        """
        with self._lock:
            if self._device:
                self._device.stop()
    
    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    
    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup()
    
    def __repr__(self) -> str:
        """
        String representation of the camera.
        
        Returns:
            str: A string describing the camera state
        """
        with self._lock:
            return (f"SafeHomeCamera(id={self.camera_id}, location={self.location}, "
                    f"enabled={self.enabled}, pan={self.pan_angle}, zoom={self.zoom_setting})")
