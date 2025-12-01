"""Sensor controller operations mixin."""

from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .sensor import Sensor


class SensorControllerOperationsMixin:
    """Arm/disarm and read operations for sensor controller."""

    _sensors: Dict[int, "Sensor"]

    def armSensors(self, sensorIDList: List[int]) -> bool:
        """여러 센서를 활성화합니다."""
        try:
            for sensor_id in sensorIDList:
                if sensor_id in self._sensors:
                    self._sensors[sensor_id].arm()
            return True
        except Exception:
            return False

    def armSensor(self, sensorID: int) -> bool:
        """단일 센서를 활성화합니다."""
        if sensorID in self._sensors:
            self._sensors[sensorID].arm()
            return True
        return False

    def disarmSensors(self, sensorIDList: List[int]) -> bool:
        """여러 센서를 비활성화합니다."""
        try:
            for sensor_id in sensorIDList:
                if sensor_id in self._sensors:
                    self._sensors[sensor_id].disarm()
            return True
        except Exception:
            return False

    def disarmAllSensors(self) -> bool:
        """모든 센서를 비활성화합니다."""
        try:
            for sensor in self._sensors.values():
                sensor.disarm()
            return True
        except Exception:
            return False

    def readSensor(self, sensorID: int) -> bool:
        """특정 센서의 상태를 읽습니다."""
        if sensorID in self._sensors:
            result = self._sensors[sensorID].read()
            return result > 0
        return False

    def read(self) -> int:
        """모든 센서의 상태를 읽고 감지된 센서 개수를 반환합니다."""
        count = 0
        for sensor in self._sensors.values():
            if sensor.read() > 0:
                count += 1
        return count

    # Legacy snake_case aliases
    def arm_sensors(self, sensorIDList: List[int]) -> bool:
        return self.armSensors(sensorIDList)

    def disarm_sensors(self, sensorIDList: List[int]) -> bool:
        return self.disarmSensors(sensorIDList)

    def disarm_all_sensors(self) -> bool:
        return self.disarmAllSensors()

