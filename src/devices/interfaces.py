"""
Device Interfaces - Abstract interfaces from TA (virtual_device_v4)
"""
from abc import ABC, abstractmethod


class InterfaceCamera(ABC):
    """Abstract interface for camera devices."""
    
    @abstractmethod
    def set_id(self, id_: int):
        """Set the camera ID and load associated image."""
        pass
    
    @abstractmethod
    def get_id(self) -> int:
        """Get the camera ID."""
        pass
    
    @abstractmethod
    def get_view(self):
        """Get the current camera view as an image (PIL Image)."""
        pass
    
    @abstractmethod
    def pan_right(self) -> bool:
        """Pan camera to the right. Returns True if successful."""
        pass
    
    @abstractmethod
    def pan_left(self) -> bool:
        """Pan camera to the left. Returns True if successful."""
        pass
    
    @abstractmethod
    def zoom_in(self) -> bool:
        """Zoom in. Returns True if successful."""
        pass
    
    @abstractmethod
    def zoom_out(self) -> bool:
        """Zoom out. Returns True if successful."""
        pass


class InterfaceSensor(ABC):
    """Abstract interface for sensor devices."""
    
    @abstractmethod
    def get_id(self) -> int:
        """Get sensor ID."""
        pass
    
    @abstractmethod
    def read(self) -> bool:
        """Read sensor state. Returns True if triggered."""
        pass
    
    @abstractmethod
    def arm(self):
        """Arm (enable) the sensor."""
        pass
    
    @abstractmethod
    def disarm(self):
        """Disarm (disable) the sensor."""
        pass
    
    @abstractmethod
    def test_armed_state(self) -> bool:
        """Test if sensor is armed."""
        pass
