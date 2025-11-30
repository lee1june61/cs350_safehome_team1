"""SafeHomeControlPanel - Main control panel class."""

from typing import TYPE_CHECKING
from src.devices.device_control_panel_abstract import DeviceControlPanelAbstract
from .button_mixin import ButtonMixin
from .handlers import (
    AlarmHandler,
    DisplayHandler,
    PasswordHandler,
    SystemHandler,
    StateTransitions,
    SecurityActions,
)

if TYPE_CHECKING:
    from src.core.system import System


class SafeHomeControlPanel(ButtonMixin, DeviceControlPanelAbstract):
    """SafeHome Control Panel - SRS V.1.a, V.1.d-g, V.2.a, V.2.d, V.2.k."""

    STATE_OFF = "off"
    STATE_BOOTING = "booting"
    STATE_IDLE = "idle"
    STATE_LOGGED_IN = "logged_in"
    STATE_CHANGING_PW = "changing_pw"
    STATE_LOCKED = "locked"
    STATE_ALARM = "alarm"
    STATE_PANIC_VERIFY = "panic_verify"

    def __init__(self, master, system: "System"):
        super().__init__(master)
        self._system = system
        self._state = self.STATE_OFF
        self._display = DisplayHandler(self)
        self._password = PasswordHandler(self)
        self._system_ctrl = SystemHandler(self)
        self._alarm = AlarmHandler(self)
        self._transitions = StateTransitions(self)
        self._security = SecurityActions(self)
        self._display.init_off_display()
        self._apply_security_policy()
        self._panic_prev_state = None
        self._panic_lock_id = None
        self._panic_lock_seconds = 0
        self._panic_lock_message = ""
        self._panic_locked = False

    @property
    def is_off(self) -> bool:
        return self._state == self.STATE_OFF

    @property
    def current_state(self) -> str:
        return self._state

    def send_request(self, cmd: str, **kw) -> dict:
        if not self._system:
            return {"success": False, "message": "System not connected"}
        return self._system.handle_request("control_panel", cmd, **kw)

    def send_command(self, cmd: str, **kw) -> dict:
        return self.send_request(cmd, **kw)

    def restore_state(self, state: str):
        self._state = state
        if state == self.STATE_LOGGED_IN:
            self._display.show_welcome(self._password.access_level)
        elif state == self.STATE_IDLE:
            self._display.show_idle()
        self._update_leds()

    def _update_leds(self):
        res = self._system_ctrl.get_status()
        if res.get("success"):
            self._display.update_leds_from_status(res.get("data", {}))

    def handle_alarm_event(self, data: dict):
        self._alarm.handle_event(data)

    def _apply_security_policy(self):
        """Sync password attempts/lock duration with system settings."""
        try:
            res = self.send_request("get_system_settings")
        except Exception:
            return
        if not isinstance(res, dict) or not res.get("success"):
            return
        data = res.get("data", {})
        attempts = data.get("max_login_attempts")
        lock_time = data.get("system_lock_time")
        self._password.configure_policy(
            max_attempts=int(attempts) if attempts else None,
            lock_time_seconds=int(lock_time) if lock_time else None,
        )

    def enter_panic_verification(self):
        """Prompt user for master password to cancel panic."""
        self._panic_prev_state = self._state if self._state != self.STATE_PANIC_VERIFY else self._panic_prev_state
        self._state = self.STATE_PANIC_VERIFY
        self._panic_locked = False
        self._password.clear_buffer()
        self.set_display_short_message1("PANIC MODE")
        self.set_display_short_message2("Enter master password")

    def exit_panic_verification(self):
        """Return to previous state after panic process."""
        self._clear_panic_lock_timer()
        self._panic_locked = False
        self._state = self._panic_prev_state or self.STATE_IDLE
        self._panic_prev_state = None
        self._password.clear_buffer()
        if self._state == self.STATE_IDLE:
            self._display.show_idle()
        elif self._state == self.STATE_LOGGED_IN:
            self._display.show_welcome(self._password.access_level)

    def show_panic_lock(self, message: str, seconds: int):
        self._panic_locked = True
        self._panic_lock_message = message or "Locked"
        self._panic_lock_seconds = max(seconds, 0)
        self._update_panic_lock_display()
        self._schedule_panic_lock_tick()

    def _update_panic_lock_display(self):
        timer_text = (
            f"{self._panic_lock_seconds}s remaining" if self._panic_lock_seconds > 0 else ""
        )
        self.set_display_short_message1(self._panic_lock_message[:16])
        self.set_display_short_message2(timer_text[:16])

    def _schedule_panic_lock_tick(self):
        self._clear_panic_lock_timer()
        if self._panic_lock_seconds <= 0:
            self.exit_panic_verification()
            return
        self._panic_lock_id = self.after(1000, self._tick_panic_lock)

    def _tick_panic_lock(self):
        self._panic_lock_seconds -= 1
        self._update_panic_lock_display()
        if self._panic_lock_seconds <= 0:
            self.exit_panic_verification()
        else:
            self._panic_lock_id = self.after(1000, self._tick_panic_lock)

    def _clear_panic_lock_timer(self):
        if self._panic_lock_id:
            self.after_cancel(self._panic_lock_id)
            self._panic_lock_id = None


def run_control_panel(system: "System", master=None) -> SafeHomeControlPanel:
    return SafeHomeControlPanel(master, system)
