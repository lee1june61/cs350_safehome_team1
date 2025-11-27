"""Floor plan interaction controller."""

from typing import Callable, Optional
from ..models.device_icon import DeviceIcon
from ..services.device_service import DeviceService
from ..views.floor_plan_canvas import FloorPlanCanvas


class FloorPlanController:
    """Controller for floor plan interactions.

    Handles mouse events and device interactions on floor plan.
    """

    def __init__(
        self, floor_plan_canvas: FloorPlanCanvas, device_service: DeviceService
    ):
        """Initialize floor plan controller.

        Args:
            floor_plan_canvas: Floor plan canvas view
            device_service: Device service
        """
        self.canvas = floor_plan_canvas
        self.device_service = device_service

        # State
        self._hovered_device: Optional[DeviceIcon] = None
        self._zone_creation_mode = False

        # Callbacks
        self.on_device_click: Optional[Callable[[DeviceIcon], None]] = None
        self.on_sensor_selected: Optional[Callable[[DeviceIcon], None]] = None

        # Bind events
        self.canvas.on_click = self._handle_click
        self.canvas.on_motion = self._handle_motion
        self.canvas.on_leave = self._handle_leave

    def draw(self):
        """Draw floor plan with all devices."""
        devices = self.device_service.get_all_devices()
        self.canvas.draw(devices)

    def set_zone_creation_mode(self, enabled: bool):
        """Enable or disable zone creation mode.

        Args:
            enabled: True to enable zone creation mode
        """
        self._zone_creation_mode = enabled
        if not enabled:
            # Clear all selections
            for device in self.device_service.get_all_devices():
                device.is_selected = False
            self.draw()

    def toggle_sensor_selection(self, device: DeviceIcon):
        """Toggle sensor selection for zone creation.

        Args:
            device: Device to toggle
        """
        device.is_selected = not device.is_selected
        self.draw()

        if self.on_sensor_selected:
            self.on_sensor_selected(device)

    def _handle_click(self, event):
        """Handle mouse click on canvas.

        Args:
            event: Mouse event
        """
        device = self.device_service.find_device_at_position(event.x, event.y)

        if device:
            if self._zone_creation_mode:
                # In zone creation mode, toggle sensor selection
                if device.is_sensor:
                    self.toggle_sensor_selection(device)
            else:
                # Normal mode, show device detail
                if self.on_device_click:
                    self.on_device_click(device)

    def _handle_motion(self, event):
        """Handle mouse motion on canvas.

        Args:
            event: Mouse event
        """
        device = self.device_service.find_device_at_position(event.x, event.y)

        if device != self._hovered_device:
            # Unhover previous device
            if self._hovered_device:
                self._hovered_device.is_hovered = False

            # Hover new device
            if device:
                device.is_hovered = True
                self.canvas.canvas.config(cursor="hand2")
            else:
                self.canvas.canvas.config(cursor="")

            self._hovered_device = device
            self.draw()

    def _handle_leave(self, event):
        """Handle mouse leaving canvas.

        Args:
            event: Mouse event
        """
        if self._hovered_device:
            self._hovered_device.is_hovered = False
            self._hovered_device = None
            self.canvas.canvas.config(cursor="")
            self.draw()
