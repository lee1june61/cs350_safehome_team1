"""Main page for Web Interface - WITH FLOOR PLAN (SRS V.2.b, V.3.a)"""
import tkinter as tk
from typing import Callable, Optional
from .main_page.header import create_header
from .main_page.status_bar import create_status_bar
from .main_page.control_panel import create_control_panel
from .main_page.floor_plan_canvas_ui import create_floor_plan_canvas_section
from .main_page.floor_plan_legend_ui import create_floor_plan_legend_section
from .main_page.floor_plan_instructions_ui import create_floor_plan_instructions_section
from .main_page.floor_plan_image_handler import FloorPlanImageHandler
from .main_page.device_renderer import DeviceRenderer


class MainPage:
    """Main web interface page with floor plan."""

    def __init__(
        self,
        parent: tk.Widget,
        username: str,
        on_device_click: Callable[[str, str], None],
        on_security: Callable[[], None],
        on_surveillance: Callable[[], None],
        on_settings: Callable[[], None],
        on_logout: Callable[[], None],
    ):
        self.parent = parent
        self.username = username
        self.on_device_click = on_device_click
        self.on_security = on_security
        self.on_surveillance = on_surveillance
        self.on_settings = on_settings
        self.on_logout = on_logout

        self.floor_plan_canvas: Optional[tk.Canvas] = None
        self.status_label: Optional[tk.Label] = None
        self.system_mode_label: Optional[tk.Label] = None
        self._device_renderer: Optional[DeviceRenderer] = None
        self._image_handler: Optional[FloorPlanImageHandler] = None

    def build(self) -> tk.Frame:
        frame = tk.Frame(self.parent, bg="#ffffff")

        # Header
        create_header(frame, self.username, self.on_logout)

        # Main content
        content = tk.Frame(frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Floor plan
        left_panel = self._create_floor_plan_panel(content)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right: Control panel
        right_panel, self.system_mode_label = create_control_panel(
            content, self.on_security, self.on_surveillance, self.on_settings)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # Status bar
        _, self.status_label = create_status_bar(frame)

        return frame

    def _create_floor_plan_panel(self, parent: tk.Frame) -> tk.LabelFrame:
        panel = tk.LabelFrame(
            parent,
            text="🏠 House Floor Plan - Click devices to control",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )

        create_floor_plan_legend_section(panel)

        self.floor_plan_canvas = create_floor_plan_canvas_section(
            panel, self._handle_canvas_click)

        self._image_handler = FloorPlanImageHandler(self.floor_plan_canvas)
        self._image_handler.draw_floor_plan(800, 600)

        self._device_renderer = DeviceRenderer(self.floor_plan_canvas)

        create_floor_plan_instructions_section(panel)

        return panel

    def _handle_canvas_click(self, event) -> None:
        if self._device_renderer:
            dtype, dev_id = self._device_renderer.get_device_at(
                event.x, event.y)
            if dtype and dev_id:
                self.on_device_click(dtype, dev_id)

    def add_device_icon(self, device_type: str, device_id: str,
                        x: int, y: int, armed: bool = False) -> None:
        if self._device_renderer:
            self._device_renderer.add_device_icon(
                device_type, device_id, x, y, armed)

    def update_status(self, message: str) -> None:
        if self.status_label:
            self.status_label.config(text=message)

    @property
    def device_items(self):
        if self._device_renderer:
            return self._device_renderer.device_items
        return {}
