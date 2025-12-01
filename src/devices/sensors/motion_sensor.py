"""Motion sensor implementation."""

from typing import List, Dict, Any
from .sensor import Sensor
from .motion_sensor_metadata import MotionSensorMetadataMixin


class MotionSensor(MotionSensorMetadataMixin, Sensor):
    """모션 감지 센서 클래스"""

    def __init__(self, sensor_id: int, sensor_type: int, location: List[int]):
        super().__init__(sensor_id, sensor_type, location)
        self._detected = False
        self._device = None
        self._friendly_id = f"M{self._id}"
        self._location_label = "Unknown"
        self._category = "motion"
        self._extra: Dict[str, Any] = {}
        self._detectedSignal = 0

    def read(self) -> int:
        """센서 상태를 읽습니다."""
        if self._armed:
            if self._device:
                self._detected = self._device.read()
            self._detectedSignal = 1 if self._detected else 0
            return self._detectedSignal
        return 0

    def isDetected(self) -> bool:
        """모션이 감지되었는지 확인합니다."""
        if self._device:
            self._detected = self._device.read()
        return self._detected

    def setDevice(self, device) -> None:
        """물리적 디바이스를 연결합니다."""
        self._device = device

    def setDetected(self, detected: bool) -> None:
        """테스트를 위한 감지 상태 설정 메서드"""
        self._detected = detected

    def isArmed(self) -> bool:
        return self._armed

    def getID(self) -> int:
        return self._id
