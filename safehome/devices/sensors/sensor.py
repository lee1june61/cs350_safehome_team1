from abc import ABC, abstractmethod
from typing import List


class Sensor(ABC):
    """센서의 기본 추상 클래스"""
    
    def __init__(self, sensor_id: int, sensor_type: int, location: List[int]):
        """
        센서를 초기화합니다.
        
        Args:
            sensor_id: 센서 ID
            sensor_type: 센서 타입
            location: 센서 위치 [x, y]
        """
        self._id = sensor_id
        self._sensorID = sensor_id
        self._type = sensor_type
        self._sensorLocation = location if location else [0, 0]
        self._detectedSignal = 0
        self._armed = False
    
    @abstractmethod
    def read(self) -> int:
        """
        센서 상태를 읽습니다.
        
        Returns:
            센서의 감지된 신호 값
        """
        pass
    
    def arm(self) -> None:
        """센서를 활성화합니다."""
        self._armed = True
    
    def disarm(self) -> bool:
        """
        센서를 비활성화합니다.
        
        Returns:
            비활성화 성공 여부
        """
        self._armed = False
        return True
    
    def isArmed(self) -> bool:
        """
        센서의 활성화 상태를 확인합니다.
        
        Returns:
            센서 활성화 여부
        """
        return self._armed
    
    def setID(self, sensor_id: int) -> None:
        """
        센서 ID를 설정합니다.
        
        Args:
            sensor_id: 설정할 센서 ID
        """
        self._id = sensor_id
        self._sensorID = sensor_id
    
    def getID(self) -> int:
        """
        센서 ID를 반환합니다.
        
        Returns:
            센서 ID
        """
        return self._id
    
    def setType(self, sensor_type: int) -> None:
        """
        센서 타입을 설정합니다.
        
        Args:
            sensor_type: 설정할 센서 타입
        """
        self._type = sensor_type
    
    def getType(self) -> int:
        """
        센서 타입을 반환합니다.
        
        Returns:
            센서 타입
        """
        return self._type
    
    def setSensorLocation(self, location: List[int]) -> bool:
        """
        센서 위치를 설정합니다.
        
        Args:
            location: 설정할 센서 위치 [x, y]
            
        Returns:
            설정 성공 여부
        """
        if location and len(location) >= 2:
            self._sensorLocation = location
            return True
        return False
    
    def getSensorLocation(self) -> List[int]:
        """
        센서 위치를 반환합니다.
        
        Returns:
            센서 위치 [x, y]
        """
        return self._sensorLocation
    
    def getLocation(self) -> List[int]:
        """
        센서 위치를 반환합니다 (getSensorLocation의 별칭).
        
        Returns:
            센서 위치 [x, y]
        """
        return self.getSensorLocation()




