"""Legacy helper mixin retained for backward compatibility tests."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class SystemLegacyMixin:
    """Provides historical APIs required by legacy/unit tests."""

    @property
    def _sensors(self):
        return getattr(self.sensor_service, "_sensors", [])

    @_sensors.setter
    def _sensors(self, value):
        setattr(self.sensor_service, "_sensors", value)

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

    def get_alarm_info(self) -> Dict[str, any]:
        is_ringing = bool(getattr(self.alarm, "is_ringing", lambda: False)())
        alarm_id = self.alarm.get_id() if hasattr(self.alarm, "get_id") else None
        location = (
            self.alarm.get_location() if hasattr(self.alarm, "get_location") else None
        )
        timestamp = datetime.now().isoformat() if is_ringing else None
        return {
            "is_ringing": is_ringing,
            "alarm_id": alarm_id,
            "location": location,
            "timestamp": timestamp,
        }

    def arm_sensors(self, sensor_ids):
        if not sensor_ids:
            return False
        if hasattr(self.sensor_controller, "arm_sensors"):
            return bool(self.sensor_controller.arm_sensors(sensor_ids))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), True) for sid in sensor_ids
        )

    def disarm_sensors(self, sensor_ids):
        if not sensor_ids:
            return False
        if hasattr(self.sensor_controller, "disarm_sensors"):
            return bool(self.sensor_controller.disarm_sensors(sensor_ids))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), False) for sid in sensor_ids
        )

    def read_sensor(self):
        if hasattr(self.sensor_controller, "read"):
            return self.sensor_controller.read()
        return self.sensor_service.collect_statuses()

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

    def init_system(self) -> bool:
        if self.config_manager is None:
            self.config_manager = self._config_manager
        if self.login_manager is None:
            self.login_manager = self._login_manager
        self.sensor_controller = self.sensor_service._controller
        self.camera_controller = self.camera_service._controller
        return True

    def process_message(self, stream) -> bool:
        if not hasattr(stream, "read"):
            return False
        message = stream.read()
        return bool(message)

    def receive_message(self):
        message = self._read_from_interface()
        if message:
            self.message_buffer.append(message)
        return message

    def send_message(self, response_data, target_interface) -> bool:
        return bool(self._write_to_interface(response_data, target_interface))

    def _read_from_interface(self):
        return None

    def _write_to_interface(self, response_data, target_interface):
        return False

    def arm_by_safe_home_mode(self, mode):
        sensors = None
        if hasattr(self.config_manager, "get_mode_sensors"):
            sensors = self.config_manager.get_mode_sensors(mode)
        if not sensors:
            return False
        if hasattr(self.sensor_controller, "arm_sensors"):
            return bool(self.sensor_controller.arm_sensors(sensors))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), True) for sid in sensors
        )

    def disarm_by_safe_home_mode(self, mode):
        sensors = None
        if hasattr(self.config_manager, "get_mode_sensors"):
            sensors = self.config_manager.get_mode_sensors(mode)
        if not sensors:
            return False
        if hasattr(self.sensor_controller, "disarm_sensors"):
            return bool(self.sensor_controller.disarm_sensors(sensors))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), False) for sid in sensors
        )


