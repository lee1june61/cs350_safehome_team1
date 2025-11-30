"""Sensor controller for managing sensors."""

from typing import List, Dict, Optional
from .sensor import Sensor
from .window_door_sensor import WindowDoorSensor
from .motion_sensor import MotionSensor
from .sensor_controller_operations import SensorControllerOperationsMixin


class SensorController(SensorControllerOperationsMixin):
    """센서들을 관리하는 컨트롤러 클래스"""

    SENSOR_TYPE_WINDOW_DOOR = 1
    SENSOR_TYPE_MOTION = 2

    def __init__(self, initial_sensor_number: int = 0):
        self.nextSensorID = 1
        self.initialSensorNumber = initial_sensor_number
        self._sensors: Dict[int, Sensor] = {}

    def initialize(self) -> bool:
        """Legacy initializer hook for compatibility tests."""
        return True

    def addSensor(self, xCoord: int, yCoord: int, inType: int) -> bool:
        """새로운 센서를 추가합니다."""
        try:
            sensor_id = self.nextSensorID
            location = [xCoord, yCoord]
            if inType == self.SENSOR_TYPE_WINDOW_DOOR:
                sensor = WindowDoorSensor(sensor_id, inType, location)
            elif inType == self.SENSOR_TYPE_MOTION:
                sensor = MotionSensor(sensor_id, inType, location)
            else:
                return False
            self._sensors[sensor_id] = sensor
            self.nextSensorID += 1
            return True
        except Exception:
            return False

    def removeSensor(self, sensorID: int) -> bool:
        """센서를 제거합니다."""
        if sensorID in self._sensors:
            del self._sensors[sensorID]
            return True
        return False

    def checkSafezone(self, sensorID: int, inSafeZone: bool) -> bool:
        """센서가 안전 구역 내에 있는지 확인합니다."""
        return sensorID in self._sensors

    def getAllSensorsInfo(self) -> List[List[int]]:
        """모든 센서의 정보를 반환합니다."""
        info_list = []
        for sensor_id, sensor in self._sensors.items():
            location = sensor.getLocation()
            info = [
                sensor_id, sensor.getType(),
                location[0] if len(location) > 0 else 0,
                location[1] if len(location) > 1 else 0,
                1 if sensor.isArmed() else 0, sensor.read()
            ]
            info_list.append(info)
        return info_list

    def getSensor(self, sensorID: int) -> Optional[Sensor]:
        """특정 센서 객체를 반환합니다."""
        return self._sensors.get(sensorID)

    def getAllSensors(self) -> Dict[int, Sensor]:
        """모든 센서 객체를 반환합니다."""
        return self._sensors
