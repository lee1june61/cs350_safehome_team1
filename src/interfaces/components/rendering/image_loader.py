"""Image loading utilities for the floor plan."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Optional

from src.resources import get_image

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:  # pragma: no cover
    HAS_PIL = False


def find_floorplan_image() -> Optional[Path]:
    """Locate the floorplan image on disk."""
    candidates = [
        get_image("floorplan.png"),
        Path.cwd() / "src" / "resources" / "images" / "floorplan.png",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def load_floorplan_image(canvas: tk.Canvas, width: int, height: int):
    """Draw the floorplan image (607x373) or fallback layout if unavailable."""
    img_path = find_floorplan_image()
    if not HAS_PIL or not img_path:
        from .fallback_drawing import draw_fallback_layout

        draw_fallback_layout(canvas, width, height)
        return None

    try:
        img = Image.open(img_path)
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        return photo, 0, 0, 1.0, 1.0
    except Exception:  # pragma: no cover - fallback path
        from .fallback_drawing import draw_fallback_layout

        draw_fallback_layout(canvas, width, height)
        return None






