"""System lifecycle methods."""

from __future__ import annotations


class SystemLifecycleMixin:
    """Provides turn_on/turn_off methods for System."""

    @property
    def _state(self):
        """Legacy alias for alarm_service.state (tests expect _state)."""
        return getattr(self.alarm_service, "state", self.status)

    @_state.setter
    def _state(self, value):
        """Allow setting _state for legacy tests."""
        if hasattr(self.alarm_service, "_state"):
            self.alarm_service._state = value
        self.status = value

    def turn_on(self):
        if getattr(self, "status", "OFF") == "ON":
            return False
        for ctrl in (self.config_manager, self.sensor_controller, self.camera_controller):
            if hasattr(ctrl, "initialize"):
                ctrl.initialize()
        self.alarm_service.turn_on()
        self.status = "ON"
        return True

    def turn_off(self):
        if not getattr(self, "is_authenticated", True):
            return False
        if hasattr(self.sensor_controller, "disarm_all_sensors"):
            self.sensor_controller.disarm_all_sensors()
        if hasattr(self.camera_controller, "disable_all_camera"):
            self.camera_controller.disable_all_camera()
        self.alarm_service.turn_off()
        self.mode_service.disarm_system(self.zone_service, log_event=False)
        self.auth_service.logout()
        self.status = "OFF"
        return True

    def _doors_open_flag(self) -> bool:
        return bool(getattr(self, "_doors_windows_open", False))

