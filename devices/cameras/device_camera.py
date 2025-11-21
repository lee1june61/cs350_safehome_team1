"""
Device Camera Module
====================
Low-level hardware abstraction for camera devices.

This module provides a wrapper around the virtual camera device implementation,
handling the actual video feed simulation using static images.
"""

import sys
from pathlib import Path
from typing import Optional, Any


# Import the DeviceCamera from virtual_device_v3
try:
    virtual_device_path = Path(__file__).parent.parent.parent / "virtual_device_v3" / "virtual_device_v3"
    if str(virtual_device_path) not in sys.path:
        sys.path.insert(0, str(virtual_device_path))
    from device.device_camera import DeviceCamera as VirtualDeviceCamera
except ImportError as e:
    print(f"Warning: Could not import DeviceCamera from virtual_device_v3: {e}")
    VirtualDeviceCamera = None


class DeviceCamera:
    """
    Low-level camera hardware abstraction.
    
    This class wraps the virtual device camera implementation and provides
    a simplified interface for getting video frames. It simulates a camera
    by loading static images from the resources directory.
    
    Attributes:
        _camera_id (int): The ID of this camera device
        _device_camera (Optional[Any]): The underlying virtual device camera instance
    """
    
    def __init__(self, camera_id: int = 0):
        """
        Initialize a device camera.
        
        Args:
            camera_id (int): The ID for this camera (used to load camera{id}.jpg)
        """
        # Private attributes
        self._camera_id: int = camera_id
        self._device_camera: Optional[Any] = None
        
        # Initialize the virtual device camera if available
        if VirtualDeviceCamera is not None:
            self._device_camera = VirtualDeviceCamera()
            if camera_id > 0:
                self._device_camera.set_id(camera_id)
    
    # Frame methods
    def get_frame(self) -> Optional[Any]:
        """
        Get the current frame/view from the camera.
        
        Returns:
            Optional[Any]: The current camera frame as a PIL Image object,
                          or None if the camera is not available
        """
        if self._device_camera is not None:
            try:
                return self._device_camera.get_view()
            except Exception as e:
                print(f"Error getting camera frame: {e}")
                return None
        return None
    
    # ID management methods
    def set_camera_id(self, camera_id: int) -> None:
        """
        Set the camera ID and load the associated image.
        
        Args:
            camera_id (int): The new camera ID
        """
        self._camera_id = camera_id
        if self._device_camera is not None:
            self._device_camera.set_id(camera_id)
    
    def get_camera_id(self) -> int:
        """
        Get the camera ID.
        
        Returns:
            int: The camera ID
        """
        if self._device_camera is not None:
            return self._device_camera.get_id()
        return self._camera_id
    
    # Pan control methods
    def pan_left(self) -> bool:
        """
        Pan the camera left (internal device operation).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._device_camera is not None:
            return self._device_camera.pan_left()
        return False
    
    def pan_right(self) -> bool:
        """
        Pan the camera right (internal device operation).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._device_camera is not None:
            return self._device_camera.pan_right()
        return False
    
    # Zoom control methods
    def zoom_in(self) -> bool:
        """
        Zoom in the camera (internal device operation).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._device_camera is not None:
            return self._device_camera.zoom_in()
        return False
    
    def zoom_out(self) -> bool:
        """
        Zoom out the camera (internal device operation).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._device_camera is not None:
            return self._device_camera.zoom_out()
        return False
    
    # Cleanup methods
    def stop(self) -> None:
        """Stop the camera device (cleanup)."""
        if self._device_camera is not None and hasattr(self._device_camera, 'stop'):
            self._device_camera.stop()
    
    # Special methods
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
