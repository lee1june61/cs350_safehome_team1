"""Window/door sensor implementation."""

from typing import List, Optional, Dict, Any
from .sensor import Sensor
from .window_door_sensor_metadata import WindowDoorSensorMetadataMixin


class WindowDoorSensor(WindowDoorSensorMetadataMixin, Sensor):
    """창문/문 센서 클래스"""

    def __init__(self, sensor_id: int = 0, sensor_type: int = 0, location: Optional[List[int]] = None):
        super().__init__(sensor_id or 0, sensor_type or 0, location or [0, 0])
        self._opened = False
        self._device = None
        self.hardware = None
        self.status = "DISARMED"
        self.type = sensor_type or 0
        self._friendly_id = f"S{self._id}"
        self._location_label = "Unknown"
        self._category = "sensor"
        self._extra: Dict[str, Any] = {}

    def read(self) -> int:
        if self._armed:
            self._opened = self._read_hardware()
            self._detectedSignal = 1 if self._opened else 0
            return self._detectedSignal
        return 0

    def isOpen(self) -> bool:
        if self._device or self.hardware:
            self._opened = self._read_hardware()
        return self._opened

    def is_open(self) -> bool:
        if self.status != "ARMED":
            return False
        return bool(self._read_hardware())

    def setDevice(self, device) -> None:
        self._device = device

    def setOpened(self, opened: bool) -> None:
        self._opened = opened
        self.status = "OPEN" if opened else "CLOSED"

    def set_open(self, opened: bool) -> None:
        self.setOpened(opened)

    def _read_hardware(self) -> bool:
        if self.hardware:
            return bool(self.hardware.read())
        if self._device:
            return bool(self._device.read())
        return self._opened

    def arm(self) -> None:
        super().arm()
        self.status = "ARMED"

    def disarm(self) -> bool:
        result = super().disarm()
        self.status = "DISARMED"
        return result

    def setType(self, sensor_type: int) -> None:
        super().setType(sensor_type)
        self.type = sensor_type

    def can_arm(self) -> bool:
        return not self.isOpen()

    def isArmed(self) -> bool:
        return self._armed

    def getID(self) -> int:
        return self._id
