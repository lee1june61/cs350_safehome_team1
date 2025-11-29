"""Sensor orchestration helpers."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

from ...devices.sensors.motion_sensor import MotionSensor
from ...devices.sensors.sensor_controller import SensorController
from ...devices.sensors.window_door_sensor import WindowDoorSensor
from .sensor.sensor_registry import SensorRegistry
from .sensor.sensor_state import SensorStateService
from .sensor.sensor_arm import SensorArmService


class SensorService:
    """Adds/arms/disarms sensors and exposes their status."""

    def __init__(self, controller: SensorController):
        self._controller = controller
        self._registry = SensorRegistry(controller)
        self._state = SensorStateService(self._registry)
        self._arm = SensorArmService(self._registry)
        self._sensors: List[Union[WindowDoorSensor, MotionSensor]] = []

    # ------------------------------------------------------------------ #
    def initialize_defaults(
        self,
        sensor_data: List[Dict[str, Any]],
        sensor_coords: Dict[str, Tuple[int, int]],
    ):
        self._registry.initialize(sensor_data, sensor_coords)
        self._sensors = self._registry.instances

    # ------------------------------------------------------------------ #
    def collect_statuses(self) -> List[Dict[str, Any]]:
        return self._state.collect_statuses()

    def get_sensor(self, sensor_id: str):
        return self._registry.get_sensor(sensor_id)

    def set_sensor_armed(self, sensor_id: str, armed: bool) -> bool:
        return self._arm.set_sensor_armed(sensor_id, armed)

    def disarm_all(self):
        self._arm.disarm_all()

    def door_or_window_open(self) -> Optional[str]:
        return self._arm.door_or_window_open()

    def get_devices_payload(
        self,
        camera_info: List[Dict[str, Any]],
        camera_labels: Dict[int, str],
    ) -> Dict[str, Dict[str, Any]]:
        return self._state.devices_payload(camera_info, camera_labels)

    def poll_armed_sensors(self, armed_mode: bool):
        return self._arm.poll_armed_sensors(armed_mode)

    @property
    def sensor_ids(self) -> List[str]:
        return list(self._registry.lookup.keys())

    @property
    def metadata(self) -> Dict[str, Dict[str, Any]]:
        return self._registry.metadata


