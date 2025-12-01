"""FloorPlan - House blueprint with clickable devices (SDS: FloorPlan class)"""

import tkinter as tk
from typing import Dict, Optional, Callable, Set
from .floor_plan_data import DEVICES
from .floor_plan_renderer import load_image, draw_device
from .floor_plan_selection import FloorPlanSelectionMixin


class FloorPlan(FloorPlanSelectionMixin):
    """Floor plan with clickable device icons."""

    ORIGINAL_IMG_WIDTH = 607
    ORIGINAL_IMG_HEIGHT = 373

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
        self._show_cameras, self._show_sensors = show_cameras, show_sensors
        self._select_mode = False
        self._device_positions: Dict[str, tuple[int, int, str]] = {}
        self._drag_start, self._drag_rect, self._drag_bound = None, None, False
        self._img_x_off, self._img_y_off = 0, 0
        self._img_scale_x, self._img_scale_y = 1.0, 1.0

    def create(self) -> tk.Canvas:
        canvas_width = max(self._w, self.ORIGINAL_IMG_WIDTH)
        canvas_height = max(self._h, self.ORIGINAL_IMG_HEIGHT)
        self._canvas = tk.Canvas(self._parent, width=canvas_width, height=canvas_height,
                                 bg="#f0f0f0", highlightthickness=1, highlightbackground="#ccc")
        self._draw()
        self._bind_drag_events()
        return self._canvas

    def _draw(self):
        if not self._canvas:
            return
        self._canvas.delete("all")
        result = load_image(self._canvas, self._w, self._h)
        if result and isinstance(result, tuple) and len(result) == 5:
            self._photo, self._img_x_off, self._img_y_off, self._img_scale_x, self._img_scale_y = result
        else:
            self._photo = result if result else None
            self._img_x_off, self._img_y_off, self._img_scale_x, self._img_scale_y = 0, 0, 1.0, 1.0
        self._draw_devices()

    def _draw_devices(self):
        self._device_positions.clear()
        for dev_id, (nx, ny, dtype) in DEVICES.items():
            if dtype == "camera" and not self._show_cameras:
                continue
            if dtype in ("sensor", "motion", "door_sensor") and not self._show_sensors:
                continue
            orig_x, orig_y = nx * self.ORIGINAL_IMG_WIDTH, ny * self.ORIGINAL_IMG_HEIGHT
            x = int(self._img_x_off + orig_x * self._img_scale_x)
            y = int(self._img_y_off + orig_y * self._img_scale_y)
            armed, selected = self._states.get(dev_id, False), dev_id in self._selected
            self._device_positions[dev_id] = (x, y, dtype)
            draw_device(self._canvas, dev_id, x, y, dtype, armed, selected, self._handle_click)

    def _handle_click(self, dev_id: str, dtype: str):
        if self._select_mode and dtype in ("sensor", "motion", "door_sensor"):
            self._selected.discard(dev_id) if dev_id in self._selected else self._selected.add(dev_id)
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
            self._clear_drag_visual()
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
        return [d for d, (_, _, t) in DEVICES.items() if t == dtype] if dtype else list(DEVICES.keys())

    def get_sensors(self) -> list:
        return [d for d, (_, _, t) in DEVICES.items() if t in ("sensor", "motion", "door_sensor")]
