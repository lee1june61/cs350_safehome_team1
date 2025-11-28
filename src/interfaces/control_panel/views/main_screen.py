"""Main functions screen view."""

import tkinter as tk
from .base_screen import BaseScreen
from .floor_plan_canvas import FloorPlanCanvas
from .control_panel_buttons import ControlPanelButtons
from ..config.ui_config import UIConfig


class MainScreen(BaseScreen):
    """Main functions screen with floor plan and controls.

    Following the WebInterface and Page hierarchy from SDS.
    """

    def __init__(self, parent: tk.Widget, username: str, on_logout):
        """Initialize main screen.

        Args:
            parent: Parent widget
            username: Logged in username
            on_logout: Callback for logout
        """
        super().__init__(parent)
        self.username = username
        self.on_logout = on_logout

        # Sub-components
        self.floor_plan_canvas: FloorPlanCanvas = None
        self.control_buttons: ControlPanelButtons = None
        self.status_label: tk.Label = None

    def build(self) -> tk.Frame:
        """Build main screen."""
        frame = tk.Frame(self.parent, bg=UIConfig.COLOR_WHITE)

        # Header
        self._create_header(frame)

        # Main content
        content = tk.Frame(frame, bg=UIConfig.COLOR_WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left: Floor plan
        left_panel = self._create_floor_plan_panel(content)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Right: Control buttons
        right_panel = self._create_control_panel(content)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        # Status bar
        self._create_status_bar(frame)

        return frame

    def _create_header(self, parent: tk.Frame):
        """Create header with title and logout."""
        header = tk.Frame(parent, bg=UIConfig.COLOR_PRIMARY, height=50)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="SafeHome Security System",
            font=UIConfig.FONT_HEADER,
            fg=UIConfig.COLOR_WHITE,
            bg=UIConfig.COLOR_PRIMARY,
        ).pack(side=tk.LEFT, padx=15, pady=8)

        tk.Label(
            header,
            text=f"👤 {self.username}",
            font=UIConfig.FONT_LABEL,
            fg=UIConfig.COLOR_WHITE,
            bg=UIConfig.COLOR_PRIMARY,
        ).pack(side=tk.LEFT)

        tk.Button(
            header, text="Logout", font=("Arial", 9), command=self.on_logout
        ).pack(side=tk.RIGHT, padx=15)

    def _create_floor_plan_panel(self, parent: tk.Frame) -> tk.LabelFrame:
        """Create floor plan panel.

        Returns:
            LabelFrame containing floor plan
        """
        panel = tk.LabelFrame(
            parent,
            text="🏠 Floor Plan - Click devices to control",
            font=("Arial", 10, "bold"),
        )

        # Legend
        legend = tk.Frame(panel, bg=UIConfig.COLOR_LIGHT_BLUE, height=25)
        legend.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            legend,
            text="🔴 Armed  ⚪ Disarmed  |  🟥 Window/Door  🟦 Motion  🟢 Camera",
            font=UIConfig.FONT_LABEL_SMALL,
            bg=UIConfig.COLOR_LIGHT_BLUE,
        ).pack()

        # Floor plan canvas
        self.floor_plan_canvas = FloorPlanCanvas(
            panel, UIConfig.CANVAS_WIDTH, UIConfig.CANVAS_HEIGHT
        )
        canvas = self.floor_plan_canvas.create()
        canvas.pack(padx=5, pady=5)

        return panel

    def _create_control_panel(self, parent: tk.Frame) -> tk.Frame:
        """Create control buttons panel.

        Returns:
            Frame containing control buttons
        """
        self.control_buttons = ControlPanelButtons(parent)
        return self.control_buttons.create()

    def _create_status_bar(self, parent: tk.Frame):
        """Create status bar at bottom."""
        status_bar = tk.Frame(parent, bg="#e0e0e0", height=22)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            status_bar, text="Ready", font=UIConfig.FONT_LABEL_SMALL, bg="#e0e0e0"
        )
        self.status_label.pack(side=tk.LEFT, padx=8)

    def update_status(self, text: str):
        """Update status bar text.

        Args:
            text: Status text to display
        """
        if self.status_label:
            self.status_label.config(text=text)
