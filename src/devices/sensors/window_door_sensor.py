from typing import List, Optional, Dict, Any
from .sensor import Sensor


class WindowDoorSensor(Sensor):
    """창문/문 센서 클래스"""

    def __init__(
        self,
        sensor_id: int = 0,
        sensor_type: int = 0,
        location: Optional[List[int]] = None,
    ):
        """
        창문/문 센서를 초기화합니다.

        Args:
            sensor_id: 센서 ID
            sensor_type: 센서 타입
            location: 센서 위치 [x, y]
        """
        super().__init__(sensor_id or 0, sensor_type or 0, location or [0, 0])
        self._opened = False
        self._device = None  # 연결된 물리적 디바이스
        self.hardware = None  # 테스트를 위한 하드웨어 모킹 포인트
        self.status = "DISARMED"
        self.type = sensor_type or 0
        self._friendly_id = f"S{self._id}"
        self._location_label = "Unknown"
        self._category = "sensor"
        self._extra: Dict[str, Any] = {}

    def read(self) -> int:
        """
        센서 상태를 읽습니다.

        Returns:
            센서가 활성화되어 있고 열려있으면 1, 아니면 0
        """
        if self._armed:
            self._opened = self._read_hardware()
            self._detectedSignal = 1 if self._opened else 0
            return self._detectedSignal
        return 0

    def isOpen(self) -> bool:
        """
        창문/문이 열려있는지 확인합니다.

        Returns:
            열림 상태 여부
        """
        if self._device or self.hardware:
            self._opened = self._read_hardware()
        return self._opened

    def is_open(self) -> bool:
        """
        snake_case helper used by certain tests/UI layers.
        """
        if self.status != "ARMED":
            return False
        return bool(self._read_hardware())

    # ------------------------------------------------------------------
    # Metadata helpers used by System/UI layers
    # ------------------------------------------------------------------
    def set_metadata(
        self,
        friendly_id: str,
        location_name: str,
        category: str = "sensor",
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Attach presentation metadata (id, friendly name, type)."""
        self._friendly_id = friendly_id or self._friendly_id
        self._location_label = location_name or self._location_label
        normalized = (category or "sensor").lower()
        if normalized == "door":
            self._category = "door_sensor"
        elif normalized == "window":
            self._category = "sensor"
        else:
            self._category = normalized
        self._extra = extra or {}

    def get_sensor_id(self) -> int:
        """Legacy helper used by System."""
        return self.getID()

    def get_location(self) -> str:
        """Return human readable location string."""
        return self._location_label

    def setDevice(self, device) -> None:
        """
        물리적 디바이스를 연결합니다.

        Args:
            device: 연결할 DeviceWinDoorSensor 객체
        """
        self._device = device

    def setOpened(self, opened: bool) -> None:
        """
        테스트를 위한 열림 상태 설정 메서드

        Args:
            opened: 열림 상태
        """
        self._opened = opened
        # Keep hardware flag in sync for tests
        if opened:
            self.status = "OPEN"
        else:
            self.status = "CLOSED"

    def set_open(self, opened: bool) -> None:
        """
        Custom helper expected by certain legacy tests/UI code.
        """
        self.setOpened(opened)

    def _read_hardware(self) -> bool:
        """
        하드웨어(또는 모킹된 디바이스)에서 상태를 읽는다.
        """
        if self.hardware:
            return bool(self.hardware.read())
        if self._device:
            return bool(self._device.read())
        return self._opened

    def arm(self) -> None:
        """센서를 활성화하고 상태 문자열을 동기화한다."""
        super().arm()
        self.status = "ARMED"

    def disarm(self) -> bool:
        """센서를 비활성화하고 상태 문자열을 동기화한다."""
        result = super().disarm()
        self.status = "DISARMED"
        return result

    def setType(self, sensor_type: int) -> None:
        """타입 설정 시 테스트용 속성도 함께 갱신한다."""
        super().setType(sensor_type)
        self.type = sensor_type

    def can_arm(self) -> bool:
        """Check if sensor can be armed (must be closed)."""
        return not self.isOpen()

    def get_type(self) -> str:
        """Return presentation type string used by UI/floor plan."""
        return self._category

    def get_status(self) -> Dict[str, Any]:
        """Return structured status for UI/system queries."""
        is_open = self.isOpen()
        return {
            "id": self._friendly_id,
            "name": self._location_label,
            "type": self.get_type(),
            "location": self._location_label,
            "armed": self.isArmed(),
            "is_open": is_open,
            "status": "open" if is_open else "closed",
            "can_arm": self.can_arm(),
            "extra": self._extra.copy(),
        }
