"""
SafeHome Interfaces Package

Web interface and control panel implementations.

Control Panel uses DeviceControlPanelAbstract from virtual_device_v4.
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
