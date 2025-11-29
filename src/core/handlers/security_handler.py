"""Security-related command implementations."""

from __future__ import annotations

from typing import Any, Callable, Dict

from ..logging.system_logger import SystemLogger
from ..services.sensor_service import SensorService
from ..services.zone_service import ZoneService
from ..services.mode_service import ModeService
from ..services.alarm_service import AlarmService
from ..services.auth_service import AuthService
from ..services.camera_service import CameraService
from .security.zone_handler import ZoneCommandHandler
from .security.sensor_handler import SensorCommandHandler
from .security.alarm_handler import AlarmCommandHandler


class SecurityHandler:
    """Handles arm/disarm operations, zones, and alarm lifecycle."""

    def __init__(
        self,
        sensor_service: SensorService,
        zone_service: ZoneService,
        mode_service: ModeService,
        alarm_service: AlarmService,
        auth_service: AuthService,
        camera_service: CameraService,
        logger: SystemLogger,
        *,
        door_state_supplier: Callable[[], bool],
    ):
        self._sensor_service = sensor_service
        self._zone_service = zone_service
        self._mode_service = mode_service
        self._alarm_service = alarm_service
        self._auth_service = auth_service
        self._camera_service = camera_service
        self._logger = logger
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
            return {
                "success": False,
                "message": "Cannot arm, a door or window is open.",
            }
        return self._mode_service.arm_system(
            mode=mode, user=self._auth_service.current_user
        )

    def disarm_system(self, **_) -> Dict[str, Any]:
        return self._mode_service.disarm_system(self._zone_service)

    def panic(self, **_) -> Dict[str, Any]:
        return self._alarm_service.panic()

    # --- Zones --------------------------------------------------------
    def get_safety_zones(self, **_) -> Dict[str, Any]:
        return self._zone_handler.get_zones()

    def arm_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zone_handler.arm_zone(zone_id)

    def disarm_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zone_handler.disarm_zone(zone_id)

    def create_safety_zone(self, name="", sensors=None, **_) -> Dict[str, Any]:
        return self._zone_handler.create_zone(name=name, sensors=sensors)

    def update_safety_zone(self, zone_id=None, name=None, sensors=None, **_) -> Dict[str, Any]:
        return self._zone_handler.update_zone(
            zone_id=zone_id, name=name, sensors=sensors
        )

    def delete_safety_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zone_handler.delete_zone(zone_id=zone_id)

    # --- Sensors / Devices -------------------------------------------
    def get_sensors(self, **_) -> Dict[str, Any]:
        return self._sensor_handler.get_sensors()

    def get_all_devices_status(self, **_) -> Dict[str, Any]:
        return self._sensor_handler.get_devices()

    def arm_sensor(self, sensor_id="", **_) -> Dict[str, Any]:
        return self._sensor_handler.arm_sensor(sensor_id=sensor_id)

    def disarm_sensor(self, sensor_id="", **_) -> Dict[str, Any]:
        return self._sensor_handler.disarm_sensor(sensor_id=sensor_id)

    def poll_sensors(self, **_) -> Dict[str, Any]:
        result = self._sensor_handler.poll_sensors()
        if result.get("intrusion_detected"):
            sensor_id = result.get("sensor_id")
            alarm = self._alarm_handler.trigger(sensor_id=sensor_id)
            return {
                "success": True,
                "intrusion_detected": True,
                "sensor_id": sensor_id,
                "alarm": alarm,
            }
        return result

    # --- Alarm lifecycle ---------------------------------------------
    def trigger_alarm(self, sensor_id="", **_) -> Dict[str, Any]:
        return self._alarm_handler.trigger(sensor_id=sensor_id)

    def clear_alarm(self, **_) -> Dict[str, Any]:
        return self._alarm_handler.clear()

    def get_alarm_status(self, **_) -> Dict[str, Any]:
        return self._alarm_handler.status()


