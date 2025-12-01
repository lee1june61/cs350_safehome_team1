"""Pytest fixtures for interface tests - uses real System class"""
import os
import sys

import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.configuration.storage_manager import StorageManager
from src.core.system import System


@pytest.fixture
def system(tmp_path):
    """Create a fresh System with an isolated database for each test."""
    StorageManager._instance = None  # reset singleton for clean DB
    db_path = tmp_path / "interface_tests.db"
    sys_inst = System(str(db_path))
    yield sys_inst
    storage = getattr(sys_inst, "_storage", None)
    if storage:
        storage.disconnect()


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
    system.handle_request("control_panel", "login_control_panel", password="1234")
    return cp
