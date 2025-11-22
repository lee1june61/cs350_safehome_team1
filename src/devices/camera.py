"""
Camera device implementation.
Virtual camera with PTZ (Pan-Tilt-Zoom) capabilities.
"""
import time
from typing import Optional
from .interfaces import InterfaceCamera


class DeviceCamera(InterfaceCamera):
    """
    Virtual camera device with PTZ capabilities.
    Simulates a network-connected security camera.
    """
    
    # PTZ limits (class constants)
    PAN_MIN = -180
    PAN_MAX = 180
    TILT_MIN = -90
    TILT_MAX = 90
    ZOOM_MIN = 0
    ZOOM_MAX = 100
    
    def __init__(self, location: str, camera_id: int):
        """
        Initialize camera device.
        
        Args:
            location: Physical location (e.g., "Front Door", "Living Room")
            camera_id: Unique camera identifier
        """
        self._location = location
        self._camera_id = camera_id
        self._pan = 0  # Current pan angle
        self._tilt = 0  # Current tilt angle
        self._zoom = 0  # Current zoom level
        self._enabled = True
        self._last_capture_time = 0
        self._password = None  # Optional camera password
    
    # ============================================================
    # InterfaceCamera Implementation
    # ============================================================
    
    def get_location(self) -> str:
        return self._location
    
    def get_pan(self) -> int:
        return self._pan
    
    def get_tilt(self) -> int:
        return self._tilt
    
    def get_zoom(self) -> int:
        return self._zoom
    
    def set_pan(self, angle: int) -> bool:
        """Set pan angle with bounds checking."""
        if not self._enabled:
            return False
        
        if self.PAN_MIN <= angle <= self.PAN_MAX:
            self._pan = angle
            return True
        return False
    
    def set_tilt(self, angle: int) -> bool:
        """Set tilt angle with bounds checking."""
        if not self._enabled:
            return False
        
        if self.TILT_MIN <= angle <= self.TILT_MAX:
            self._tilt = angle
            return True
        return False
    
    def set_zoom(self, level: int) -> bool:
        """Set zoom level with bounds checking."""
        if not self._enabled:
            return False
        
        if self.ZOOM_MIN <= level <= self.ZOOM_MAX:
            self._zoom = level
            return True
        return False
    
    def capture_frame(self) -> Optional[bytes]:
        """
        Simulate frame capture.
        In real implementation, this would return actual image data from camera.
        """
        if not self._enabled:
            return None
        
        self._last_capture_time = time.time()
        
        # Simulate image data with metadata
        frame_data = (
            f"CAMERA_FRAME|"
            f"ID={self._camera_id}|"
            f"LOC={self._location}|"
            f"PAN={self._pan}|"
            f"TILT={self._tilt}|"
            f"ZOOM={self._zoom}|"
            f"TIME={self._last_capture_time}"
        )
        return frame_data.encode('utf-8')
    
    # ============================================================
    # Additional Camera Methods
    # ============================================================
    
    def get_camera_id(self) -> int:
        """Get camera ID."""
        return self._camera_id
    
    def enable(self):
        """Enable camera for recording/viewing."""
        self._enabled = True
    
    def disable(self):
        """Disable camera (privacy mode)."""
        self._enabled = False
    
    def is_enabled(self) -> bool:
        """Check if camera is enabled."""
        return self._enabled
    
    def set_password(self, password: str):
        """Set access password for this camera."""
        self._password = password
    
    def clear_password(self):
        """Remove access password."""
        self._password = None
    
    def verify_password(self, password: str) -> bool:
        """Verify camera access password."""
        if self._password is None:
            return True  # No password set
        return self._password == password