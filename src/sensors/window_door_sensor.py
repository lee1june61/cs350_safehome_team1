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




