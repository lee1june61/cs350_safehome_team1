"""
Test script for SafeHome Control Panel.
Run this to test the UI with skeleton system.
"""
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core import System
from src.interfaces.control_panel import SafeHomeControlPanel


def main():
    """Main test function."""
    print("=" * 60)
    print("SafeHome Control Panel Test")
    print("=" * 60)
    print()
    print("Initializing SafeHome System...")
    
    # Create system instance (with skeleton methods)
    system = System()
    system.turn_on()
    
    print("System initialized successfully!")
    print("Starting Control Panel GUI...")
    print()
    print("Test Login: Use password '1234'")
    print("=" * 60)
    print()
    
    # Create and start control panel
    panel = SafeHomeControlPanel(system)
    panel.start()


if __name__ == "__main__":
    main()