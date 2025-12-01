"""Device icon drawing helpers."""

from __future__ import annotations

import tkinter as tk
from typing import Callable

from ...utils import sensor_display_name
from ..floor_plan_data import DEVICE_COLORS


def draw_device_icon(
    canvas: tk.Canvas,
    device_id: str,
    x: int,
    y: int,
    device_type: str,
    armed: bool,
    selected: bool,
    click_handler: Callable[[str, str], None],
) -> None:
    """Draw sensor icon with state colors and click binding."""
    radius = 10
    fill_color = DEVICE_COLORS.get(device_type, "#666")

    if selected:
        outline, line_width = "#f39c12", 3
    elif armed:
        outline, line_width = "#27ae60", 3
    else:
        outline, line_width = "#333", 2

    tag = f"d_{device_id}"
    canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill=fill_color,
        outline=outline,
        width=line_width,
        tags=(tag, "device", device_type),
    )
    canvas.create_text(
        x,
        y + 16,
        text=sensor_display_name(device_id, device_type),
        font=("Arial", 9, "bold"),
        fill="#333",
        tags=(f"lbl_{device_id}",),
    )
    canvas.tag_bind(
        tag,
        "<Button-1>",
        lambda event, dev=device_id, dtype=device_type: click_handler(dev, dtype),
    )

