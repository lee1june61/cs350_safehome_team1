"""Alarm handler for control panel - SRS V.2.d."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class AlarmHandler:
    """Handles alarm polling and display."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel
        self._alarm_active = False
        self._poll_job: Optional[int] = None
        self._previous_state: Optional[str] = None

    @property
    def is_active(self) -> bool:
        return self._alarm_active

    def start_polling(self):
        """Start periodic alarm status polling."""
        self._poll()

    def stop_polling(self):
        """Stop alarm polling."""
        if self._poll_job:
            self._panel.after_cancel(self._poll_job)
            self._poll_job = None
        self._alarm_active = False

    def _poll(self):
        """Poll system for alarm condition."""
        if self._panel.is_off:
            return

        res = self._panel.send_request("get_alarm_status")
        if res.get("success"):
            data = res.get("data", {})
            is_alarm = data.get("alarm_active", False)
            if is_alarm and not self._alarm_active:
                self._trigger(data)
            elif not is_alarm and self._alarm_active:
                self._clear()

        self._poll_job = self._panel.after(1000, self._poll)

    def _trigger(self, data: dict):
        """Trigger alarm display."""
        self._alarm_active = True
        self._previous_state = self._panel.current_state

        sensor_id = data.get("sensor_id", "Unknown")
        zone_name = data.get("zone_name", "Unknown")
        alarm_type = data.get("alarm_type", "INTRUSION")

        self._panel.set_display_short_message1(f"!ALARM! {alarm_type}")
        self._panel.set_display_short_message2(f"{sensor_id} @ {zone_name}"[:20])
        self._panel.set_armed_led(True)
        self._panel.set_display_not_ready(True)

    def _clear(self):
        """Clear alarm display."""
        self._alarm_active = False
        self._panel.set_display_not_ready(False)
        if self._previous_state:
            self._panel.restore_state(self._previous_state)

    def handle_event(self, data: dict):
        """Handle external alarm event."""
        if data.get("alarm_active", False):
            self._trigger(data)
        else:
            self._clear()







