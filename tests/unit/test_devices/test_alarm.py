"""
test_alarm.py
Unit tests for Alarm class
"""

import pytest
from unittest.mock import Mock, patch
from alarm import Alarm


class TestAlarm:
    """Unit tests for Alarm class"""
    
    @pytest.fixture
    def alarm(self):
        """Fixture to create an Alarm instance"""
        alarm = Alarm()
        alarm.id = 1
        alarm.location = [150, 300]
        alarm.status = "IDLE"
        return alarm
    
    # UT-ALM-setID
    def test_set_id_valid(self, alarm):
        """
        Test Case: setID()
        Description: Verifies alarm ID is properly assigned
        Reference: CRC Card for Alarm
        """
        # Arrange
        alarm_id = 5
        
        # Act
        alarm.set_id(alarm_id)
        
        # Assert
        assert alarm.id == alarm_id
    
    def test_set_id_zero(self, alarm):
        """
        Test Case: setID() with zero
        Description: Verifies handling of zero ID
        """
        # Arrange
        alarm_id = 0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Alarm ID must be positive"):
            alarm.set_id(alarm_id)
    
    def test_set_id_negative(self, alarm):
        """
        Test Case: setID() with negative value
        Description: Verifies rejection of negative ID
        """
        # Arrange
        alarm_id = -3
        
        # Act & Assert
        with pytest.raises(ValueError, match="Alarm ID must be positive"):
            alarm.set_id(alarm_id)
    
    # UT-ALM-getId
    def test_get_id(self, alarm):
        """
        Test Case: getId()
        Description: Verifies alarm ID is correctly retrieved
        Reference: State Diagram page 35 of SDS
        """
        # Arrange
        alarm.id = 10
        
        # Act
        result = alarm.get_id()
        
        # Assert
        assert result == 10
    
    def test_get_id_after_set(self, alarm):
        """
        Test Case: getId() after setID()
        Description: Verifies ID persistence after setting
        """
        # Arrange
        alarm.set_id(7)
        
        # Act
        result = alarm.get_id()
        
        # Assert
        assert result == 7
    
    # UT-ALM-getLocation
    def test_get_location(self, alarm):
        """
        Test Case: getLocation()
        Description: Verifies alarm location is retrieved correctly
        Reference: CRC Card for Alarm
        """
        # Arrange
        alarm.location = [150, 300]
        
        # Act
        result = alarm.get_location()
        
        # Assert
        assert result == [150, 300]
        assert isinstance(result, list)
        assert len(result) == 2
    
    def test_get_location_modified(self, alarm):
        """
        Test Case: getLocation() after location change
        Description: Verifies location updates are reflected
        """
        # Arrange
        alarm.location = [100, 200]
        alarm.location = [250, 350]
        
        # Act
        result = alarm.get_location()
        
        # Assert
        assert result == [250, 350]
    
    # UT-ALM-isRinging
    def test_is_ringing_active(self, alarm):
        """
        Test Case: isRinging()
        Description: Verifies alarm reports ringing status correctly
        Reference: State Diagram for Alarm showing RINGING state
        """
        # Arrange
        alarm.status = "RINGING"
        
        # Act
        result = alarm.is_ringing()
        
        # Assert
        assert result is True
    
    def test_is_ringing_idle(self, alarm):
        """
        Test Case: isRinging() when idle
        Description: Verifies alarm reports idle status
        """
        # Arrange
        alarm.status = "IDLE"
        
        # Act
        result = alarm.is_ringing()
        
        # Assert
        assert result is False
    
    def test_is_ringing_after_activation(self, alarm):
        """
        Test Case: isRinging() after ringAlarm()
        Description: Verifies status changes after activation
        """
        # Arrange
        alarm.status = "IDLE"
        alarm.ring_alarm(True)
        
        # Act
        result = alarm.is_ringing()
        
        # Assert
        assert result is True
    
    # UT-ALM-ringAlarm
    def test_ring_alarm_activate(self, alarm):
        """
        Test Case: ringAlarm()
        Description: Verifies alarm activates when commanded
        Reference: Sequence Diagram page 58 of SDS
        """
        # Arrange
        alarm.status = "IDLE"
        with patch.object(alarm, '_activate_hardware') as mock_hardware:
            # Act
            result = alarm.ring_alarm(True)
            
            # Assert
            assert result is True
            assert alarm.status == "RINGING"
            mock_hardware.assert_called_once()
    
    def test_ring_alarm_deactivate(self, alarm):
        """
        Test Case: ringAlarm(False)
        Description: Verifies alarm stops when commanded
        """
        # Arrange
        alarm.status = "RINGING"
        with patch.object(alarm, '_deactivate_hardware') as mock_hardware:
            # Act
            result = alarm.ring_alarm(False)
            
            # Assert
            assert result is True
            assert alarm.status == "IDLE"
            mock_hardware.assert_called_once()
    
    def test_ring_alarm_already_ringing(self, alarm):
        """
        Test Case: ringAlarm() when already ringing
        Description: Verifies handling of already active alarm
        """
        # Arrange
        alarm.status = "RINGING"
        
        # Act
        result = alarm.ring_alarm(True)
        
        # Assert
        assert result is True
        assert alarm.status == "RINGING"
    
    def test_ring_alarm_intrusion_scenario(self, alarm):
        """
        Test Case: ringAlarm() during intrusion detection
        Description: Verifies alarm activation on intrusion
        Reference: CRC Card "Ring the alarm"
        """
        # Arrange
        alarm.status = "IDLE"
        intrusion_detected = True
        
        with patch.object(alarm, '_activate_hardware') as mock_hw:
            with patch.object(alarm, '_log_alarm_event') as mock_log:
                # Act
                result = alarm.ring_alarm(intrusion_detected)
                
                # Assert
                assert result is True
                assert alarm.status == "RINGING"
                mock_hw.assert_called_once()
                mock_log.assert_called_once()
    
    def test_ring_alarm_with_delay(self, alarm):
        """
        Test Case: ringAlarm() with entry delay
        Description: Verifies alarm respects delay before ringing
        Reference: SystemSettings delay time
        """
        # Arrange
        alarm.status = "IDLE"
        delay_seconds = 30
        
        with patch('time.sleep') as mock_sleep:
            with patch.object(alarm, '_activate_hardware'):
                # Act
                result = alarm.ring_alarm(True, delay=delay_seconds)
                
                # Assert
                assert result is True
                mock_sleep.assert_called_once_with(delay_seconds)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])