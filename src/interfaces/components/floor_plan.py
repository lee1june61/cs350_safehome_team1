"""FloorPlan - House blueprint with clickable devices (SDS: FloorPlan class)"""

import tkinter as tk
from typing import Dict, Optional, Callable, Set
from .floor_plan_data import DEVICES
from .floor_plan_renderer import load_image, draw_device


class FloorPlan:
    """Floor plan with clickable device icons."""

    def __init__(
        self,
        parent: tk.Widget,
        width: int = 450,
        height: int = 280,
        show_cameras: bool = True,
        show_sensors: bool = True,
    ):
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
        self._device_positions: Dict[str, tuple[int, int, str]] = {}
        self._drag_start: Optional[tuple[int, int]] = None
        self._drag_rect: Optional[int] = None
        self._drag_bound = False
        # Image transformation parameters
        self._img_x_off = 0
        self._img_y_off = 0
        self._img_scale_x = 1.0
        self._img_scale_y = 1.0

    def create(self) -> tk.Canvas:
        # Fixed image size: 607x373
        # Canvas should be at least this size to display the image without clipping
        FIXED_IMG_WIDTH = 607
        FIXED_IMG_HEIGHT = 373
        canvas_width = max(self._w, FIXED_IMG_WIDTH)
        canvas_height = max(self._h, FIXED_IMG_HEIGHT)

        self._canvas = tk.Canvas(
            self._parent,
            width=canvas_width,
            height=canvas_height,
            bg="#f0f0f0",
            highlightthickness=1,
            highlightbackground="#ccc",
        )
        self._draw()
        self._bind_drag_events()
        return self._canvas

    def _draw(self):
        if not self._canvas:
            return
        self._canvas.delete("all")
        result = load_image(self._canvas, self._w, self._h)
        if result and isinstance(result, tuple) and len(result) == 5:
            (
                self._photo,
                self._img_x_off,
                self._img_y_off,
                self._img_scale_x,
                self._img_scale_y,
            ) = result
        else:
            self._photo = result if result else None
            # Fallback: assume image fills canvas (no scaling/offset)
            self._img_x_off, self._img_y_off = 0, 0
            self._img_scale_x, self._img_scale_y = 1.0, 1.0
        self._draw_devices()

    def _draw_devices(self):
        # Original image dimensions (607x373) - fixed size
        ORIGINAL_IMG_WIDTH = 607
        ORIGINAL_IMG_HEIGHT = 373

        self._device_positions.clear()
        for dev_id, (nx, ny, dtype) in DEVICES.items():
            if dtype == "camera" and not self._show_cameras:
                continue
            if dtype in ("sensor", "motion", "door_sensor") and not self._show_sensors:
                continue

            # Convert normalized coordinates (0-1) to pixel coordinates
            # Since image is displayed at fixed size (607x373), we can use coordinates directly
            orig_x = nx * ORIGINAL_IMG_WIDTH
            orig_y = ny * ORIGINAL_IMG_HEIGHT

            # Apply offset and scale (should be 0, 0, 1.0, 1.0 for fixed-size image)
            x = int(self._img_x_off + orig_x * self._img_scale_x)
            y = int(self._img_y_off + orig_y * self._img_scale_y)

            armed = self._states.get(dev_id, False)
            selected = dev_id in self._selected
            self._device_positions[dev_id] = (x, y, dtype)
            draw_device(
                self._canvas, dev_id, x, y, dtype, armed, selected, self._handle_click
            )

    def _handle_click(self, dev_id: str, dtype: str):
        if self._select_mode and dtype in ("sensor", "motion", "door_sensor"):
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
        if dtype:
            return [d for d, (_, _, t) in DEVICES.items() if t == dtype]
        return list(DEVICES.keys())

    def get_sensors(self) -> list:
        return [
            d
            for d, (_, _, t) in DEVICES.items()
            if t in ("sensor", "motion", "door_sensor")
        ]

    def _bind_drag_events(self):
        if self._drag_bound or not self._canvas:
            return
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self._canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self._drag_bound = True

    def _canvas_coords(self, event):
        if not self._canvas:
            return event.x, event.y
        return self._canvas.canvasx(event.x), self._canvas.canvasy(event.y)

    def _on_mouse_down(self, event):
        if not self._select_mode or not self._canvas:
            return
        self._drag_start = self._canvas_coords(event)
        self._clear_drag_visual()

    def _on_mouse_drag(self, event):
        if not self._select_mode or not self._canvas or not self._drag_start:
            return
        x0, y0 = self._drag_start
        x1, y1 = self._canvas_coords(event)
        self._clear_drag_visual()
        self._drag_rect = self._canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            outline="#2980b9",
            dash=(4, 2),
            width=1,
        )

    def _on_mouse_up(self, event):
        if not self._select_mode or not self._canvas or not self._drag_start:
            self._clear_drag_visual()
            self._drag_start = None
            return
        x0, y0 = self._drag_start
        x1, y1 = self._canvas_coords(event)
        self._drag_start = None
        self._clear_drag_visual()
        if abs(x0 - x1) < 5 and abs(y0 - y1) < 5:
            return
        self._select_sensors_in_box(x0, y0, x1, y1)

    def _clear_drag_visual(self):
        if self._canvas and self._drag_rect:
            self._canvas.delete(self._drag_rect)
        self._drag_rect = None

    def _select_sensors_in_box(self, x0: float, y0: float, x1: float, y1: float):
        min_x, max_x = sorted([x0, x1])
        min_y, max_y = sorted([y0, y1])
        newly_added = []
        for dev_id, (dx, dy, dtype) in self._device_positions.items():
            if dtype not in ("sensor", "motion", "door_sensor"):
                continue
            if min_x <= dx <= max_x and min_y <= dy <= max_y:
                if dev_id not in self._selected:
                    self._selected.add(dev_id)
                    newly_added.append((dev_id, dtype))
        if newly_added:
            self.refresh()
            if self._on_sensor_click:
                for dev_id, dtype in newly_added:
                    self._on_sensor_click(dev_id, dtype, True)
