"""
Device interfaces for SafeHome system.
Base abstract interfaces that all devices must implement.
"""
from abc import ABC, abstractmethod
from typing import Optional


class InterfaceCamera(ABC):
    """Abstract interface for camera devices."""
    
    @abstractmethod
    def get_location(self) -> str:
        """Get camera location identifier."""
        pass
    
    @abstractmethod
    def get_pan(self) -> int:
        """Get current pan angle (-180 to 180 degrees)."""
        pass
    
    @abstractmethod
    def get_tilt(self) -> int:
        """Get current tilt angle (-90 to 90 degrees)."""
        pass
    
    @abstractmethod
    def get_zoom(self) -> int:
        """Get current zoom level (0-100)."""
        pass
    
    @abstractmethod
    def set_pan(self, angle: int) -> bool:
        """Set pan angle. Returns True if successful."""
        pass
    
    @abstractmethod
    def set_tilt(self, angle: int) -> bool:
        """Set tilt angle. Returns True if successful."""
        pass
    
    @abstractmethod
    def set_zoom(self, level: int) -> bool:
        """Set zoom level. Returns True if successful."""
        pass
    
    @abstractmethod
    def capture_frame(self) -> Optional[bytes]:
        """Capture current frame. Returns image data or None."""
        pass


class InterfaceSensor(ABC):
    """Abstract interface for sensor devices."""
    
    @abstractmethod
    def get_location(self) -> str:
        """Get sensor location identifier."""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Get sensor type (motion, door, window)."""
        pass
    
    @abstractmethod
    def is_triggered(self) -> bool:
        """Check if sensor is currently triggered."""
        pass
    
    @abstractmethod
    def arm(self) -> bool:
        """Arm the sensor. Returns True if successful."""
        pass
    
    @abstractmethod
    def disarm(self) -> bool:
        """Disarm the sensor. Returns True if successful."""
        pass
    
    @abstractmethod
    def is_armed(self) -> bool:
        """Check if sensor is armed."""
        pass
    
    @abstractmethod
    def get_battery_level(self) -> int:
        """Get battery level (0-100%)."""
        pass
