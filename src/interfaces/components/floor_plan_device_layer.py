"""Device layer rendering for FloorPlan."""

from __future__ import annotations

from typing import Callable, Dict, Tuple

import tkinter as tk

from .floor_plan_data import DEVICES
from .rendering.device_icon import draw_device_icon


class DeviceLayer:
    """Handles drawing devices and returning their positions."""

    def __init__(self, show_cameras: bool = True, show_sensors: bool = True):
        self._show_cameras = show_cameras
        self._show_sensors = show_sensors

    def render(
        self,
        canvas: tk.Canvas,
        offsets: Tuple[float, float],
        scale: Tuple[float, float],
        states: Dict[str, bool],
        selected: set[str],
        click_handler: Callable[[str, str], None],
    ) -> Dict[str, Tuple[int, int, str]]:
        """Draw devices and return {device_id: (x, y, dtype)} positions."""
        positions: Dict[str, Tuple[int, int, str]] = {}
        x_off, y_off = offsets
        scale_x, scale_y = scale

        for dev_id, (nx, ny, dtype) in DEVICES.items():
            if dtype == "camera" and not self._show_cameras:
                continue
            if dtype in ("sensor", "motion", "door_sensor") and not self._show_sensors:
                continue

            orig_x = nx * FloorPlanGeometry.ORIGINAL_IMG_WIDTH
            orig_y = ny * FloorPlanGeometry.ORIGINAL_IMG_HEIGHT
            x = int(x_off + orig_x * scale_x)
            y = int(y_off + orig_y * scale_y)
            armed = states.get(dev_id, False)
            is_selected = dev_id in selected
            draw_device_icon(canvas, dev_id, x, y, dtype, armed, is_selected, click_handler)
            positions[dev_id] = (x, y, dtype)
        return positions


class FloorPlanGeometry:
    """Namespace for shared geometry constants."""

    ORIGINAL_IMG_WIDTH = 607
    ORIGINAL_IMG_HEIGHT = 373






