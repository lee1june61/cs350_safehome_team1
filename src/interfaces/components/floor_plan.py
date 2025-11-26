"""
FloorPlan - Contains and displays the house blueprint

SDS: Contains given image which describes the blueprint of the house.
"""
import tkinter as tk
from typing import List, Dict, Optional, Callable
from .device_icon import DeviceIcon, DevicePosition


class FloorPlan:
    """
    Manages and displays the house floor plan with device icons.
    
    Responsibilities (from SDS CRC):
    - Manage blueprint of the house
    - Draw the blueprint of the house
    """
    
    def __init__(self, parent: tk.Widget, width: int = 400, height: int = 300):
        self._parent = parent
        self._width = width
        self._height = height
        self._canvas: Optional[tk.Canvas] = None
        self._devices: Dict[str, DeviceIcon] = {}
        self._on_device_click: Optional[Callable] = None
        
        self._rooms = [
            {'name': 'Living Room', 'bounds': (30, 30, 180, 140)},
            {'name': 'Kitchen', 'bounds': (190, 30, 280, 100)},
            {'name': 'Bedroom', 'bounds': (30, 150, 140, 230)},
            {'name': 'Bathroom', 'bounds': (150, 150, 220, 200)},
            {'name': 'Entrance', 'bounds': (290, 30, 370, 80)},
        ]
    
    def create_canvas(self) -> tk.Canvas:
        if self._canvas is None:
            self._canvas = tk.Canvas(self._parent, width=self._width, 
                                    height=self._height, bg='#F5F5F5',
                                    highlightthickness=1, highlightbackground='#BDBDBD')
            self._draw()
        return self._canvas
    
    def _draw(self) -> None:
        if not self._canvas:
            return
        self._canvas.delete('all')
        self._draw_rooms()
        for device in self._devices.values():
            device.draw(self._canvas)
    
    def _draw_rooms(self) -> None:
        for room in self._rooms:
            x1, y1, x2, y2 = room['bounds']
            self._canvas.create_rectangle(x1, y1, x2, y2, fill='white', 
                                         outline='#424242', width=2)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            self._canvas.create_text(cx, cy, text=room['name'], 
                                    font=('Arial', 8), fill='#757575')
    
    def add_device(self, device: DeviceIcon) -> None:
        self._devices[device.device_id] = device
        if self._on_device_click:
            device.set_click_handler(self._on_device_click)
        if self._canvas:
            device.draw(self._canvas)
    
    def remove_device(self, device_id: str) -> None:
        if device_id in self._devices:
            self._devices.pop(device_id)
            if self._canvas:
                self._canvas.delete(f'device_{device_id}')
    
    def get_device(self, device_id: str) -> Optional[DeviceIcon]:
        return self._devices.get(device_id)
    
    def get_all_devices(self) -> List[DeviceIcon]:
        return list(self._devices.values())
    
    def set_device_click_handler(self, handler: Callable[[DeviceIcon], None]) -> None:
        self._on_device_click = handler
        for device in self._devices.values():
            device.set_click_handler(handler)
    
    def refresh(self) -> None:
        self._draw()
    
    def highlight_devices(self, device_ids: List[str]) -> None:
        for device_id, device in self._devices.items():
            device.is_active = device_id in device_ids
        self.refresh()
    
    def load_devices_from_list(self, devices: List[Dict]) -> None:
        self._devices.clear()
        positions = [(100, 50), (50, 100), (180, 50), (250, 60),
                    (80, 180), (180, 170), (330, 50), (330, 100)]
        
        for i, data in enumerate(devices):
            if 'x' not in data:
                pos = positions[i] if i < len(positions) else (100 + i * 30, 100)
                data['x'], data['y'] = pos
            device = DeviceIcon.from_dict(data)
            self.add_device(device)
