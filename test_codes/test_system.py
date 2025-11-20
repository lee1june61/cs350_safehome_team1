"""
test_system.py
Unit tests for System class
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from system import System
from sensor_controller import SensorController
from camera_controller import CameraController
from login_manager import LoginManager
from configuration_manager import ConfigurationManager
from alarm import Alarm


class TestSystem:
    """Unit tests for System class"""
    
    @pytest.fixture
    def system(self):
        """Fixture to create a System instance for testing"""
        system = System()
        system.sensor_controller = Mock(spec=SensorController)
        system.camera_controller = Mock(spec=CameraController)
        system.login_manager = Mock(spec=LoginManager)
        system.config_manager = Mock(spec=ConfigurationManager)
        system.alarm = Mock(spec=Alarm)
        return system
    
    # UT-SYS-makePanic
    def test_make_panic_phone_call_success(self, system):
        """
        Test Case: makePanicPhoneCall()
        Description: Verifies that the system successfully initiates a panic call
        Reference: Sequence Diagram page 65 of SDS
        """
        # Arrange
        system.status = "ARMED"
        system.alarm.is_ringing = Mock(return_value=True)
        system.config_manager.get_monitoring_phone = Mock(return_value="911")
        
        # Act
        result = system.make_panic_phone_call()
        
        # Assert
        assert result is True
        system.config_manager.get_monitoring_phone.assert_called_once()
        
    # UT-SYS-turnOn
    def test_turn_on_success(self, system):
        """
        Test Case: turnOn()
        Description: Verifies system transitions from OFF to ON state
        Reference: Sequence Diagram page 50-51 of SDS
        """
        # Arrange
        system.status = "OFF"
        
        # Act
        result = system.turn_on()
        
        # Assert
        assert result is True
        assert system.status == "ON"
        system.config_manager.initialize.assert_called_once()
        system.sensor_controller.initialize.assert_called_once()
        system.camera_controller.initialize.assert_called_once()
    
    def test_turn_on_already_on(self, system):
        """
        Test Case: turnOn() when already ON
        Description: Verifies system handles already ON state
        """
        # Arrange
        system.status = "ON"
        
        # Act
        result = system.turn_on()
        
        # Assert
        assert result is False
        
    # UT-SYS-turnOff
    def test_turn_off_success(self, system):
        """
        Test Case: turnOff()
        Description: Verifies system properly shuts down
        Reference: Sequence Diagram page 52 of SDS
        """
        # Arrange
        system.status = "ON"
        system.is_authenticated = True
        system.access_level = "MASTER"
        
        # Act
        result = system.turn_off()
        
        # Assert
        assert result is True
        assert system.status == "OFF"
        system.sensor_controller.disarm_all_sensors.assert_called_once()
        system.camera_controller.disable_all_camera.assert_called_once()
    
    def test_turn_off_unauthorized(self, system):
        """
        Test Case: turnOff() without proper authentication
        Description: Verifies system rejects unauthorized shutdown
        """
        # Arrange
        system.status = "ON"
        system.is_authenticated = False
        
        # Act
        result = system.turn_off()
        
        # Assert
        assert result is False
        assert system.status == "ON"
    
    # UT-SYS-reset
    def test_reset_success(self, system):
        """
        Test Case: reset()
        Description: Verifies system resets to initial state
        Reference: Sequence Diagram page 53 of SDS
        """
        # Arrange
        system.status = "ON"
        system.login_tries = 3
        system.access_level = "MASTER"
        
        # Act
        result = system.reset()
        
        # Assert
        assert result is True
        assert system.login_tries == 0
        system.config_manager.reset_to_default.assert_called_once()
    
    # UT-SYS-getAlarmInfo
    def test_get_alarm_info_ringing(self, system):
        """
        Test Case: getAlarmInfo()
        Description: Verifies alarm status retrieval when alarm is ringing
        Reference: CRC Card for System and Alarm classes
        """
        # Arrange
        system.alarm.is_ringing = Mock(return_value=True)
        system.alarm.get_id = Mock(return_value=1)
        system.alarm.get_location = Mock(return_value=[100, 200])
        
        # Act
        alarm_info = system.get_alarm_info()
        
        # Assert
        assert alarm_info['is_ringing'] is True
        assert alarm_info['alarm_id'] == 1
        assert alarm_info['location'] == [100, 200]
        assert 'timestamp' in alarm_info
    
    def test_get_alarm_info_not_ringing(self, system):
        """
        Test Case: getAlarmInfo() when alarm is not active
        Description: Verifies correct status when alarm is silent
        """
        # Arrange
        system.alarm.is_ringing = Mock(return_value=False)
        
        # Act
        alarm_info = system.get_alarm_info()
        
        # Assert
        assert alarm_info['is_ringing'] is False
        assert alarm_info['timestamp'] is None
    
    # UT-SYS-armSensors
    def test_arm_sensors_valid_list(self, system):
        """
        Test Case: armSensors()
        Description: Verifies specified sensors are armed correctly
        Reference: Sequence Diagram page 55-56 of SDS
        """
        # Arrange
        system.status = "ON"
        sensor_ids = [1, 3, 5]
        system.sensor_controller.arm_sensors = Mock(return_value=True)
        
        # Act
        result = system.arm_sensors(sensor_ids)
        
        # Assert
        assert result is True
        system.sensor_controller.arm_sensors.assert_called_once_with(sensor_ids)
    
    def test_arm_sensors_empty_list(self, system):
        """
        Test Case: armSensors() with empty list
        Description: Verifies handling of empty sensor list
        """
        # Arrange
        sensor_ids = []
        
        # Act
        result = system.arm_sensors(sensor_ids)
        
        # Assert
        assert result is False
    
    # UT-SYS-disarmSensors
    def test_disarm_sensors_valid_list(self, system):
        """
        Test Case: disarmSensors()
        Description: Verifies specified sensors are disarmed correctly
        Reference: State Diagram for System
        """
        # Arrange
        system.status = "ARMED"
        sensor_ids = [2, 4]
        system.sensor_controller.disarm_sensors = Mock(return_value=True)
        
        # Act
        result = system.disarm_sensors(sensor_ids)
        
        # Assert
        assert result is True
        system.sensor_controller.disarm_sensors.assert_called_once_with(sensor_ids)
    
    # UT-SYS-readSensor
    def test_read_sensor_with_detection(self, system):
        """
        Test Case: readSensor()
        Description: Verifies system polls all active sensors
        Reference: Sequence Diagram page 58 of SDS
        """
        # Arrange
        system.status = "ARMED"
        mock_sensor_data = [
            {'id': 1, 'signal': True, 'type': 'motion'},
            {'id': 2, 'signal': False, 'type': 'door'},
            {'id': 3, 'signal': False, 'type': 'window'}
        ]
        system.sensor_controller.read = Mock(return_value=mock_sensor_data)
        
        # Act
        result = system.read_sensor()
        
        # Assert
        assert result == mock_sensor_data
        assert result[0]['signal'] is True
        system.sensor_controller.read.assert_called_once()
    
    def test_read_sensor_no_detection(self, system):
        """
        Test Case: readSensor() with no activity
        Description: Verifies normal operation with no intrusion
        """
        # Arrange
        system.status = "ARMED"
        mock_sensor_data = [
            {'id': 1, 'signal': False, 'type': 'motion'},
            {'id': 2, 'signal': False, 'type': 'door'}
        ]
        system.sensor_controller.read = Mock(return_value=mock_sensor_data)
        
        # Act
        result = system.read_sensor()
        
        # Assert
        assert all(sensor['signal'] is False for sensor in result)
    
    # UT-SYS-authenticateUser
    def test_authenticate_user_valid_credentials(self, system):
        """
        Test Case: authenticateUser()
        Description: Verifies successful user authentication
        Reference: Sequence Diagram page 47 of SDS
        """
        # Arrange
        username = "master"
        password = "1234"
        interface = "CP"
        system.login_manager.authenticate = Mock(return_value="MASTER_ACCESS")
        
        # Act
        result = system.authenticate_user(username, password, interface)
        
        # Assert
        assert result == "MASTER_ACCESS"
        assert system.login_tries == 0
        system.login_manager.authenticate.assert_called_once_with(
            username, password, interface
        )
    
    def test_authenticate_user_invalid_credentials(self, system):
        """
        Test Case: authenticateUser() with wrong password
        Description: Verifies failed authentication handling
        """
        # Arrange
        username = "master"
        password = "wrong"
        interface = "CP"
        system.login_tries = 0
        system.login_manager.authenticate = Mock(return_value=None)
        
        # Act
        result = system.authenticate_user(username, password, interface)
        
        # Assert
        assert result is None
        assert system.login_tries == 1
    
    def test_authenticate_user_max_attempts(self, system):
        """
        Test Case: authenticateUser() after max attempts
        Description: Verifies system locks after multiple failed attempts
        """
        # Arrange
        system.login_tries = 3
        
        # Act
        result = system.authenticate_user("user", "pass", "CP")
        
        # Assert
        assert result is None
        assert system.is_locked is True
    
    # UT-SYS-initSystem
    def test_init_system_success(self, system):
        """
        Test Case: initSystem()
        Description: Verifies system initializes all components
        Reference: Sequence Diagram page 50 of SDS
        """
        # Arrange
        system.config_manager = None
        system.login_manager = None
        
        # Act
        result = system.init_system()
        
        # Assert
        assert result is True
        assert system.config_manager is not None
        assert system.login_manager is not None
        assert system.sensor_controller is not None
        assert system.camera_controller is not None
    
    # UT-SYS-processMessage
    def test_process_message_valid_command(self, system):
        """
        Test Case: processMessage()
        Description: Verifies system processes incoming messages correctly
        Reference: CRC Card for System
        """
        # Arrange
        mock_stream = Mock()
        mock_message = {'command': 'ARM', 'sensors': [1, 2, 3]}
        mock_stream.read = Mock(return_value=mock_message)
        
        # Act
        result = system.process_message(mock_stream)
        
        # Assert
        assert result is True
        mock_stream.read.assert_called_once()
    
    def test_process_message_invalid_format(self, system):
        """
        Test Case: processMessage() with malformed message
        Description: Verifies error handling for invalid messages
        """
        # Arrange
        mock_stream = Mock()
        mock_stream.read = Mock(return_value=None)
        
        # Act
        result = system.process_message(mock_stream)
        
        # Assert
        assert result is False
    
    # UT-SYS-receiveMessage
    def test_receive_message_success(self, system):
        """
        Test Case: receiveMessage()
        Description: Verifies system receives messages from interfaces
        Reference: Architectural structure page 9 of SDS
        """
        # Arrange
        mock_message = {'type': 'command', 'data': 'turn_on'}
        system.message_buffer = []
        
        with patch.object(system, '_read_from_interface', return_value=mock_message):
            # Act
            result = system.receive_message()
            
            # Assert
            assert result == mock_message
            assert mock_message in system.message_buffer
    
    # UT-SYS-sendMessage
    def test_send_message_to_interface(self, system):
        """
        Test Case: sendMessage()
        Description: Verifies system sends response messages
        Reference: State Diagram for System
        """
        # Arrange
        response_data = {'status': 'success', 'message': 'System armed'}
        target_interface = "WebInterface"
        
        with patch.object(system, '_write_to_interface', return_value=True) as mock_write:
            # Act
            result = system.send_message(response_data, target_interface)
            
            # Assert
            assert result is True
            mock_write.assert_called_once_with(response_data, target_interface)
    
    # UT-SYS-armBySafeHomeMode
    def test_arm_by_safe_home_mode_home(self, system):
        """
        Test Case: armBySafeHomeMode()
        Description: Verifies sensors armed according to HOME mode
        Reference: Sequence Diagram page 63 of SDS
        """
        # Arrange
        mode = 1  # HOME mode
        system.status = "ON"
        home_mode_sensors = [1, 3, 5]
        system.config_manager.get_mode_sensors = Mock(return_value=home_mode_sensors)
        system.sensor_controller.arm_sensors = Mock(return_value=True)
        
        # Act
        result = system.arm_by_safe_home_mode(mode)
        
        # Assert
        assert result is True
        system.config_manager.get_mode_sensors.assert_called_once_with(mode)
        system.sensor_controller.arm_sensors.assert_called_once_with(home_mode_sensors)
    
    def test_arm_by_safe_home_mode_invalid(self, system):
        """
        Test Case: armBySafeHomeMode() with invalid mode
        Description: Verifies handling of invalid mode ID
        """
        # Arrange
        mode = 99  # Invalid mode
        system.config_manager.get_mode_sensors = Mock(return_value=None)
        
        # Act
        result = system.arm_by_safe_home_mode(mode)
        
        # Assert
        assert result is False
    
    # UT-SYS-disarmBySafeHomeMode
    def test_disarm_by_safe_home_mode_away(self, system):
        """
        Test Case: disarmBySafeHomeMode()
        Description: Verifies sensors disarmed by mode
        Reference: State Diagram for System and SafeHomeMode
        """
        # Arrange
        mode = 2  # AWAY mode
        system.status = "ARMED"
        away_mode_sensors = [1, 2, 3, 4, 5]
        system.config_manager.get_mode_sensors = Mock(return_value=away_mode_sensors)
        system.sensor_controller.disarm_sensors = Mock(return_value=True)
        
        # Act
        result = system.disarm_by_safe_home_mode(mode)
        
        # Assert
        assert result is True
        system.sensor_controller.disarm_sensors.assert_called_once_with(away_mode_sensors)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])