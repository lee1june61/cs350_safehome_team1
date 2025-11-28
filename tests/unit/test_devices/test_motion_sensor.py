"""
test_sensor.py
Unit tests for Sensor class
"""

import pytest
from unittest.mock import Mock
from src.devices.sensors.sensor import Sensor


class TestSensor:
    """Unit tests for Sensor class"""
    
    @pytest.fixture
    def sensor(self):
        """Fixture to create a Sensor instance"""
        return Sensor()
    
    # UT-SEN-isArmed
    def test_is_armed_true(self, sensor):
        """
        Test Case: isArmed()
        Description: Verifies sensor reports armed status correctly
        Reference: State Diagram page 39 of SDS
        """
        # Arrange
        sensor.status = "ARMED"
        
        # Act
        result = sensor.is_armed()
        
        # Assert
        assert result is True
    
    def test_is_armed_false(self, sensor):
        """
        Test Case: isArmed() when disarmed
        Description: Verifies sensor reports disarmed status
        """
        # Arrange
        sensor.status = "DISARMED"
        
        # Act
        result = sensor.is_armed()
        
        # Assert
        assert result is False
    
    # UT-SEN-read
    def test_read_detection(self, sensor):
        """
        Test Case: read()
        Description: Verifies sensor reads signal from hardware
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor.status = "ARMED"
        sensor.hardware_signal = True  # Simulated hardware detection
        
        # Act
        result = sensor.read()
        
        # Assert
        assert result is True
    
    def test_read_no_detection(self, sensor):
        """
        Test Case: read() with no activity
        Description: Verifies normal operation with clear signal
        """
        # Arrange
        sensor.status = "ARMED"
        sensor.hardware_signal = False
        
        # Act
        result = sensor.read()
        
        # Assert
        assert result is False
    
    def test_read_disarmed(self, sensor):
        """
        Test Case: read() when sensor is disarmed
        Description: Verifies disarmed sensor doesn't report activity
        """
        # Arrange
        sensor.status = "DISARMED"
        sensor.hardware_signal = True
        
        # Act
        result = sensor.read()
        
        # Assert
        assert result is False  # Disarmed sensors don't trigger
    
    # UT-SEN-arm
    def test_arm_success(self, sensor):
        """
        Test Case: arm()
        Description: Verifies sensor transitions to armed state
        Reference: State Diagram for Sensor
        """
        # Arrange
        sensor.status = "DISARMED"
        
        # Act
        result = sensor.arm()
        
        # Assert
        assert result is True
        assert sensor.status == "ARMED"
    
    def test_arm_already_armed(self, sensor):
        """
        Test Case: arm() when already armed
        Description: Verifies handling of already armed sensor
        """
        # Arrange
        sensor.status = "ARMED"
        
        # Act
        result = sensor.arm()
        
        # Assert
        assert result is True
        assert sensor.status == "ARMED"
    
    # UT-SEN-disarm
    def test_disarm_success(self, sensor):
        """
        Test Case: disarm()
        Description: Verifies sensor transitions to disarmed state
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor.status = "ARMED"
        
        # Act
        result = sensor.disarm()
        
        # Assert
        assert result is True
        assert sensor.status == "DISARMED"
    
    def test_disarm_already_disarmed(self, sensor):
        """
        Test Case: disarm() when already disarmed
        Description: Verifies handling of already disarmed sensor
        """
        # Arrange
        sensor.status = "DISARMED"
        
        # Act
        result = sensor.disarm()
        
        # Assert
        assert result is True
        assert sensor.status == "DISARMED"
    
    # UT-SEN-setID
    def test_set_id(self, sensor):
        """
        Test Case: setID()
        Description: Verifies sensor ID is properly assigned
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor_id = 10
        
        # Act
        sensor.set_id(sensor_id)
        
        # Assert
        assert sensor.id == sensor_id
    
    def test_set_id_negative(self, sensor):
        """
        Test Case: setID() with negative value
        Description: Verifies handling of invalid ID
        """
        # Arrange
        sensor_id = -5
        
        # Act & Assert
        with pytest.raises(ValueError):
            sensor.set_id(sensor_id)
    
    # UT-SEN-getID
    def test_get_id(self, sensor):
        """
        Test Case: getID()
        Description: Verifies sensor ID is correctly retrieved
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor.id = 15
        
        # Act
        result = sensor.get_id()
        
        # Assert
        assert result == 15
    
    # UT-SEN-setType
    def test_set_type_window_door(self, sensor):
        """
        Test Case: setType()
        Description: Verifies sensor type is assigned correctly
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor_type = 1  # WINDOW_DOOR
        
        # Act
        sensor.set_type(sensor_type)
        
        # Assert
        assert sensor.type == sensor_type
    
    def test_set_type_motion(self, sensor):
        """
        Test Case: setType() for motion sensor
        Description: Verifies motion sensor type assignment
        """
        # Arrange
        sensor_type = 2  # MOTION
        
        # Act
        sensor.set_type(sensor_type)
        
        # Assert
        assert sensor.type == 2
    
    # UT-SEN-getType
    def test_get_type(self, sensor):
        """
        Test Case: getType()
        Description: Verifies sensor type is retrieved correctly
        Reference: CRC Card for Sensor
        """
        # Arrange
        sensor.type = 1
        
        # Act
        result = sensor.get_type()
        
        # Assert
        assert result == 1
    
    # UT-SEN-setSensorLocation
    def test_set_sensor_location(self, sensor):
        """
        Test Case: setSensorLocation()
        Description: Verifies sensor location coordinates are set
        Reference: CRC Card for Sensor
        """
        # Arrange
        location = [250, 350]
        
        # Act
        sensor.set_sensor_location(location)
        
        # Assert
        assert sensor.location == location
    
    def test_set_sensor_location_invalid(self, sensor):
        """
        Test Case: setSensorLocation() with invalid coordinates
        Description: Verifies handling of out-of-bounds location
        """
        # Arrange
        location = [-10, 5000]
        
        # Act & Assert
        with pytest.raises(ValueError):
            sensor.set_sensor_location(location)
    
    # UT-SEN-getSensorLocation
    def test_get_sensor_location(self, sensor):
        """
        Test Case: getSensorLocation()
        Description: Verifies sensor location is retrieved correctly
        Reference: Class Diagram page 16 of SDS
        """
        # Arrange
        sensor.location = [100, 200]
        
        # Act
        result = sensor.get_sensor_location()
        
        # Assert
        assert result == [100, 200]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
