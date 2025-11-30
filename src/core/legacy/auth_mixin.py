"""Legacy authentication methods for backward compatibility."""

from __future__ import annotations


class LegacyAuthMixin:
    """Provides legacy auth APIs required by older unit tests."""

    def authenticate_user(self, username, password, interface):
        if self.is_locked:
            return None
        result = None
        if hasattr(self.login_manager, "authenticate"):
            result = self.login_manager.authenticate(username, password, interface)
        if result:
            self.is_authenticated = True
            self.access_level = result
            self.login_tries = 0
            self.is_locked = False
            return result
        self.login_tries += 1
        if self.login_tries >= 3:
            self.is_locked = True
        return None

    def make_panic_phone_call(self) -> bool:
        phone = None
        if hasattr(self.config_manager, "get_monitoring_phone"):
            phone = self.config_manager.get_monitoring_phone()
        if not phone:
            phone = self.settings_service.get_settings().monitoring_service_phone
        if not phone:
            return False
        alarm_ringing = False
        if hasattr(self.alarm, "is_ringing"):
            alarm_ringing = bool(self.alarm.is_ringing())
        if alarm_ringing:
            self.security_handler.panic()
        return True

    def reset(self) -> bool:
        self.status = "OFF"
        self.login_tries = 0
        self.access_level = None
        self.is_authenticated = False
        if hasattr(self.config_manager, "reset_to_default"):
            self.config_manager.reset_to_default()
        if hasattr(self.sensor_controller, "disarm_all_sensors"):
            self.sensor_controller.disarm_all_sensors()
        if hasattr(self.camera_controller, "disable_all_camera"):
            self.camera_controller.disable_all_camera()
        return True

