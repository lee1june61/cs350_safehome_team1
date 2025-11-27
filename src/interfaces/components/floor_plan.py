"""
FloorPlan - Contains and displays the house blueprint

Single Responsibility: Manage floor plan display and devices.
"""
import tkinter as tk
from typing import List, Dict, Optional, Callable

from .device_icon import DeviceIcon
from .device_position import DevicePosition
from .device_renderer import DeviceRenderer
from .room_renderer import RoomRenderer, DEFAULT_ROOMS


class FloorPlan:
    """Manages and displays house floor plan with device icons"""
    
    def __init__(self, parent: tk.Widget, width: int = 400, height: int = 300):
        self._parent = parent
        self._width = width
        self._height = height
        self._canvas: Optional[tk.Canvas] = None
        self._devices: Dict[str, DeviceIcon] = {}
        self._on_device_click: Optional[Callable] = None
        self._rooms = DEFAULT_ROOMS
    
    def create_canvas(self) -> tk.Canvas:
        """Create and return the floor plan canvas"""
        if self._canvas is None:
            self._canvas = tk.Canvas(
                self._parent, width=self._width, height=self._height,
                bg='#F5F5F5', highlightthickness=1, highlightbackground='#BDBDBD'
            )
            self._draw()
        return self._canvas
    
    def _draw(self) -> None:
        """Redraw entire floor plan"""
        if not self._canvas:
            return
        self._canvas.delete('all')
        RoomRenderer.draw_rooms(self._canvas, self._rooms)
        self._draw_devices()
    
    def _draw_devices(self) -> None:
        """Draw all device icons"""
        for device in self._devices.values():
            DeviceRenderer.draw(device, self._canvas)
            if self._on_device_click:
                DeviceRenderer.bind_click(device, self._canvas, self._on_device_click)
    
    def add_device(self, device: DeviceIcon) -> None:
        """Add device to floor plan"""
        self._devices[device.device_id] = device
        if self._canvas:
            DeviceRenderer.draw(device, self._canvas)
            if self._on_device_click:
                DeviceRenderer.bind_click(device, self._canvas, self._on_device_click)
    
    def remove_device(self, device_id: str) -> None:
        """Remove device from floor plan"""
        if device_id in self._devices:
            self._devices.pop(device_id)
            if self._canvas:
                self._canvas.delete(f'device_{device_id}')
    
    def get_device(self, device_id: str) -> Optional[DeviceIcon]:
        return self._devices.get(device_id)
    
    def get_all_devices(self) -> List[DeviceIcon]:
        return list(self._devices.values())
    
    def set_device_click_handler(self, handler: Callable) -> None:
        self._on_device_click = handler
    
    def refresh(self) -> None:
        self._draw()
    
    def highlight_devices(self, device_ids: List[str]) -> None:
        """Highlight specific devices"""
        for device_id, device in self._devices.items():
            device.is_active = device_id in device_ids
        self.refresh()
    
    def load_devices_from_list(self, devices: List[Dict]) -> None:
        """Load devices from list of dictionaries"""
        self._devices.clear()
        for i, data in enumerate(devices):
            if 'x' not in data:
                data['x'] = 100 + (i % 4) * 80
                data['y'] = 80 + (i // 4) * 80
            self.add_device(DeviceIcon.from_dict(data))
