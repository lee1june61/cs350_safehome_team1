"""
DeviceIcon - Represents devices on the floor plan

SDS: Represents devices such as sensors, alarm, and camera on the floor plan.
"""
import tkinter as tk
from dataclasses import dataclass
from typing import Optional, Callable, Tuple


@dataclass
class DevicePosition:
    """Position and size information for a device icon"""
    x: int
    y: int
    width: int = 30
    height: int = 30


class DeviceIcon:
    """
    Visual representation of a device on floor plan.
    
    Responsibilities (from SDS CRC):
    - Hold image data of a device
    - Give image data on request
    - Hold location and size information
    """
    
    DEVICE_COLORS = {
        'DOOR': '#4CAF50', 'WINDOW': '#2196F3', 'MOTION': '#FF9800',
        'CAMERA': '#9C27B0', 'ALARM': '#F44336', 'DEFAULT': '#757575'
    }
    
    DEVICE_SYMBOLS = {
        'DOOR': 'D', 'WINDOW': 'W', 'MOTION': 'M',
        'CAMERA': 'C', 'ALARM': '!', 'DEFAULT': '?'
    }
    
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
        if self._is_triggered:
            return '#F44336'
        return self.DEVICE_COLORS.get(self._type, self.DEVICE_COLORS['DEFAULT'])
    
    def get_symbol(self) -> str:
        return self.DEVICE_SYMBOLS.get(self._type, self.DEVICE_SYMBOLS['DEFAULT'])
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw the device icon on a canvas"""
        canvas.delete(f'device_{self._id}')
        
        x, y = self._position.x, self._position.y
        w, h = self._position.width, self._position.height
        color = self.get_color()
        
        # Draw shape
        if self._type in ['CAMERA', 'ALARM']:
            canvas.create_oval(x - w//2, y - h//2, x + w//2, y + h//2,
                             fill=color, outline='black',
                             width=2 if self._is_active else 1,
                             tags=f'device_{self._id}')
        else:
            canvas.create_rectangle(x - w//2, y - h//2, x + w//2, y + h//2,
                                  fill=color, outline='black',
                                  width=2 if self._is_active else 1,
                                  tags=f'device_{self._id}')
        
        # Draw symbol
        canvas.create_text(x, y, text=self.get_symbol(), fill='white',
                          font=('Arial', 10, 'bold'), tags=f'device_{self._id}')
        
        # Bind click
        if self._on_click:
            canvas.tag_bind(f'device_{self._id}', '<Button-1>', 
                          lambda e: self._on_click(self))
    
    def set_click_handler(self, callback: Callable[['DeviceIcon'], None]) -> None:
        self._on_click = callback
    
    def contains_point(self, px: int, py: int) -> bool:
        x, y = self._position.x, self._position.y
        w, h = self._position.width, self._position.height
        return (x - w//2 <= px <= x + w//2) and (y - h//2 <= py <= y + h//2)
    
    def to_dict(self) -> dict:
        return {
            'id': self._id, 'type': self._type, 'name': self._name,
            'x': self._position.x, 'y': self._position.y,
            'active': self._is_active, 'triggered': self._is_triggered
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DeviceIcon':
        return cls(
            device_id=data['id'], device_type=data['type'],
            device_name=data['name'],
            position=DevicePosition(x=data.get('x', 0), y=data.get('y', 0))
        )
