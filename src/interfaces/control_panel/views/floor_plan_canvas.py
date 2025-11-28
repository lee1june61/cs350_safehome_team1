"""Floor plan canvas view."""

import tkinter as tk
from typing import List, Optional, Callable
from ..models.device_icon import DeviceIcon
from ..config.ui_config import UIConfig


class FloorPlanCanvas:
    """Canvas for displaying floor plan with devices.

    Following FloorPlan and DeviceIcon classes from SDS.
    """

    def __init__(self, parent: tk.Widget, width: int, height: int):
        """Initialize floor plan canvas.

        Args:
            parent: Parent widget
            width: Canvas width
            height: Canvas height
        """
        self.parent = parent
        self.width = width
        self.height = height
        self.canvas: Optional[tk.Canvas] = None
        self.floor_image = None
        self.floor_photo = None

        # Callbacks
        self.on_click: Optional[Callable] = None
        self.on_motion: Optional[Callable] = None
        self.on_leave: Optional[Callable] = None

    def create(self) -> tk.Canvas:
        """Create canvas widget.

        Returns:
            Canvas widget
        """
        self.canvas = tk.Canvas(
            self.parent,
            bg=UIConfig.CANVAS_BG,
            width=self.width,
            height=self.height,
            highlightthickness=1,
            highlightbackground="#999",
        )

        # Bind events
        if self.on_click:
            self.canvas.bind("<Button-1>", self.on_click)
        if self.on_motion:
            self.canvas.bind("<Motion>", self.on_motion)
        if self.on_leave:
            self.canvas.bind("<Leave>", self.on_leave)

        return self.canvas

    def set_floor_plan(self, image, photo):
        """Set floor plan image.

        Args:
            image: PIL Image object
            photo: ImageTk PhotoImage object
        """
        self.floor_image = image
        self.floor_photo = photo

    def draw(self, devices: List[DeviceIcon]):
        """Draw floor plan with devices.

        Args:
            devices: List of device icons to draw
        """
        if not self.canvas:
            return

        self.canvas.delete("all")

        # Draw floor plan background
        if self.floor_photo and self.floor_image:
            img_w, img_h = self.floor_image.size
            x_offset = (self.width - img_w) // 2
            y_offset = (self.height - img_h) // 2
            self.canvas.create_image(
                x_offset + img_w // 2, y_offset + img_h // 2, image=self.floor_photo
            )

        # Draw devices
        for device in devices:
            self._draw_device(device)

    def _draw_device(self, device: DeviceIcon):
        """Draw a single device icon.

        Args:
            device: Device to draw
        """
        x, y = device.x, device.y
        size = UIConfig.ICON_HOVER_SIZE if device.is_hovered else UIConfig.ICON_SIZE
        half = size // 2

        # Selection border
        if device.is_selected:
            self.canvas.create_rectangle(
                x - half - 4,
                y - half - 4,
                x + half + 4,
                y + half + 4,
                outline=UIConfig.COLOR_SELECTION,
                width=4,
            )

        # Draw based on device type
        if device.device_type == "window_door":
            self._draw_window_door_sensor(device, x, y, half)
        elif device.device_type == "motion":
            self._draw_motion_sensor(device, x, y, half)
        else:  # camera
            self._draw_camera(device, x, y, half)

        # Draw label
        self._draw_label(device, x, y, half)

    def _draw_window_door_sensor(self, device: DeviceIcon, x: int, y: int, half: int):
        """Draw window/door sensor as red square."""
        fill = (
            UIConfig.COLOR_SENSOR_ARMED
            if device.is_armed
            else UIConfig.COLOR_SENSOR_DISARMED
        )
        outline = (
            UIConfig.COLOR_SENSOR_ARMED_OUTLINE
            if device.is_armed
            else UIConfig.COLOR_SENSOR_DISARMED_OUTLINE
        )

        self.canvas.create_rectangle(
            x - half, y - half, x + half, y + half, fill=fill, outline=outline, width=3
        )

        self.canvas.create_text(
            x, y, text="S", font=("Arial", 10, "bold"), fill=UIConfig.COLOR_WHITE
        )

    def _draw_motion_sensor(self, device: DeviceIcon, x: int, y: int, half: int):
        """Draw motion sensor as blue square with M."""
        fill = (
            UIConfig.COLOR_MOTION_ARMED
            if device.is_armed
            else UIConfig.COLOR_MOTION_DISARMED
        )
        outline = (
            UIConfig.COLOR_MOTION_ARMED_OUTLINE
            if device.is_armed
            else UIConfig.COLOR_MOTION_DISARMED_OUTLINE
        )

        self.canvas.create_rectangle(
            x - half, y - half, x + half, y + half, fill=fill, outline=outline, width=3
        )

        self.canvas.create_text(
            x, y, text="M", font=("Arial", 11, "bold"), fill=UIConfig.COLOR_WHITE
        )

    def _draw_camera(self, device: DeviceIcon, x: int, y: int, half: int):
        """Draw camera as green circle."""
        fill = (
            UIConfig.COLOR_CAMERA_ENABLED
            if device.is_enabled
            else UIConfig.COLOR_CAMERA_DISABLED
        )
        outline = (
            UIConfig.COLOR_CAMERA_ENABLED_OUTLINE
            if device.is_enabled
            else UIConfig.COLOR_CAMERA_DISABLED_OUTLINE
        )

        self.canvas.create_oval(
            x - half, y - half, x + half, y + half, fill=fill, outline=outline, width=3
        )

        # Camera lens
        lens = half // 2
        self.canvas.create_oval(
            x - lens,
            y - lens,
            x + lens,
            y + lens,
            fill=UIConfig.COLOR_WHITE,
            outline=UIConfig.COLOR_BLACK,
            width=2,
        )

        self.canvas.create_text(
            x, y + 1, text="C", font=("Arial", 8, "bold"), fill=UIConfig.COLOR_BLACK
        )

    def _draw_label(self, device: DeviceIcon, x: int, y: int, half: int):
        """Draw device label with background."""
        label_y = y + half + 10

        # Create temporary text to get bounds
        temp = self.canvas.create_text(
            x, label_y, text=device.name, font=UIConfig.FONT_LABEL_SMALL
        )
        bbox = self.canvas.bbox(temp)
        self.canvas.delete(temp)

        # Draw background
        if bbox:
            self.canvas.create_rectangle(
                bbox[0] - 1,
                bbox[1] - 1,
                bbox[2] + 1,
                bbox[3] + 1,
                fill=UIConfig.COLOR_WHITE,
                outline=UIConfig.COLOR_BLACK,
                width=1,
            )

        # Draw label
        device.label_id = self.canvas.create_text(
            x,
            label_y,
            text=device.name,
            font=("Arial", 7, "bold"),
            fill=UIConfig.COLOR_BLACK,
        )
