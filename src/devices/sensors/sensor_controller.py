from typing import List, Dict, Optional
from .sensor import Sensor
from .window_door_sensor import WindowDoorSensor
from .motion_sensor import MotionSensor


class SensorController:
    """센서들을 관리하는 컨트롤러 클래스"""
    
    # 센서 타입 상수
    SENSOR_TYPE_WINDOW_DOOR = 1
    SENSOR_TYPE_MOTION = 2
    
    def __init__(self, initial_sensor_number: int = 0):
        """
        센서 컨트롤러를 초기화합니다.
        
        Args:
            initial_sensor_number: 초기 센서 개수
        """
        self.nextSensorID = 1
        self.initialSensorNumber = initial_sensor_number
        self._sensors: Dict[int, Sensor] = {}
    
    def addSensor(self, xCoord: int, yCoord: int, inType: int) -> bool:
        """
        새로운 센서를 추가합니다.
        
        Args:
            xCoord: 센서의 X 좌표
            yCoord: 센서의 Y 좌표
            inType: 센서 타입 (1: WindowDoor, 2: Motion)
            
        Returns:
            센서 추가 성공 여부
        """
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
        """
        센서를 제거합니다.
        
        Args:
            sensorID: 제거할 센서 ID
            
        Returns:
            센서 제거 성공 여부
        """
        if sensorID in self._sensors:
            del self._sensors[sensorID]
            return True
        return False
    
    def armSensors(self, sensorIDList: List[int]) -> bool:
        """
        여러 센서를 활성화합니다.
        
        Args:
            sensorIDList: 활성화할 센서 ID 리스트
            
        Returns:
            활성화 성공 여부
        """
        try:
            for sensor_id in sensorIDList:
                if sensor_id in self._sensors:
                    self._sensors[sensor_id].arm()
            return True
        except Exception:
            return False
    
    def armSensor(self, sensorID: int) -> bool:
        """
        단일 센서를 활성화합니다.
        
        Args:
            sensorID: 활성화할 센서 ID
            
        Returns:
            활성화 성공 여부
        """
        if sensorID in self._sensors:
            self._sensors[sensorID].arm()
            return True
        return False
    
    def disarmSensors(self, sensorIDList: List[int]) -> bool:
        """
        여러 센서를 비활성화합니다.
        
        Args:
            sensorIDList: 비활성화할 센서 ID 리스트
            
        Returns:
            비활성화 성공 여부
        """
        try:
            for sensor_id in sensorIDList:
                if sensor_id in self._sensors:
                    self._sensors[sensor_id].disarm()
            return True
        except Exception:
            return False
    
    def disarmAllSensors(self) -> bool:
        """
        모든 센서를 비활성화합니다.
        
        Returns:
            비활성화 성공 여부
        """
        try:
            for sensor in self._sensors.values():
                sensor.disarm()
            return True
        except Exception:
            return False
    
    def readSensor(self, sensorID: int) -> bool:
        """
        특정 센서의 상태를 읽습니다.
        
        Args:
            sensorID: 읽을 센서 ID
            
        Returns:
            센서 감지 여부 (감지됨: True, 감지 안됨: False)
        """
        if sensorID in self._sensors:
            result = self._sensors[sensorID].read()
            return result > 0
        return False
    
    def read(self) -> int:
        """
        모든 센서의 상태를 읽고 감지된 센서 개수를 반환합니다.
        
        Returns:
            감지된 센서의 개수
        """
        count = 0
        for sensor in self._sensors.values():
            if sensor.read() > 0:
                count += 1
        return count
    
    def checkSafezone(self, sensorID: int, inSafeZone: bool) -> bool:
        """
        센서가 안전 구역 내에 있는지 확인합니다.
        
        Args:
            sensorID: 확인할 센서 ID
            inSafeZone: 안전 구역 내 여부
            
        Returns:
            확인 성공 여부
        """
        if sensorID in self._sensors:
            # 안전 구역 확인 로직
            # 실제 구현에서는 SafetyZone과 연동하여 확인
            return True
        return False
    
    def getAllSensorsInfo(self) -> List[List[int]]:
        """
        모든 센서의 정보를 반환합니다.
        
        Returns:
            센서 정보 리스트 [[id, type, x, y, armed, detected], ...]
        """
        info_list = []
        for sensor_id, sensor in self._sensors.items():
            location = sensor.getLocation()
            info = [
                sensor_id,
                sensor.getType(),
                location[0] if len(location) > 0 else 0,
                location[1] if len(location) > 1 else 0,
                1 if sensor.isArmed() else 0,
                sensor.read()
            ]
            info_list.append(info)
        return info_list
    
    def getSensor(self, sensorID: int) -> Optional[Sensor]:
        """
        특정 센서 객체를 반환합니다.
        
        Args:
            sensorID: 조회할 센서 ID
            
        Returns:
            센서 객체 또는 None
        """
        return self._sensors.get(sensorID)
    
    def getAllSensors(self) -> Dict[int, Sensor]:
        """
        모든 센서 객체를 반환합니다.
        
        Returns:
            센서 ID를 키로 하는 센서 딕셔너리
        """
        return self._sensors




