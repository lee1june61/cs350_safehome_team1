"""
test_sensor_controller_new.py
Unit tests for SensorController class (새 구현 기준)
"""

import pytest
from unittest.mock import Mock, patch
from src.devices.sensors.sensor_controller import SensorController
from src.devices.sensors.window_door_sensor import WindowDoorSensor
from src.devices.sensors.motion_sensor import MotionSensor


class TestSensorController:
    """SensorController 클래스 테스트"""
    
    @pytest.fixture
    def controller(self):
        """SensorController fixture"""
        return SensorController()
    
    def test_initialization(self, controller):
        """SensorController 초기화 테스트"""
        assert controller.nextSensorID == 1
        assert controller.initialSensorNumber == 0
        assert len(controller.getAllSensors()) == 0
    
    def test_initialization_with_initial_number(self):
        """초기 센서 개수를 지정한 초기화 테스트"""
        controller = SensorController(initial_sensor_number=5)
        assert controller.initialSensorNumber == 5
    
    # addSensor 테스트
    def test_add_window_door_sensor(self, controller):
        """WindowDoorSensor 추가 테스트"""
        result = controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        assert result is True
        assert len(controller.getAllSensors()) == 1
        assert controller.nextSensorID == 2
        
        sensor = controller.getSensor(1)
        assert sensor is not None
        assert isinstance(sensor, WindowDoorSensor)
        assert sensor.getLocation() == [100, 200]
    
    def test_add_motion_sensor(self, controller):
        """MotionSensor 추가 테스트"""
        result = controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        assert result is True
        assert len(controller.getAllSensors()) == 1
        
        sensor = controller.getSensor(1)
        assert sensor is not None
        assert isinstance(sensor, MotionSensor)
        assert sensor.getLocation() == [300, 400]
    
    def test_add_invalid_sensor_type(self, controller):
        """유효하지 않은 센서 타입 추가 테스트"""
        result = controller.addSensor(100, 200, 99)  # 잘못된 타입
        assert result is False
        assert len(controller.getAllSensors()) == 0
    
    def test_add_multiple_sensors(self, controller):
        """여러 센서 추가 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        assert len(controller.getAllSensors()) == 3
        assert controller.nextSensorID == 4
    
    # removeSensor 테스트
    def test_remove_sensor_success(self, controller):
        """센서 제거 성공 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        assert len(controller.getAllSensors()) == 1
        
        result = controller.removeSensor(1)
        assert result is True
        assert len(controller.getAllSensors()) == 0
    
    def test_remove_sensor_not_exist(self, controller):
        """존재하지 않는 센서 제거 테스트"""
        result = controller.removeSensor(999)
        assert result is False
    
    def test_remove_sensor_multiple(self, controller):
        """여러 센서 중 일부 제거 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        controller.removeSensor(2)
        assert len(controller.getAllSensors()) == 2
        assert controller.getSensor(2) is None
        assert controller.getSensor(1) is not None
        assert controller.getSensor(3) is not None
    
    # armSensor 테스트
    def test_arm_single_sensor(self, controller):
        """단일 센서 활성화 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        result = controller.armSensor(1)
        assert result is True
        
        sensor = controller.getSensor(1)
        assert sensor.isArmed() is True
    
    def test_arm_sensor_not_exist(self, controller):
        """존재하지 않는 센서 활성화 테스트"""
        result = controller.armSensor(999)
        assert result is False
    
    # armSensors 테스트
    def test_arm_multiple_sensors(self, controller):
        """여러 센서 활성화 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        result = controller.armSensors([1, 3])
        assert result is True
        
        assert controller.getSensor(1).isArmed() is True
        assert controller.getSensor(2).isArmed() is False
        assert controller.getSensor(3).isArmed() is True
    
    def test_arm_empty_list(self, controller):
        """빈 리스트로 센서 활성화 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        result = controller.armSensors([])
        assert result is True  # 빈 리스트도 성공으로 처리
    
    # disarmSensors 테스트
    def test_disarm_multiple_sensors(self, controller):
        """여러 센서 비활성화 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        controller.armSensors([1, 2, 3])
        
        result = controller.disarmSensors([1, 3])
        assert result is True
        
        assert controller.getSensor(1).isArmed() is False
        assert controller.getSensor(2).isArmed() is True
        assert controller.getSensor(3).isArmed() is False
    
    # disarmAllSensors 테스트
    def test_disarm_all_sensors(self, controller):
        """모든 센서 비활성화 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        controller.armSensors([1, 2, 3])
        
        result = controller.disarmAllSensors()
        assert result is True
        
        for sensor in controller.getAllSensors().values():
            assert sensor.isArmed() is False
    
    def test_disarm_all_sensors_when_empty(self, controller):
        """센서가 없을 때 모두 비활성화 테스트"""
        result = controller.disarmAllSensors()
        assert result is True
    
    # readSensor 테스트
    def test_read_sensor(self, controller):
        """특정 센서 읽기 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        sensor = controller.getSensor(1)
        
        # 비활성화 상태
        result = controller.readSensor(1)
        assert result is False
        
        # 활성화 후 감지되지 않은 상태
        controller.armSensor(1)
        result = controller.readSensor(1)
        assert result is False
        
        # 활성화 후 감지된 상태
        sensor.setOpened(True)
        result = controller.readSensor(1)
        assert result is True
    
    def test_read_sensor_not_exist(self, controller):
        """존재하지 않는 센서 읽기 테스트"""
        result = controller.readSensor(999)
        assert result is False
    
    # read 테스트
    def test_read_all_sensors(self, controller):
        """모든 센서 읽기 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        controller.armSensors([1, 2, 3])
        
        # 아무것도 감지되지 않은 상태
        count = controller.read()
        assert count == 0
        
        # 센서 1, 3 감지
        controller.getSensor(1).setOpened(True)
        controller.getSensor(3).setOpened(True)
        
        count = controller.read()
        assert count == 2
    
    # getAllSensorsInfo 테스트
    def test_get_all_sensors_info(self, controller):
        """모든 센서 정보 조회 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        
        controller.armSensor(1)
        controller.getSensor(1).setOpened(True)
        
        info_list = controller.getAllSensorsInfo()
        
        assert len(info_list) == 2
        
        # 첫 번째 센서 정보 확인 [id, type, x, y, armed, detected]
        sensor1_info = info_list[0]
        assert sensor1_info[0] == 1  # ID
        assert sensor1_info[1] == SensorController.SENSOR_TYPE_WINDOW_DOOR  # Type
        assert sensor1_info[2] == 100  # X
        assert sensor1_info[3] == 200  # Y
        assert sensor1_info[4] == 1  # Armed
        assert sensor1_info[5] == 1  # Detected
    
    def test_get_all_sensors_info_empty(self, controller):
        """센서가 없을 때 정보 조회 테스트"""
        info_list = controller.getAllSensorsInfo()
        assert len(info_list) == 0
    
    # getSensor 테스트
    def test_get_sensor(self, controller):
        """특정 센서 조회 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        sensor = controller.getSensor(1)
        assert sensor is not None
        assert isinstance(sensor, WindowDoorSensor)
        assert sensor.getID() == 1
    
    def test_get_sensor_not_exist(self, controller):
        """존재하지 않는 센서 조회 테스트"""
        sensor = controller.getSensor(999)
        assert sensor is None
    
    # getAllSensors 테스트
    def test_get_all_sensors(self, controller):
        """모든 센서 조회 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
        
        sensors = controller.getAllSensors()
        assert len(sensors) == 2
        assert 1 in sensors
        assert 2 in sensors
        assert isinstance(sensors[1], WindowDoorSensor)
        assert isinstance(sensors[2], MotionSensor)
    
    # checkSafezone 테스트
    def test_check_safezone(self, controller):
        """안전 구역 확인 테스트"""
        controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
        
        result = controller.checkSafezone(1, True)
        assert result is True
        
        result = controller.checkSafezone(1, False)
        assert result is True
    
    def test_check_safezone_not_exist(self, controller):
        """존재하지 않는 센서의 안전 구역 확인 테스트"""
        result = controller.checkSafezone(999, True)
        assert result is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

