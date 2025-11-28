"""
SafeHome Interfaces Package

Web interface and control panel implementations.
All UI-related code is now consolidated here (replacing src/ui/).

Structure:
- components/: Reusable UI components (FloorPlan, DeviceIcon, etc.)
- control_panel/: Control Panel implementation
  - screens/: Control Panel screen classes
- pages/: Web Interface pages
  - dialogs/: Dialog windows
- web_interface.py: Main Web Interface class
- page_registry.py: Page class registry
"""
from .web_interface import WebInterface, run_web_interface
from .page_registry import PAGE_CLASSES, get_page_class, get_all_page_names
from .control_panel import SafeHomeControlPanel, run_control_panel

__all__ = [
    'WebInterface',
    'run_web_interface',
    'PAGE_CLASSES',
    'get_page_class',
    'get_all_page_names',
    'SafeHomeControlPanel',
    'run_control_panel',
]
