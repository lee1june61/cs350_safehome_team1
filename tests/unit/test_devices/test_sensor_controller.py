"""
test_sensor_controller.py
Unit tests for SensorController class
"""

import pytest
from unittest.mock import Mock, MagicMock
from sensor_controller import SensorController
from sensor import Sensor
from window_door_sensor import WindowDoorSensor
from motion_sensor import MotionSensor


class TestSensorController:
    """Unit tests for SensorController class"""
    
    @pytest.fixture
    def sensor_controller(self):
        """Fixture to create a SensorController instance"""
        return SensorController()
    
    @pytest.fixture
    def mock_sensor(self):
        """Fixture to create a mock Sensor"""
        sensor = Mock(spec=Sensor)
        sensor.get_id = Mock(return_value=1)
        sensor.get_type = Mock(return_value=1)
        sensor.get_sensor_location = Mock(return_value=[100, 200])
        sensor.is_armed = Mock(return_value=False)
        return sensor
    
    # UT-SC-addSensor-Valid
    def test_add_sensor_valid_coordinates(self, sensor_controller):
        """
        Test Case: addSensor()
        Description: Verifies new sensor is added at specified coordinates
        Reference: CRC Card for SensorController, Class Diagram page 16
        """
        # Arrange
        x_coord = 100
        y_coord = 200
        sensor_type = 1  # WINDOW_DOOR
        
        # Act
        sensor_id = sensor_controller.add_sensor(x_coord, y_coord, sensor_type)
        
        # Assert
        assert sensor_id is not None
        assert sensor_id > 0
        assert len(sensor_controller.sensor_list) == 1
        
        added_sensor = sensor_controller.sensor_list[0]
        assert added_sensor.get_sensor_location() == [x_coord, y_coord]
        assert added_sensor.get_type() == sensor_type
    
    def test_add_sensor_invalid_coordinates(self, sensor_controller):
        """
        Test Case: addSensor() with out-of-bounds coordinates
        Description: Verifies rejection of invalid coordinates
        """
        # Arrange
        x_coord = -10
        y_coord = 5000
        sensor_type = 1
        
        # Act
        sensor_id = sensor_controller.add_sensor(x_coord, y_coord, sensor_type)
        
        # Assert
        assert sensor_id is None
        assert len(sensor_controller.sensor_list) == 0
    
    def test_add_sensor_duplicate_location(self, sensor_controller):
        """
        Test Case: addSensor() at existing sensor location
        Description: Verifies handling of duplicate locations
        """
        # Arrange
        x_coord = 100
        y_coord = 200
        sensor_type = 1
        
        # Act
        first_id = sensor_controller.add_sensor(x_coord, y_coord, sensor_type)
        second_id = sensor_controller.add_sensor(x_coord, y_coord, sensor_type)
        
        # Assert
        assert first_id is not None
        assert second_id is not None
        assert first_id != second_id  # Different IDs allowed at same location
        assert len(sensor_controller.sensor_list) == 2
    
    # UT-SC-deleteSensor
    def test_delete_sensor_existing(self, sensor_controller, mock_sensor):
        """
        Test Case: deleteSensor()
        Description: Verifies sensor is properly removed
        Reference: CRC Card for SensorController
        """
        # Arrange
        sensor_controller.sensor_list = [mock_sensor]
        sensor_id = 1
        
        # Act
        result = sensor_controller.delete_sensor(sensor_id)
        
        # Assert
        assert result is True
        assert len(sensor_controller.sensor_list) == 0
    
    def test_delete_sensor_non_existing(self, sensor_controller):
        """
        Test Case: deleteSensor() with invalid ID
        Description: Verifies handling of non-existent sensor
        """
        # Arrange
        sensor_id = 999
        
        # Act
        result = sensor_controller.delete_sensor(sensor_id)
        
        # Assert
        assert result is False
    
    # UT-SC-armSensors
    def test_arm_sensors_valid_list(self, sensor_controller):
        """
        Test Case: armSensors()
        Description: Verifies multiple sensors armed simultaneously
        Reference: Sequence Diagram page 55-56 of SDS
        """
        # Arrange
        sensor1 = Mock(spec=Sensor)
        sensor1.get_id = Mock(return_value=1)
        sensor1.arm = Mock(return_value=True)
        
        sensor2 = Mock(spec=Sensor)
        sensor2.get_id = Mock(return_value=3)
        sensor2.arm = Mock(return_value=True)
        
        sensor3 = Mock(spec=Sensor)
        sensor3.get_id = Mock(return_value=4)
        sensor3.arm = Mock(return_value=True)
        
        sensor_controller.sensor_list = [sensor1, sensor2, sensor3]
        sensor_ids = [1, 3]
        
        # Act
        result = sensor_controller.arm_sensors(sensor_ids)
        
        # Assert
        assert result == [True, True]
        sensor1.arm.assert_called_once()
        sensor2.arm.assert_called_once()
        sensor3.arm.assert_not_called()
    
    def test_arm_sensors_empty_list(self, sensor_controller):
        """
        Test Case: armSensors() with empty list
        Description: Verifies handling of empty sensor list
        """
        # Arrange
        sensor_ids = []
        
        # Act
        result = sensor_controller.arm_sensors(sensor_ids)
        
        # Assert
        assert result == []
    
    # UT-SC-disarmSensors
    def test_disarm_sensors_valid_list(self, sensor_controller):
        """
        Test Case: disarmSensors()
        Description: Verifies multiple sensors disarmed together
        Reference: State Diagram for Sensor
        """
        # Arrange
        sensor1 = Mock(spec=Sensor)
        sensor1.get_id = Mock(return_value=2)
        sensor1.disarm = Mock(return_value=True)
        sensor1.is_armed = Mock(return_value=True)
        
        sensor2 = Mock(spec=Sensor)
        sensor2.get_id = Mock(return_value=4)
        sensor2.disarm = Mock(return_value=True)
        sensor2.is_armed = Mock(return_value=True)
        
        sensor_controller.sensor_list = [sensor1, sensor2]
        sensor_ids = [2, 4]
        
        # Act
        result = sensor_controller.disarm_sensors(sensor_ids)
        
        # Assert
        assert result == [True, True]
        sensor1.disarm.assert_called_once()
        sensor2.disarm.assert_called_once()
    
    # UT-SC-armAllSensors
    def test_arm_all_sensors(self, sensor_controller):
        """
        Test Case: armAllSensors()
        Description: Verifies all sensors armed in single operation
        Reference: CRC Card for SensorController
        """
        # Arrange
        sensors = []
        for i in range(5):
            sensor = Mock(spec=Sensor)
            sensor.get_id = Mock(return_value=i+1)
            sensor.arm = Mock(return_value=True)
            sensors.append(sensor)
        
        sensor_controller.sensor_list = sensors
        
        # Act
        count = sensor_controller.arm_all_sensors()
        
        # Assert
        assert count == 5
        for sensor in sensors:
            sensor.arm.assert_called_once()
    
    def test_arm_all_sensors_empty(self, sensor_controller):
        """
        Test Case: armAllSensors() with no sensors
        Description: Verifies handling of empty sensor list
        """
        # Arrange
        sensor_controller.sensor_list = []
        
        # Act
        count = sensor_controller.arm_all_sensors()
        
        # Assert
        assert count == 0
    
    # UT-SC-disarmAllSensors
    def test_disarm_all_sensors(self, sensor_controller):
        """
        Test Case: disarmAllSensors()
        Description: Verifies all sensors disarmed simultaneously
        Reference: Sequence Diagram page 52 of SDS
        """
        # Arrange
        sensors = []
        for i in range(3):
            sensor = Mock(spec=Sensor)
            sensor.get_id = Mock(return_value=i+1)
            sensor.disarm = Mock(return_value=True)
            sensor.is_armed = Mock(return_value=True)
            sensors.append(sensor)
        
        sensor_controller.sensor_list = sensors
        
        # Act
        count = sensor_controller.disarm_all_sensors()
        
        # Assert
        assert count == 3
        for sensor in sensors:
            sensor.disarm.assert_called_once()
    
    # UT-SC-armSensor
    def test_arm_sensor_single(self, sensor_controller):
        """
        Test Case: armSensor()
        Description: Verifies single sensor is armed
        Reference: State Diagram for Sensor
        """
        # Arrange
        sensor = Mock(spec=Sensor)
        sensor.get_id = Mock(return_value=3)
        sensor.arm = Mock(return_value=True)
        
        sensor_controller.sensor_list = [sensor]
        
        # Act
        result = sensor_controller.arm_sensor(3)
        
        # Assert
        assert result is True
        sensor.arm.assert_called_once()
    
    def test_arm_sensor_invalid_id(self, sensor_controller):
        """
        Test Case: armSensor() with invalid ID
        Description: Verifies handling of non-existent sensor
        """
        # Arrange
        sensor_controller.sensor_list = []
        
        # Act
        result = sensor_controller.arm_sensor(999)
        
        # Assert
        assert result is False
    
    # UT-SC-disarmSensor
    def test_disarm_sensor_single(self, sensor_controller):
        """
        Test Case: disarmSensor()
        Description: Verifies specific sensor is disarmed
        Reference: CRC Card for SensorController
        """
        # Arrange
        sensor = Mock(spec=Sensor)
        sensor.get_id = Mock(return_value=7)
        sensor.disarm = Mock(return_value=True)
        sensor.is_armed = Mock(return_value=True)
        
        sensor_controller.sensor_list = [sensor]
        
        # Act
        result = sensor_controller.disarm_sensor(7)
        
        # Assert
        assert result is True
        sensor.disarm.assert_called_once()
    
    # UT-SC-read
    def test_read_sensors_with_detection(self, sensor_controller):
        """
        Test Case: read()
        Description: Verifies controller reads all armed sensors
        Reference: Sequence Diagram page 58 of SDS
        """
        # Arrange
        sensor1 = Mock(spec=Sensor)
        sensor1.get_id = Mock(return_value=1)
        sensor1.is_armed = Mock(return_value=True)
        sensor1.read = Mock(return_value=True)  # Detection
        
        sensor2 = Mock(spec=Sensor)
        sensor2.get_id = Mock(return_value=2)
        sensor2.is_armed = Mock(return_value=True)
        sensor2.read = Mock(return_value=False)  # No detection
        
        sensor3 = Mock(spec=Sensor)
        sensor3.get_id = Mock(return_value=3)
        sensor3.is_armed = Mock(return_value=False)  # Disarmed
        sensor3.read = Mock(return_value=False)
        
        sensor_controller.sensor_list = [sensor1, sensor2, sensor3]
        
        # Act
        readings = sensor_controller.read()
        
        # Assert
        assert len(readings) == 3
        assert readings[0]['detection'] is True
        assert readings[1]['detection'] is False
        assert readings[2]['detection'] is False
        sensor1.read.assert_called_once()
        sensor2.read.assert_called_once()
    
    def test_read_sensors_all_clear(self, sensor_controller):
        """
        Test Case: read() with no detections
        Description: Verifies normal operation with no activity
        """
        # Arrange
        sensors = []
        for i in range(3):
            sensor = Mock(spec=Sensor)
            sensor.get_id = Mock(return_value=i+1)
            sensor.is_armed = Mock(return_value=True)
            sensor.read = Mock(return_value=False)
            sensors.append(sensor)
        
        sensor_controller.sensor_list = sensors
        
        # Act
        readings = sensor_controller.read()
        
        # Assert
        assert all(reading['detection'] is False for reading in readings)
    
    # UT-SC-getAllSensorInfo
    def test_get_all_sensor_info(self, sensor_controller):
        """
        Test Case: getAllSensorInfo()
        Description: Verifies complete sensor information retrieval
        Reference: CRC Card for SensorController
        """
        # Arrange
        sensor1 = Mock(spec=Sensor)
        sensor1.get_id = Mock(return_value=1)
        sensor1.get_type = Mock(return_value=1)
        sensor1.get_sensor_location = Mock(return_value=[100, 150])
        sensor1.is_armed = Mock(return_value=True)
        
        sensor2 = Mock(spec=Sensor)
        sensor2.get_id = Mock(return_value=2)
        sensor2.get_type = Mock(return_value=2)
        sensor2.get_sensor_location = Mock(return_value=[200, 250])
        sensor2.is_armed = Mock(return_value=False)
        
        sensor_controller.sensor_list = [sensor1, sensor2]
        
        # Act
        info = sensor_controller.get_all_sensor_info()
        
        # Assert
        assert len(info) == 2
        assert info[0]['id'] == 1
        assert info[0]['type'] == 1
        assert info[0]['location'] == [100, 150]
        assert info[0]['armed'] is True
        assert info[1]['id'] == 2
        assert info[1]['armed'] is False
    
    def test_get_all_sensor_info_empty(self, sensor_controller):
        """
        Test Case: getAllSensorInfo() with no sensors
        Description: Verifies handling of empty sensor list
        """
        # Arrange
        sensor_controller.sensor_list = []
        
        # Act
        info = sensor_controller.get_all_sensor_info()
        
        # Assert
        assert info == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])