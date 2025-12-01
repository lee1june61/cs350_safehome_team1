"""SafeHomeControlPanel - Main control panel class."""

from typing import TYPE_CHECKING
from src.devices.device_control_panel_abstract import DeviceControlPanelAbstract
from .button_mixin import ButtonMixin
from .panic_handler import PanicVerificationMixin
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


class SafeHomeControlPanel(
    ButtonMixin, PanicVerificationMixin, DeviceControlPanelAbstract
):
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
        try:
            res = self.send_request("get_system_settings")
        except Exception:
            return
        if not isinstance(res, dict) or not res.get("success"):
            return
        data = res.get("data", {})
        attempts, lock_time = data.get("max_login_attempts"), data.get(
            "system_lock_time"
        )
        self._password.configure_policy(
            max_attempts=int(attempts) if attempts else None,
            lock_time_seconds=int(lock_time) if lock_time else None,
        )


def run_control_panel(system: "System", master=None) -> SafeHomeControlPanel:
    return SafeHomeControlPanel(master, system)
