"""
test_sensor_new.py
Unit tests for Sensor base class (새 구현 기준)
"""

import pytest
from unittest.mock import Mock
from src.devices.sensors.sensor import Sensor
from src.devices.sensors.window_door_sensor import WindowDoorSensor
from src.devices.sensors.motion_sensor import MotionSensor


class TestSensor:
    """Sensor 추상 클래스 테스트"""
    
    @pytest.fixture
    def window_door_sensor(self):
        """WindowDoorSensor를 Sensor 테스트용으로 사용"""
        return WindowDoorSensor(sensor_id=1, sensor_type=1, location=[100, 200])
    
    def test_sensor_initialization(self, window_door_sensor):
        """센서 초기화 테스트"""
        assert window_door_sensor.getID() == 1
        assert window_door_sensor.getType() == 1
        assert window_door_sensor.getLocation() == [100, 200]
        assert window_door_sensor.isArmed() is False
    
    def test_sensor_arm(self, window_door_sensor):
        """센서 활성화 테스트"""
        window_door_sensor.arm()
        assert window_door_sensor.isArmed() is True
    
    def test_sensor_disarm(self, window_door_sensor):
        """센서 비활성화 테스트"""
        window_door_sensor.arm()
        result = window_door_sensor.disarm()
        assert result is True
        assert window_door_sensor.isArmed() is False
    
    def test_sensor_set_get_id(self, window_door_sensor):
        """센서 ID 설정 및 조회 테스트"""
        window_door_sensor.setID(99)
        assert window_door_sensor.getID() == 99
    
    def test_sensor_set_get_type(self, window_door_sensor):
        """센서 타입 설정 및 조회 테스트"""
        window_door_sensor.setType(2)
        assert window_door_sensor.getType() == 2
    
    def test_sensor_set_location_valid(self, window_door_sensor):
        """유효한 위치 설정 테스트"""
        result = window_door_sensor.setSensorLocation([300, 400])
        assert result is True
        assert window_door_sensor.getSensorLocation() == [300, 400]
    
    def test_sensor_set_location_invalid(self, window_door_sensor):
        """유효하지 않은 위치 설정 테스트"""
        result = window_door_sensor.setSensorLocation([])
        assert result is False
        
        result = window_door_sensor.setSensorLocation(None)
        assert result is False
    
    def test_sensor_get_location_alias(self, window_door_sensor):
        """getLocation이 getSensorLocation의 별칭으로 동작하는지 테스트"""
        window_door_sensor.setSensorLocation([500, 600])
        assert window_door_sensor.getLocation() == [500, 600]
        assert window_door_sensor.getLocation() == window_door_sensor.getSensorLocation()


