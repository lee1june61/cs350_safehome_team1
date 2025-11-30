"""Sensor registry and lookup helpers."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union

from src.devices.sensors.motion_sensor import MotionSensor
from src.devices.sensors.sensor_controller import SensorController
from src.devices.sensors.window_door_sensor import WindowDoorSensor


class SensorRegistry:
    """Responsible for bootstrapping sensors and maintaining lookup maps."""

    def __init__(self, controller: SensorController):
        self._controller = controller
        self.lookup: Dict[str, int] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.instances: List[Union[WindowDoorSensor, MotionSensor]] = []

    def initialize(
        self,
        sensor_data: List[Dict[str, Any]],
        sensor_coords: Dict[str, Tuple[int, int]],
    ):
        sensors: List[Union[WindowDoorSensor, MotionSensor]] = []
        for entry in sensor_data:
            sensor_id = entry.get("id")
            if not sensor_id:
                continue
            coords = sensor_coords.get(sensor_id, (0, 0))
            sensor_type = (
                SensorController.SENSOR_TYPE_MOTION
                if entry.get("type") == "MOTION"
                else SensorController.SENSOR_TYPE_WINDOW_DOOR
            )
            if not self._controller.addSensor(coords[0], coords[1], sensor_type):
                continue
            controller_id = self._controller.nextSensorID - 1
            sensor_obj = self._controller.getSensor(controller_id)
            display_name = entry.get("name") or entry.get("location") or sensor_id
            category = entry.get("type", "").lower()
            extra = {"label": entry.get("location")}
            if hasattr(sensor_obj, "set_metadata"):
                sensor_obj.set_metadata(
                    friendly_id=sensor_id,
                    location_name=display_name,
                    category=category,
                    extra=extra,
                )
            else:
                setattr(sensor_obj, "friendly_id", sensor_id)
                setattr(sensor_obj, "location_name", display_name)
            self.lookup[sensor_id] = controller_id
            self.metadata[sensor_id] = entry
            if entry.get("armed"):
                sensor_obj.arm()
            else:
                sensor_obj.disarm()
            sensors.append(sensor_obj)
        self.instances = sensors

    def get_sensor(self, sensor_id: str):
        internal_id = self.lookup.get(sensor_id)
        if internal_id is None:
            return None
        return self._controller.getSensor(internal_id)


