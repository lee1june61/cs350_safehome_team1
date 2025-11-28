"""FloorPlan - House blueprint with clickable devices (SDS: FloorPlan class)"""
import tkinter as tk
from typing import Dict, Optional, Callable, Set
from .floor_plan_data import DEVICES
from .floor_plan_renderer import load_image, draw_device


class FloorPlan:
    """Floor plan with clickable device icons."""

    def __init__(self, parent: tk.Widget, width: int = 450, height: int = 280,
                 show_cameras: bool = True, show_sensors: bool = True):
        self._parent = parent
        self._w, self._h = width, height
        self._canvas: Optional[tk.Canvas] = None
        self._photo = None
        self._on_click: Optional[Callable] = None
        self._on_sensor_click: Optional[Callable] = None
        self._states: Dict[str, bool] = {}
        self._selected: Set[str] = set()
        self._show_cameras = show_cameras
        self._show_sensors = show_sensors
        self._select_mode = False

    def create(self) -> tk.Canvas:
        self._canvas = tk.Canvas(
            self._parent, width=self._w, height=self._h,
            bg='#f0f0f0', highlightthickness=1, highlightbackground='#ccc')
        self._draw()
        return self._canvas

    def _draw(self):
        if not self._canvas:
            return
        self._canvas.delete('all')
        self._photo = load_image(self._canvas, self._w, self._h)
        self._draw_devices()

    def _draw_devices(self):
        for dev_id, (nx, ny, dtype) in DEVICES.items():
            if dtype == 'camera' and not self._show_cameras:
                continue
            if dtype in ('sensor', 'motion') and not self._show_sensors:
                continue

            x, y = int(nx * self._w), int(ny * self._h)
            armed = self._states.get(dev_id, False)
            selected = dev_id in self._selected
            draw_device(self._canvas, dev_id, x, y, dtype,
                        armed, selected, self._handle_click)

    def _handle_click(self, dev_id: str, dtype: str):
        if self._select_mode and dtype in ('sensor', 'motion'):
            if dev_id in self._selected:
                self._selected.discard(dev_id)
            else:
                self._selected.add(dev_id)
            self.refresh()
            if self._on_sensor_click:
                self._on_sensor_click(dev_id, dtype, dev_id in self._selected)
        elif self._on_click:
            self._on_click(dev_id, dtype)

    def set_on_click(self, handler: Callable[[str, str], None]):
        self._on_click = handler

    def set_on_sensor_click(self, handler: Callable[[str, str, bool], None]):
        self._on_sensor_click = handler

    def set_select_mode(self, enabled: bool):
        self._select_mode = enabled
        if not enabled:
            self._selected.clear()
        self.refresh()

    def set_armed(self, device_id: str, armed: bool):
        self._states[device_id] = armed

    def set_selected(self, device_ids: list):
        self._selected = set(device_ids)
        self.refresh()

    def get_selected(self) -> list:
        return list(self._selected)

    def clear_selection(self):
        self._selected.clear()
        self.refresh()

    def refresh(self):
        self._draw()

    def get_devices(self, dtype: str = None) -> list:
        if dtype:
            return [d for d, (_, _, t) in DEVICES.items() if t == dtype]
        return list(DEVICES.keys())

    def get_sensors(self) -> list:
        return [d for d, (_, _, t) in DEVICES.items() if t in ('sensor', 'motion')]
