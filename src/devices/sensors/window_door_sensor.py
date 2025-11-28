<<<<<<< HEAD
from typing import List
from .sensor import Sensor


class WindowDoorSensor(Sensor):
    """창문/문 센서 클래스"""
    
    def __init__(self, sensor_id: int, sensor_type: int, location: List[int]):
        """
        창문/문 센서를 초기화합니다.
        
        Args:
            sensor_id: 센서 ID
            sensor_type: 센서 타입
            location: 센서 위치 [x, y]
        """
        super().__init__(sensor_id, sensor_type, location)
        self._opened = False
        self._device = None  # 연결된 물리적 디바이스
    
    def read(self) -> int:
        """
        센서 상태를 읽습니다.
        
        Returns:
            센서가 활성화되어 있고 열려있으면 1, 아니면 0
        """
        if self._armed:
            if self._device:
                # 물리적 디바이스가 연결되어 있으면 디바이스에서 읽음
                self._opened = self._device.read()
            self._detectedSignal = 1 if self._opened else 0
            return self._detectedSignal
        return 0
    
    def isOpen(self) -> bool:
        """
        창문/문이 열려있는지 확인합니다.
        
        Returns:
            열림 상태 여부
        """
        if self._device:
            self._opened = self._device.read()
        return self._opened
    
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




=======
"""
Custom Window/Door contact sensor implementation.
A detailed magnetic contact sensor simulation that extends the base virtual device.
"""
from ...virtual_devices.device_windoor_sensor import DeviceWinDoorSensor as BaseWinDoorSensor


class CustomWinDoorSensor(BaseWinDoorSensor):
    """
    A custom, more detailed virtual window/door contact sensor.
    It simulates battery drain and provides a richer interface, while extending
    the base DeviceWinDoorSensor.
    """
    
    def __init__(self, location: str, sensor_id: int, sensor_subtype: str = "door"):
        """
        Initialize the custom window/door sensor.
        
        Args:
            location: Physical location (e.g., "Front Door", "Kitchen Window")
            sensor_id: Unique sensor identifier
            sensor_subtype: Type of sensor ("door" or "window")
        """
        super().__init__()
        # Override the ID assigned by the base class
        self.sensor_id = sensor_id
        
        self._location = location
        self._subtype = sensor_subtype  # "door" or "window"
        self._battery_level = 100.0
        
        # The state 'self.opened' and 'self.armed' are inherited from BaseWinDoorSensor
        # and will be the single source of truth.

    # ============================================================
    # Override and extend base class methods
    # ============================================================
    
    def arm(self) -> bool:
        """
        Arm the sensor.
        Cannot arm if door/window is currently open (safety feature).
        """
        if self.opened:
            return False  # Cannot arm when open
        
        super().arm()
        return True
    
    def disarm(self) -> bool:
        """Disarm the sensor."""
        super().disarm()
        return True

    def read(self) -> bool:
        """
        Returns True if door/window is open AND sensor is armed.
        This is the triggered state.
        """
        # This now relies entirely on the state from the base class
        return self.armed and self.opened

    # ============================================================
    # Custom methods specific to this detailed simulation
    # ============================================================
    
    def get_location(self) -> str:
        return self._location

    def get_type(self) -> str:
        return f"{self._subtype}_sensor"

    def get_sensor_id(self) -> int:
        """Get sensor ID."""
        return self.sensor_id

    def get_subtype(self) -> str:
        """Get sensor subtype (door or window)."""
        return self._subtype

    def get_battery_level(self) -> int:
        """Get battery level."""
        if self.armed and self._battery_level > 0:
            self._battery_level -= 0.005
        
        return max(0, int(self._battery_level))

    def set_open(self, is_open: bool):
        """
        Simulate opening/closing the sensor.
        This updates the state in the base class.
        
        Args:
            is_open: True to simulate open, False for closed
        """
        if is_open:
            self.intrude()  # Sets self.opened = True in base class
        else:
            self.release()  # Sets self.opened = False in base class

    def is_open(self) -> bool:
        """Check if door/window is currently open."""
        return self.opened

    def is_closed(self) -> bool:
        """Check if door/window is currently closed."""
        return not self.opened
    
    def open(self):
        """Simulate opening (convenience method for testing)."""
        self.set_open(True)
    
    def close(self):
        """Simulate closing (convenience method for testing)."""
        self.set_open(False)

    def can_arm(self) -> bool:
        """Check if sensor can be armed (must be closed)."""
        return not self.opened

    def get_status(self) -> dict:
        """Get comprehensive sensor status."""
        return {
            'id': f"S{self.sensor_id}",
            'type': self.get_type(),
            'subtype': self._subtype,
            'location': self._location,
            'armed': self.armed,
            'is_open': self.opened,
            'triggered': self.read(),
            'battery': self.get_battery_level(),
            'can_arm': self.can_arm()
        }
    
    def __repr__(self):
        status = "ARMED" if self.armed else "DISARMED"
        state = "OPEN" if self.opened else "CLOSED"
        trigger = " [TRIGGERED]" if self.read() else ""
        return (
            f"CustomWinDoorSensor(id={self.sensor_id}, type={self._subtype}, "
            f"location='{self._location}', state={state}, status={status}{trigger})"
        )
>>>>>>> 9a4a412e3225b666a8e21459659dbb99e759a5d8
