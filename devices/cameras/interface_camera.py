"""
Interface Camera Module
========================
Defines the abstract interface for a camera in the SafeHome security system.

This abstract base class specifies all required methods that concrete camera
implementations must provide.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Any


class InterfaceCamera(ABC):
    """
    Abstract interface for a camera device in the SafeHome system.
    
    This interface defines all the methods that a concrete camera implementation
    must provide, including control methods (zoom, pan) and state management
    (location, ID, password, enable/disable).
    """
    
    @abstractmethod
    def display_view(self) -> Any:
        """
        Get the current camera view/frame.
        
        Returns:
            Any: The current camera frame (typically a PIL Image object)
        """
        pass
    
    @abstractmethod
    def zoom_in(self) -> bool:
        """
        Zoom in the camera view.
        
        Returns:
            bool: True if zoom was successful, False if at maximum zoom
        """
        pass
    
    @abstractmethod
    def zoom_out(self) -> bool:
        """
        Zoom out the camera view.
        
        Returns:
            bool: True if zoom was successful, False if at minimum zoom
        """
        pass
    
    @abstractmethod
    def pan_left(self) -> bool:
        """
        Pan the camera to the left.
        
        Returns:
            bool: True if pan was successful, False if at leftmost position
        """
        pass
    
    @abstractmethod
    def pan_right(self) -> bool:
        """
        Pan the camera to the right.
        
        Returns:
            bool: True if pan was successful, False if at rightmost position
        """
        pass
    
    @abstractmethod
    def set_password(self, password: str) -> None:
        """
        Set a password for this camera.
        
        Args:
            password: The password to set for camera access
        """
        pass
    
    @abstractmethod
    def get_password(self) -> Optional[str]:
        """
        Get the camera's password.
        
        Returns:
            Optional[str]: The camera's password, or None if no password is set
        """
        pass
    
    @abstractmethod
    def enable(self) -> None:
        """
        Enable the camera (turn it on).
        """
        pass
    
    @abstractmethod
    def disable(self) -> None:
        """
        Disable the camera (turn it off).
        """
        pass
    
    @abstractmethod
    def get_id(self) -> int:
        """
        Get the camera's unique identifier.
        
        Returns:
            int: The camera's ID
        """
        pass
    
    @abstractmethod
    def get_location(self) -> Tuple[int, int]:
        """
        Get the camera's location coordinates.
        
        Returns:
            Tuple[int, int]: A tuple of (x, y) coordinates
        """
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """
        Check if the camera is currently enabled.
        
        Returns:
            bool: True if camera is enabled, False otherwise
        """
        pass
    
    @abstractmethod
    def has_password(self) -> bool:
        """
        Check if the camera has a password set.
        
        Returns:
            bool: True if camera has a password, False otherwise
        """
        pass
    
    @abstractmethod
    def get_pan_angle(self) -> int:
        """
        Get the current pan angle of the camera.
        
        Returns:
            int: The current pan angle
        """
        pass
    
    @abstractmethod
    def get_zoom_setting(self) -> int:
        """
        Get the current zoom setting of the camera.
        
        Returns:
            int: The current zoom level
        """
        pass
