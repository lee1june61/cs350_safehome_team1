"""
DeviceIcon - Visual representation of devices on floor plan

Single Responsibility: Manage device icon state and rendering.
"""
import tkinter as tk
from typing import Optional, Callable
from .device_position import DevicePosition


# Color and symbol constants
DEVICE_COLORS = {
    'DOOR': '#4CAF50', 'WINDOW': '#2196F3', 'MOTION': '#FF9800',
    'CAMERA': '#9C27B0', 'ALARM': '#F44336', 'DEFAULT': '#757575'
}

DEVICE_SYMBOLS = {
    'DOOR': 'D', 'WINDOW': 'W', 'MOTION': 'M',
    'CAMERA': 'C', 'ALARM': '!', 'DEFAULT': '?'
}


class DeviceIcon:
    """Visual representation of a device on floor plan"""
    
    def __init__(self, device_id: str, device_type: str,
                 device_name: str, position: DevicePosition):
        self._id = device_id
        self._type = device_type.upper()
        self._name = device_name
        self._position = position
        self._is_active = False
        self._is_triggered = False
        self._on_click: Optional[Callable] = None
    
    @property
    def device_id(self) -> str:
        return self._id
    
    @property
    def device_type(self) -> str:
        return self._type
    
    @property
    def device_name(self) -> str:
        return self._name
    
    @property
    def position(self) -> DevicePosition:
        return self._position
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = value
    
    @property
    def is_triggered(self) -> bool:
        return self._is_triggered
    
    @is_triggered.setter
    def is_triggered(self, value: bool):
        self._is_triggered = value
    
    def get_color(self) -> str:
        """Get display color based on state"""
        if self._is_triggered:
            return '#F44336'  # Red for triggered
        return DEVICE_COLORS.get(self._type, DEVICE_COLORS['DEFAULT'])
    
    def get_symbol(self) -> str:
        """Get display symbol for device type"""
        return DEVICE_SYMBOLS.get(self._type, DEVICE_SYMBOLS['DEFAULT'])
    
    def contains_point(self, px: int, py: int) -> bool:
        """Check if point is within icon bounds"""
        return self._position.contains(px, py)
    
    def set_click_handler(self, callback: Callable[['DeviceIcon'], None]):
        """Set click callback"""
        self._on_click = callback
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'id': self._id, 'type': self._type, 'name': self._name,
            'x': self._position.x, 'y': self._position.y,
            'active': self._is_active, 'triggered': self._is_triggered
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DeviceIcon':
        """Deserialize from dictionary"""
        return cls(
            device_id=data['id'], device_type=data['type'],
            device_name=data['name'],
            position=DevicePosition(x=data.get('x', 0), y=data.get('y', 0))
        )
