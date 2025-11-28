"""Pytest fixtures for interface tests - uses real System class"""
import pytest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from src.core.system import System


@pytest.fixture
def system():
    """Create a fresh System for each test"""
    return System()


@pytest.fixture
def mock_system(system):
    """Alias for the system fixture, ensuring the same instance is used."""
    return system


@pytest.fixture
def web_interface(system):
    """Create WebInterface without GUI initialization"""
    from src.interfaces.web_interface import WebInterface
    wi = object.__new__(WebInterface)
    wi._system = system
    wi._pages = {}
    wi._current_page = None
    wi._context = {}
    return wi


@pytest.fixture
def control_panel(system):
    """Create ControlPanel in STATE_OFF (SRS V.1.d)"""
    from src.interfaces.control_panel.control_panel import SafeHomeControlPanel
    cp = object.__new__(SafeHomeControlPanel)
    cp._system = system
    cp._state = SafeHomeControlPanel.STATE_OFF
    cp._pw_buffer = ''
    cp._new_pw_buffer = ''
    cp._access_level = None
    cp._attempts = 3
    return cp


@pytest.fixture
def control_panel_ready(system):
    """ControlPanel in IDLE state (system on, ready for login)"""
    from src.interfaces.control_panel.control_panel import SafeHomeControlPanel
    cp = object.__new__(SafeHomeControlPanel)
    cp._system = system
    cp._state = SafeHomeControlPanel.STATE_IDLE
    cp._pw_buffer = ''
    cp._new_pw_buffer = ''
    cp._access_level = None
    cp._attempts = 3
    return cp


@pytest.fixture
def control_panel_logged_in(system):
    """ControlPanel in LOGGED_IN state"""
    from src.interfaces.control_panel.control_panel import SafeHomeControlPanel
    cp = object.__new__(SafeHomeControlPanel)
    cp._system = system
    cp._state = SafeHomeControlPanel.STATE_LOGGED_IN
    cp._pw_buffer = ''
    cp._new_pw_buffer = ''
    cp._access_level = 'MASTER'
    cp._attempts = 3
    return cp
