"""
test_window_door_sensor.py
Unit tests for WindowDoorSensor class
"""

import pytest
from unittest.mock import Mock, patch
from window_door_sensor import WindowDoorSensor


class TestWindowDoorSensor:
    """Unit tests for WindowDoorSensor class"""
    
    @pytest.fixture
    def window_door_sensor(self):
        """Fixture to create a WindowDoorSensor instance"""
        sensor = WindowDoorSensor()
        sensor.id = 1
        sensor.location = [100, 150]
        return sensor
    
    # UT-WDS-isOpen
    def test_is_open_door_opened(self, window_door_sensor):
        """
        Test Case: isOpen()
        Description: Verifies sensor detects open state correctly
        Reference: CRC Card for WindowDoorSensor, Class Diagram page 16
        """
        # Arrange
        window_door_sensor.status = "ARMED"
        with patch.object(window_door_sensor, '_read_hardware', return_value=True):
            # Act
            result = window_door_sensor.is_open()
            
            # Assert
            assert result is True
    
    def test_is_open_door_closed(self, window_door_sensor):
        """
        Test Case: isOpen() when door is closed
        Description: Verifies sensor reports closed state
        """
        # Arrange
        window_door_sensor.status = "ARMED"
        with patch.object(window_door_sensor, '_read_hardware', return_value=False):
            # Act
            result = window_door_sensor.is_open()
            
            # Assert
            assert result is False
    
    def test_is_open_sensor_disarmed(self, window_door_sensor):
        """
        Test Case: isOpen() when sensor is disarmed
        Description: Verifies disarmed sensor behavior
        """
        # Arrange
        window_door_sensor.status = "DISARMED"
        with patch.object(window_door_sensor, '_read_hardware', return_value=True):
            # Act
            result = window_door_sensor.is_open()
            
            # Assert
            assert result is False  # Disarmed sensors don't report status
    
    def test_is_open_window_sensor(self, window_door_sensor):
        """
        Test Case: isOpen() for window sensor
        Description: Verifies window sensor detects open state
        """
        # Arrange
        window_door_sensor.type = 1  # WINDOW
        window_door_sensor.status = "ARMED"
        with patch.object(window_door_sensor, '_read_hardware', return_value=True):
            # Act
            result = window_door_sensor.is_open()
            
            # Assert
            assert result is True
    
    def test_is_open_integration_with_hardware(self, window_door_sensor):
        """
        Test Case: isOpen() with hardware integration
        Description: Verifies connection to WinDoorSensor hardware
        Reference: CRC Card "Connect to window/door sensor hardware"
        """
        # Arrange
        window_door_sensor.status = "ARMED"
        mock_hardware = Mock()
        mock_hardware.read = Mock(return_value=True)
        window_door_sensor.hardware = mock_hardware
        
        # Act
        result = window_door_sensor.is_open()
        
        # Assert
        assert result is True
        mock_hardware.read.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])