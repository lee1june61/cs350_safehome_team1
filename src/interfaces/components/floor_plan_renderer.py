"""Floor plan rendering utilities."""

import tkinter as tk

from .rendering.image_loader import load_floorplan_image
from .rendering.fallback_drawing import draw_fallback_layout
from .rendering.device_icon import draw_device_icon

load_image = load_floorplan_image
draw_fallback = draw_fallback_layout
draw_device = draw_device_icon
