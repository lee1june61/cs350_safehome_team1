"""
Unit Tests for UI Components (FloorPlan)

Run: cd safehome_team1 && python -m pytest tests/unit/test_interfaces/test_components.py -v
"""
import pytest
from unittest.mock import Mock

# The DeviceIcon class is no longer used by the current FloorPlan implementation.
# These tests are commented out or removed to reflect the current state of the code.
# class TestDeviceIcon: ...

class TestFloorPlan:
    """Tests for the refactored FloorPlan component"""
    
    @pytest.fixture
    def floor_plan(self):
        """Fixture to create a FloorPlan instance."""
        from src.interfaces.components.floor_plan import FloorPlan
        # Mock the tkinter parent widget
        mock_parent = Mock()
        return FloorPlan(mock_parent, width=400, height=300)

    def test_floor_plan_creation(self, floor_plan):
        """Test FloorPlan initialization."""
        assert floor_plan._w == 400
        assert floor_plan._h == 300
        assert floor_plan._canvas is None

    def test_get_devices(self, floor_plan):
        """Test getting device IDs from the static list."""
        # Test getting all devices
        all_devices = floor_plan.get_devices()
        assert len(all_devices) > 0
        assert 'C1' in all_devices
        assert 'S1' in all_devices
        assert 'M1' in all_devices

        # Test filtering by type
        cameras = floor_plan.get_devices(dtype='camera')
        assert all(d.startswith('C') for d in cameras)
        assert len(cameras) == 3

    def test_get_sensors(self, floor_plan):
        """Test getting all sensor types (sensor + motion)."""
        sensors = floor_plan.get_sensors()
        assert 'S1' in sensors
        assert 'M1' in sensors
        assert 'C1' not in sensors
        assert len(sensors) == 8

    def test_selection_methods(self, floor_plan):
        """Test selection and highlight functionality."""
        # Initially, no devices are selected
        assert floor_plan.get_selected() == []

        # Select a list of devices
        devices_to_select = ['S1', 'M2']
        floor_plan.set_selected(devices_to_select)
        
        # Check if they are correctly reported as selected
        selected = floor_plan.get_selected()
        assert set(selected) == set(devices_to_select)

        # Clear selection
        floor_plan.clear_selection()
        assert floor_plan.get_selected() == []

    def test_armed_state(self, floor_plan):
        """Test setting and checking armed states of devices."""
        # Initially, no device state is set
        assert not floor_plan._states.get('S1', False)

        # Arm a device
        floor_plan.set_armed('S1', True)
        assert floor_plan._states.get('S1') == True

        # Disarm a device
        floor_plan.set_armed('S1', False)
        assert floor_plan._states.get('S1') == False

