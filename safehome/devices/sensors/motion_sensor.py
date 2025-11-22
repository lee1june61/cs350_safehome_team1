from typing import List
from .sensor import Sensor


class MotionSensor(Sensor):
    """모션 감지 센서 클래스"""
    
    def __init__(self, sensor_id: int, sensor_type: int, location: List[int]):
        """
        모션 센서를 초기화합니다.
        
        Args:
            sensor_id: 센서 ID
            sensor_type: 센서 타입
            location: 센서 위치 [x, y]
        """
        super().__init__(sensor_id, sensor_type, location)
        self._detected = False
        self._device = None  # 연결된 물리적 디바이스
    
    def read(self) -> int:
        """
        센서 상태를 읽습니다.
        
        Returns:
            센서가 활성화되어 있고 모션이 감지되면 1, 아니면 0
        """
        if self._armed:
            if self._device:
                # 물리적 디바이스가 연결되어 있으면 디바이스에서 읽음
                self._detected = self._device.read()
            self._detectedSignal = 1 if self._detected else 0
            return self._detectedSignal
        return 0
    
    def isDetected(self) -> bool:
        """
        모션이 감지되었는지 확인합니다.
        
        Returns:
            모션 감지 여부
        """
        if self._device:
            self._detected = self._device.read()
        return self._detected
    
    def setDevice(self, device) -> None:
        """
        물리적 디바이스를 연결합니다.
        
        Args:
            device: 연결할 DeviceMotionDetector 객체
        """
        self._device = device
    
    def setDetected(self, detected: bool) -> None:
        """
        테스트를 위한 감지 상태 설정 메서드
        
        Args:
            detected: 감지 상태
        """
        self._detected = detected




