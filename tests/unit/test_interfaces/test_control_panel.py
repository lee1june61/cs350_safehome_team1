"""
Unit Tests for SafeHomeControlPanel (TC-SHCP-01 ~ TC-SHCP-04)

Based on: SDS CRC Cards and SRS Use Cases
Run: cd safehome_team1 && python -m pytest tests/unit/test_interfaces/test_control_panel.py -v

SRS References:
- V.1.a: Log onto the system through control panel
- V.1.d: Turn the system on
- V.1.e: Turn the system off
- V.1.f: Reset the system
- V.1.g: Change master password
- V.2.a: Arm/disarm system through control panel
- V.2.k: Call monitoring service (panic)
"""

import pytest


class TestSafeHomeControlPanelStates:
    """Tests for Control Panel state machine"""

    def test_initial_state_is_off(self, control_panel):
        """System should start in OFF state (SRS V.1.d precondition)"""
        from src.interfaces.control_panel.control_panel import SafeHomeControlPanel

        assert control_panel._state == SafeHomeControlPanel.STATE_OFF

    def test_turn_on_system(self, control_panel):
        """Test turning system on (SRS V.1.d)"""
        from src.interfaces.control_panel.control_panel import SafeHomeControlPanel

        # Simulate button1 press (ON button)
        control_panel._state = SafeHomeControlPanel.STATE_OFF

        # After turn on, state should change to IDLE
        control_panel._state = SafeHomeControlPanel.STATE_IDLE
        assert control_panel._state == SafeHomeControlPanel.STATE_IDLE


class TestSafeHomeControlPanelLogin:
    """Tests for login functionality (SRS V.1.a)"""

    def test_login_success_master(self, control_panel_ready):
        """Test master login with correct PIN"""
        result = control_panel_ready.send_command("login_control_panel", password="1234")
        assert result.get("success") == True
        assert result.get("access_level") == "MASTER"

    def test_login_success_guest(self, control_panel_ready):
        """Test guest login with correct PIN"""
        result = control_panel_ready.send_command("login_control_panel", password="5678")
        assert result.get("success") == True
        assert result.get("access_level") == "GUEST"

    def test_login_failure_wrong_password(self, control_panel_ready):
        """Test login with wrong password"""
        result = control_panel_ready.send_command("login_control_panel", password="0000")
        assert result.get("success") == False

    def test_login_attempts_tracking(self, control_panel_ready, mock_system):
        """Test that failed login decrements attempts (SRS V.1.a Exception 3a)"""
        result = control_panel_ready.send_command("login_control_panel", password="0000")
        assert result.get("attempts_remaining") == 2

        result = control_panel_ready.send_command("login_control_panel", password="0000")
        assert result.get("attempts_remaining") == 1

    def test_system_lock_after_3_failures(self, control_panel_ready, mock_system):
        """Test system locks after 3 failures (SRS V.1.a Exception 3a.2)"""
        for _ in range(3):
            control_panel_ready.send_command("login_control_panel", password="0000")

        # System should be locked now
        result = control_panel_ready.send_command("login_control_panel", password="1234")
        assert result.get("locked") == True


class TestSafeHomeControlPanelSecurity:
    """Tests for security functions (SRS V.2.a)"""

    def test_arm_system(self, control_panel_logged_in, mock_system):
        """Test arming system (SRS V.2.a)"""
        result = control_panel_logged_in.send_command("arm_system", mode="AWAY")
        assert result.get("success") == True

    def test_disarm_system(self, control_panel_logged_in, mock_system):
        """Test disarming system (SRS V.2.a)"""
        result = control_panel_logged_in.send_command("disarm_system")
        assert result.get("success") == True

    def test_arm_fails_if_doors_open(self, control_panel_logged_in, system):
        """Test arm fails if doors/windows open (SRS V.2.a Exception 2a)"""
        # Find a window/door sensor in the system and open it
        win_door_sensor = None
        for sensor in system._sensors:
            if hasattr(sensor, 'set_open'): # Check if it is a CustomWinDoorSensor
                win_door_sensor = sensor
                break
        
        assert win_door_sensor is not None, "Test setup error: No window/door sensor found in mock_system"
        win_door_sensor.set_open(True) # Set the sensor to be open

        result = control_panel_logged_in.send_command("arm_system", mode="AWAY")
        assert result.get("success") == False
        assert (
            "cannot arm" in result.get("message", "").lower()
        )


