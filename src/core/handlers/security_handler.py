"""Security-related command implementations."""

from __future__ import annotations

from typing import Any, Callable, Dict

from .security.zone_handler import ZoneCommandHandler
from .security.sensor_handler import SensorCommandHandler
from .security.alarm_handler import AlarmCommandHandler


class SecurityHandler:
    """Handles arm/disarm operations, zones, and alarm lifecycle."""

    def __init__(
        self,
        sensor_service,
        zone_service,
        mode_service,
        alarm_service,
        auth_service,
        camera_service,
        logger,
        *,
        door_state_supplier: Callable[[], bool],
    ):
        self._mode = mode_service
        self._alarm = alarm_service
        self._auth = auth_service
        self._door_state_supplier = door_state_supplier
        self._zone_handler = ZoneCommandHandler(
            zone_service, sensor_service, auth_service
        )
        self._sensor_handler = SensorCommandHandler(
            sensor_service, mode_service, camera_service
        )
        self._alarm_handler = AlarmCommandHandler(
            sensor_service, zone_service, alarm_service, auth_service, logger
        )

    # --- Arm / Disarm -------------------------------------------------
    def arm_system(self, mode="AWAY", **_) -> Dict[str, Any]:
        if self._door_state_supplier():
            return {"success": False, "message": "Cannot arm, door/window open."}
        return self._mode.arm_system(mode=mode, user=self._auth.current_user)

    def disarm_system(self, **_) -> Dict[str, Any]:
        return self._mode.disarm_system(self._zone_handler._zones)

    def panic(self, **_) -> Dict[str, Any]:
        return self._alarm.panic()

    # --- Zones --------------------------------------------------------
    def get_safety_zones(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.get_zones(**kw)

    def arm_zone(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.arm_zone(**kw)

    def disarm_zone(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.disarm_zone(**kw)

    def create_safety_zone(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.create_zone(**kw)

    def update_safety_zone(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.update_zone(**kw)

    def delete_safety_zone(self, **kw) -> Dict[str, Any]:
        return self._zone_handler.delete_zone(**kw)

    # --- Sensors / Devices -------------------------------------------
    def get_sensors(self, **kw) -> Dict[str, Any]:
        return self._sensor_handler.get_sensors(**kw)

    def get_all_devices_status(self, **kw) -> Dict[str, Any]:
        return self._sensor_handler.get_devices(**kw)

    def arm_sensor(self, **kw) -> Dict[str, Any]:
        return self._sensor_handler.arm_sensor(**kw)

    def disarm_sensor(self, **kw) -> Dict[str, Any]:
        return self._sensor_handler.disarm_sensor(**kw)

    def poll_sensors(self, **_) -> Dict[str, Any]:
        result = self._sensor_handler.poll_sensors()
        if result.get("intrusion_detected"):
            alarm = self._alarm_handler.trigger(sensor_id=result.get("sensor_id"))
            return {**result, "alarm": alarm}
        return result

    # --- Alarm lifecycle ---------------------------------------------
    def trigger_alarm(self, **kw) -> Dict[str, Any]:
        return self._alarm_handler.trigger(**kw)

    def clear_alarm(self, **_) -> Dict[str, Any]:
        return self._alarm_handler.clear()

    def get_alarm_status(self, **_) -> Dict[str, Any]:
        return self._alarm_handler.status()
