"""Legacy mode methods for backward compatibility."""

from __future__ import annotations


class LegacyModeMixin:
    """Provides legacy mode APIs required by older unit tests."""

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