class TestWindowDoorSensor:
    """WindowDoorSensor 클래스 테스트"""
    
    @pytest.fixture
    def sensor(self):
        """WindowDoorSensor fixture"""
        return WindowDoorSensor(sensor_id=1, sensor_type=1, location=[100, 200])
    
    @pytest.fixture
    def mock_device(self):
        """Mock device fixture"""
        device = Mock()
        device.read = Mock(return_value=True)
        return device
    
    def test_initialization(self, sensor):
        """WindowDoorSensor 초기화 테스트"""
        assert sensor.getID() == 1
        assert sensor.getType() == 1
        assert sensor.getLocation() == [100, 200]
        assert sensor.isOpen() is False
    
    def test_read_when_disarmed(self, sensor):
        """비활성화 상태에서 read 테스트"""
        sensor.setOpened(True)
        result = sensor.read()
        assert result == 0  # 비활성화 상태에서는 0 반환
    
    def test_read_when_armed_and_closed(self, sensor):
        """활성화 상태에서 닫힌 경우 read 테스트"""
        sensor.arm()
        sensor.setOpened(False)
        result = sensor.read()
        assert result == 0
    
    def test_read_when_armed_and_opened(self, sensor):
        """활성화 상태에서 열린 경우 read 테스트"""
        sensor.arm()
        sensor.setOpened(True)
        result = sensor.read()
        assert result == 1
    
    def test_is_open(self, sensor):
        """isOpen 메서드 테스트"""
        assert sensor.isOpen() is False
        
        sensor.setOpened(True)
        assert sensor.isOpen() is True
        
        sensor.setOpened(False)
        assert sensor.isOpen() is False
    
    def test_set_device(self, sensor, mock_device):
        """디바이스 연결 테스트"""
        sensor.setDevice(mock_device)
        sensor.arm()
        
        # 디바이스가 연결되면 read() 시 디바이스에서 값을 읽음
        result = sensor.read()
        mock_device.read.assert_called_once()
        assert result == 1  # mock_device.read()가 True를 반환
    
    def test_read_with_device(self, sensor, mock_device):
        """디바이스 연결 시 read 동작 테스트"""
        mock_device.read.return_value = False
        sensor.setDevice(mock_device)
        sensor.arm()
        
        result = sensor.read()
        assert result == 0
        
        mock_device.read.return_value = True
        result = sensor.read()
        assert result == 1
    
    def test_is_open_with_device(self, sensor, mock_device):
        """디바이스 연결 시 isOpen 동작 테스트"""
        mock_device.read.return_value = True
        sensor.setDevice(mock_device)
        
        result = sensor.isOpen()
        assert result is True
        mock_device.read.assert_called()


class TestMotionSensor:
    """MotionSensor 클래스 테스트"""
    
    @pytest.fixture
    def sensor(self):
        """MotionSensor fixture"""
        return MotionSensor(sensor_id=2, sensor_type=2, location=[300, 400])
    
    @pytest.fixture
    def mock_device(self):
        """Mock device fixture"""
        device = Mock()
        device.read = Mock(return_value=True)
        return device
    
    def test_initialization(self, sensor):
        """MotionSensor 초기화 테스트"""
        assert sensor.getID() == 2
        assert sensor.getType() == 2
        assert sensor.getLocation() == [300, 400]
        assert sensor.isDetected() is False
    
    def test_read_when_disarmed(self, sensor):
        """비활성화 상태에서 read 테스트"""
        sensor.setDetected(True)
        result = sensor.read()
        assert result == 0  # 비활성화 상태에서는 0 반환
    
    def test_read_when_armed_and_not_detected(self, sensor):
        """활성화 상태에서 감지되지 않은 경우 read 테스트"""
        sensor.arm()
        sensor.setDetected(False)
        result = sensor.read()
        assert result == 0
    
    def test_read_when_armed_and_detected(self, sensor):
        """활성화 상태에서 감지된 경우 read 테스트"""
        sensor.arm()
        sensor.setDetected(True)
        result = sensor.read()
        assert result == 1
    
    def test_is_detected(self, sensor):
        """isDetected 메서드 테스트"""
        assert sensor.isDetected() is False
        
        sensor.setDetected(True)
        assert sensor.isDetected() is True
        
        sensor.setDetected(False)
        assert sensor.isDetected() is False
    
    def test_set_device(self, sensor, mock_device):
        """디바이스 연결 테스트"""
        sensor.setDevice(mock_device)
        sensor.arm()
        
        # 디바이스가 연결되면 read() 시 디바이스에서 값을 읽음
        result = sensor.read()
        mock_device.read.assert_called_once()
        assert result == 1  # mock_device.read()가 True를 반환
    
    def test_read_with_device(self, sensor, mock_device):
        """디바이스 연결 시 read 동작 테스트"""
        mock_device.read.return_value = False
        sensor.setDevice(mock_device)
        sensor.arm()
        
        result = sensor.read()
        assert result == 0
        
        mock_device.read.return_value = True
        result = sensor.read()
        assert result == 1
    
    def test_is_detected_with_device(self, sensor, mock_device):
        """디바이스 연결 시 isDetected 동작 테스트"""
        mock_device.read.return_value = True
        sensor.setDevice(mock_device)
        
        result = sensor.isDetected()
        assert result is True
        mock_device.read.assert_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

