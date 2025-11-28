#!/usr/bin/env python3
"""
SafeHome Main Runner
====================
Usage: python main.py

Runs Control Panel and Web Interface simultaneously.

SRS Flow:
1. System starts in OFF state
2. Control Panel shows "Press 1 to start"
3. User presses 1 (ON button) to boot system
4. After boot, user can enter password to login
5. Web Interface is available independently
"""
import sys
import os
import tkinter as tk

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.system import System
from src.interfaces.control_panel import SafeHomeControlPanel
from src.interfaces.web_interface import WebInterface


def main():
    print("=" * 60)
    print("SafeHome System")
    print("=" * 60)

    system = System()
    print(f"[OK] System created (State: {system._state})")

    # Root is hidden; only Control Panel and Web Interface windows are shown.
    root = tk.Tk()
    root.withdraw()

    windows = []
    shutting_down = {"value": False}

    def quit_all():
        """Shut down system and close all windows."""
        if shutting_down["value"]:
            return
        shutting_down["value"] = True
        print("\n[INFO] Shutting down SafeHome...")
        try:
            system.turn_off()
        except Exception as exc:  # pragma: no cover
            print(f"[WARN] Failed to turn off cleanly: {exc}")
        for win in list(windows):
            if win.winfo_exists():
                win.destroy()
        root.quit()

    try:
        control_panel = SafeHomeControlPanel(root, system)
        control_panel.title("SafeHome Control Panel")
        control_panel.protocol("WM_DELETE_WINDOW", quit_all)
        windows.append(control_panel)
        print("[OK] Control Panel created (OFF state - press 1 to start)")
    except Exception as e:  # pragma: no cover
        print(f"[ERROR] Control Panel: {e}")
        import traceback

        traceback.print_exc()

    try:
        system.turn_on()
        web_interface = WebInterface(system, root)
        web_interface.title("SafeHome Web Interface")
        web_interface.protocol("WM_DELETE_WINDOW", quit_all)
        windows.append(web_interface)
        print("[OK] Web Interface created")
    except Exception as e:  # pragma: no cover
        print(f"[ERROR] Web Interface: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("SafeHome Ready!")
    print("=" * 60)
    print(
        """
CONTROL PANEL USAGE (SRS V.1):
  1. Press '1' (ON) to start the system
  2. Enter 4-digit password:
     - Master: 1234
     - Guest: 5678
  3. After login:
     - 7 = AWAY (arm all)
     - 8 = HOME (disarm)
     - 9 = CODE (change password)
     - 3 = OFF (turn off system)
     - 6 = RESET
  4. PANIC: Press '*' or '#' anytime

WEB INTERFACE USAGE (SRS V.1.b):
  - User ID: admin
  - Password 1: password
  - Password 2: password
  - Verify identity with phone/address for security functions
"""
    )
    print("=" * 60)

    try:
        root.mainloop()
    finally:
        root.destroy()


if __name__ == "__main__":
    main()
