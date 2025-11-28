"""
Integration Tests: Common Functions (IT-001 ~ IT-007)
Based on SafeHome_Integration_Test_Cases.md

Tests:
- IT-001: Log onto system through control panel
- IT-002: Log onto system through web browser
- IT-003: Configure system setting
- IT-004: Turn the system on
- IT-005: Turn the system off
- IT-006: Reset the system
- IT-007: Change master password through control panel
"""
import pytest


class TestIT001ControlPanelLogin:
    """IT-001: Log onto the system through control panel."""

    def test_master_login_success(self, system_on):
        """Normal: Master password login succeeds."""
        result = system_on.handle_request(
            "control_panel", "login_control_panel", password="1234"
        )
        assert result["success"] is True
        assert result["access_level"] == "MASTER"

    def test_guest_login_success(self, system_on):
        """Normal: Guest password login succeeds."""
        result = system_on.handle_request(
            "control_panel", "login_control_panel", password="5678"
        )
        assert result["success"] is True
        assert result["access_level"] == "GUEST"

    def test_wrong_password_rejected(self, system_on):
        """Exception 3a.1: Incorrect password asks again."""
        result = system_on.handle_request(
            "control_panel", "login_control_panel", password="0000"
        )
        assert result["success"] is False
        assert result["attempts_remaining"] == 2

    def test_lockout_after_3_failures(self, system_on):
        """Exception 3a.2: Lock after 3 failures."""
        for _ in range(3):
            system_on.handle_request(
                "control_panel", "login_control_panel", password="0000"
            )

        result = system_on.handle_request(
            "control_panel", "login_control_panel", password="1234"
        )
        assert result.get("locked") is True


class TestIT002WebBrowserLogin:
    """IT-002: Log onto the System through web browser."""

    def test_web_login_success(self, system_on):
        """Normal: Web login with valid credentials."""
        result = system_on.handle_request(
            "web", "web_login", user_id="homeowner", password="password"
        )
        assert result["success"] is True

    def test_web_login_wrong_password(self, system_on):
        """Exception 4a: Wrong password rejected."""
        result = system_on.handle_request(
            "web", "web_login", user_id="homeowner", password="wrong"
        )
        assert result["success"] is False


class TestIT003ConfigureSystemSetting:
    """IT-003: Configure system setting."""

    def test_configure_delay_time(self, system_web_logged_in):
        """Normal: Set delay time >= 5 minutes."""
        result = system_web_logged_in.handle_request(
            "web", "configure_system_settings",
            delay_time=10, monitor_phone="123-456-7890"
        )
        assert result["success"] is True

    def test_get_settings(self, system_web_logged_in):
        """Normal: Get current system settings."""
        result = system_web_logged_in.handle_request("web", "get_system_settings")
        assert result["success"] is True
        assert "delay_time" in result["data"]
        assert "monitor_phone" in result["data"]


class TestIT004TurnSystemOn:
    """IT-004: Turn the system on."""

    def test_turn_on_from_off(self, system):
        """Normal: Turn on system from OFF state."""
        assert system._state == "OFF"
        result = system.handle_request("control_panel", "turn_on")
        assert result["success"] is True
        assert system._state == "READY"

    def test_turn_on_already_on(self, system_on):
        """System already on returns success."""
        result = system_on.handle_request("control_panel", "turn_on")
        # Should succeed or indicate already on
        assert system_on._state == "READY"


class TestIT005TurnSystemOff:
    """IT-005: Turn the system off."""

    def test_turn_off_logged_in(self, system_logged_in_master):
        """Normal: Turn off after login."""
        result = system_logged_in_master.handle_request("control_panel", "turn_off")
        assert result["success"] is True
        assert system_logged_in_master._state == "OFF"


class TestIT006ResetSystem:
    """IT-006: Reset the system."""

    def test_reset_system(self, system_logged_in_master):
        """Normal: Reset system after login."""
        result = system_logged_in_master.handle_request("control_panel", "reset_system")
        assert result["success"] is True


class TestIT007ChangePassword:
    """IT-007: Change master password through control panel."""

    def test_change_password_success(self, system_logged_in_master):
        """Normal: Change master password with correct current."""
        result = system_logged_in_master.handle_request(
            "control_panel", "change_password",
            current_password="1234", new_password="9999"
        )
        assert result["success"] is True

        # Verify new password works
        system_logged_in_master.handle_request("control_panel", "turn_off")
        system_logged_in_master.handle_request("control_panel", "turn_on")
        login_result = system_logged_in_master.handle_request(
            "control_panel", "login_control_panel", password="9999"
        )
        assert login_result["success"] is True

    def test_change_password_wrong_current(self, system_logged_in_master):
        """Exception 4a: Wrong current password."""
        result = system_logged_in_master.handle_request(
            "control_panel", "change_password",
            current_password="0000", new_password="9999"
        )
        assert result["success"] is False

