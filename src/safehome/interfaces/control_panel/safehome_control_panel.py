"""SafeHome Control Panel.

Main control panel with context-aware button functionality.
"""

import sys
from pathlib import Path
from typing import Optional, Any, Dict

# Project structure:
# safehome_team1/
#   ├── src/safehome/interfaces/control_panel/  ← current file
#   └── virtual_device_v3/virtual_device_v3/    ← target

# Calculate paths clearly
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[4]  # safehome_team1/
VIRTUAL_DEVICE_PATH = PROJECT_ROOT / 'virtual_device_v3' / 'virtual_device_v3'

# Add to Python path
if VIRTUAL_DEVICE_PATH.exists():
    sys.path.insert(0, str(VIRTUAL_DEVICE_PATH))
else:
    raise ImportError(
        f"Virtual device not found at: {VIRTUAL_DEVICE_PATH}\n"
        f"Please ensure virtual_device_v3 is in project root."
    )

try:
    from device.device_control_panel_abstract import (
        DeviceControlPanelAbstract
    )
except ImportError as e:
    print(f"ERROR: Cannot import DeviceControlPanelAbstract")
    print(f"Path checked: {VIRTUAL_DEVICE_PATH}")
    print(f"Error: {e}")
    sys.exit(1)

from .panel_state import PanelState
from .display_manager import DisplayManager
from .button_handler import ButtonHandler
from .constants import MSG_READY, MSG_ENTER_PASSWORD


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """SafeHome Control Panel with context-aware buttons."""
    
    def __init__(self, system: Optional[Any] = None) -> None:
        """Initialize control panel.
        
        Args:
            system: System instance (from backend team)
        """
        super().__init__()
        
        self.system = system
        self.state = PanelState()
        self.display = DisplayManager(self)
        self.button = ButtonHandler(self, system)
        
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize panel display."""
        self.display.initialize()
        self.display.show_message(MSG_READY, MSG_ENTER_PASSWORD)
    
    # ... rest of the code stays the same