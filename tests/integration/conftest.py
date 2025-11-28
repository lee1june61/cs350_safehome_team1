"""
Integration test fixtures for SafeHome system.
Based on SafeHome_Integration_Test_Cases.md
"""
import pytest
from src.core.system import System


@pytest.fixture
def system():
    """Create a fresh System instance for each test."""
    return System()


@pytest.fixture
def system_on(system):
    """System that has been turned on."""
    system.handle_request("control_panel", "turn_on")
    return system


@pytest.fixture
def system_logged_in_master(system_on):
    """System logged in with master password via control panel."""
    system_on.handle_request(
        "control_panel", "login_control_panel", password="1234"
    )
    return system_on


@pytest.fixture
def system_logged_in_guest(system_on):
    """System logged in with guest password via control panel."""
    system_on.handle_request(
        "control_panel", "login_control_panel", password="5678"
    )
    return system_on


@pytest.fixture
def system_web_logged_in(system_on):
    """System logged in via web interface."""
    system_on.handle_request(
        "web", "web_login", user_id="homeowner", password="password"
    )
    return system_on


@pytest.fixture
def system_armed_away(system_logged_in_master):
    """System armed in AWAY mode."""
    # Close all doors/windows first
    for sensor in system_logged_in_master._sensors:
        if hasattr(sensor, "set_open"):
            sensor.set_open(False)
    system_logged_in_master.handle_request(
        "control_panel", "arm_system", mode="AWAY"
    )
    return system_logged_in_master