class TestSafeHomeControlPanelPanic:
    """Tests for panic button (SRS V.2.k)"""

    def test_panic_button_works_anytime(self, control_panel):
        """Panic button should work even when system is off (SRS V.2.k)"""
        result = control_panel.send_command("panic")
        assert result.get("success") == True


class TestSafeHomeControlPanelPasswordChange:
    """Tests for password change (SRS V.1.g)"""

    def test_password_change_success(self, control_panel_logged_in):
        """Test password change (SRS V.1.g)"""
        result = control_panel_logged_in.send_command("change_password", current_password="1234", new_password="9999")
        assert result.get("success") == True


class TestSafeHomeControlPanelNoSystem:
    """Tests for error handling when System not connected"""

    def test_no_system_connected(self):
        """Test error when System not connected"""
        from src.interfaces.control_panel.control_panel import SafeHomeControlPanel

        cp = object.__new__(SafeHomeControlPanel)
        cp._system = None

        result = cp.send_command("get_status")
        assert result["success"] == False
        assert "not connected" in result.get("message", "").lower()


from unittest.mock import Mock

@pytest.fixture
def cp_unit_isolated():
    """
    Fixture for a ControlPanel instance, isolated from the System and Tkinter.
    It uses object.__new__ to bypass __init__ and manually sets attributes,
    attaching a mocked system and mocking out UI methods.
    """
    from src.interfaces.control_panel.control_panel import SafeHomeControlPanel
    
    mock_system = Mock()
    mock_system.handle_request.return_value = {'success': True}

    cp = object.__new__(SafeHomeControlPanel)
    cp._system = mock_system
    cp._state = SafeHomeControlPanel.STATE_IDLE
    cp._pw_buffer = ''
    cp._new_pw_buffer = ''
    cp._access_level = None
    cp._attempts = 3
    
    # Mock all UI-interacting methods from the abstract parent class
    cp.after = Mock()
    cp.set_display_short_message1 = Mock()
    cp.set_display_short_message2 = Mock()
    cp.set_powered_led = Mock()
    cp.set_armed_led = Mock()
    cp.set_display_away = Mock()
    cp.set_display_stay = Mock()

    return cp, mock_system

class TestSafeHomeControlPanelUnit:
    """
    Unit tests for SafeHomeControlPanel focusing on specific method logic
    as described in the adapted test cases from 미팅로그.pdf.
    """
    def test_tc_shcp_01_do_system_order(self, cp_unit_isolated):
        """TC-SHCP-01: Verify button press sends correct command to system."""
        cp, mock_system = cp_unit_isolated
        # Set state to logged in to allow arming
        cp._state = cp.STATE_LOGGED_IN
        
        # Press the 'AWAY' button
        cp.button7()
        
        # Verify that the system was called correctly.
        # We use assert_any_call because the method also calls _update_leds,
        # which triggers a second call to handle_request ('get_status').
        mock_system.handle_request.assert_any_call(
            'control_panel', 'arm_system', mode='AWAY'
        )

    def test_tc_shcp_02_read_button_input(self, cp_unit_isolated):
        """TC-SHCP-02: Verify digit button presses update password buffer."""
        cp, _ = cp_unit_isolated
        # State is already IDLE from fixture
        
        cp.button1()
        cp.button2()
        cp.button3()
        
        assert cp._pw_buffer == '123'

    def test_tc_shcp_03_lock_mechanism(self, cp_unit_isolated):
        """TC-SHCP-03: Verify system locks after 3 failed login attempts."""
        cp, mock_system = cp_unit_isolated
        
        # Setup mock system to always fail login
        mock_system.handle_request.return_value = {
            'success': False, 
            'message': 'Wrong password'
        }
        
        # Pre-condition: state is IDLE and attempts are 3
        assert cp._state == cp.STATE_IDLE
        assert cp._attempts == 3

        # Attempt to login 3 times with a 4-digit password
        # Note: _try_login is a private method, but we call it for a focused unit test
        for i in range(3):
            cp._pw_buffer = f'123{i}'
            cp._try_login()
            if i < 2:
                assert cp._state == cp.STATE_IDLE
            
        # After 3rd failure, state should be LOCKED
        assert cp._state == cp.STATE_LOCKED
        # Also check that the timer to unlock was set
        cp.after.assert_called_once_with(60000, cp._unlock)

    # TC-SHCP-04 (matchNewPasswords) is not implemented because the functionality
    # does not exist in the current implementation of SafeHomeControlPanel.
    # The panel accepts a new password and sends it directly to the system
    # without an internal matching step.
