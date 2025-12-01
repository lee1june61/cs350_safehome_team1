"""Floor plan selection and drag handling."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Set, Tuple

if TYPE_CHECKING:
    import tkinter as tk


class FloorPlanSelectionMixin:
    """Handles selection and drag operations for floor plan."""

    _canvas: Optional["tk.Canvas"]
    _select_mode: bool
    _selected: Set[str]
    _device_positions: dict
    _on_sensor_click: Optional[Callable]
    _drag_start: Optional[Tuple[int, int]]
    _drag_rect: Optional[int]
    _drag_bound: bool

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
            x0, y0, x1, y1, outline="#2980b9", dash=(4, 2), width=1
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

