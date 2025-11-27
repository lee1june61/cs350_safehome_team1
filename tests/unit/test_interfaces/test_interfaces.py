"""
Legacy test file - imports from split modules for backward compatibility

Tests have been split into separate files:
- test_web_interface.py
- test_control_panel.py  
- test_components.py
- test_integration.py

Run: cd safehome_team1 && python -m pytest tests/unit/test_interfaces -v
"""
# Re-export all test classes for backward compatibility
from .test_web_interface import TestWebInterface
from .test_control_panel import TestSafeHomeControlPanel
from .test_components import TestDeviceIcon, TestFloorPlan
from .test_integration import (
    TestLoginFlow, TestSecurityFlow, 
    TestCameraFlow, TestSystemSettings, TestMockSystem
)

__all__ = [
    'TestWebInterface',
    'TestSafeHomeControlPanel', 
    'TestDeviceIcon',
    'TestFloorPlan',
    'TestLoginFlow',
    'TestSecurityFlow',
    'TestCameraFlow',
    'TestSystemSettings',
    'TestMockSystem',
]


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
