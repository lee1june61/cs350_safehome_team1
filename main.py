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
    
    root = tk.Tk()
    root.title("SafeHome Main Controller")
    root.geometry("350x200")
    root.configure(bg='#2c3e50')
    
    tk.Label(root, text="SafeHome System", font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50').pack(pady=20)
    tk.Label(root, text="Control Panel: Separate Window\nWeb Interface: Separate Window",
             font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50').pack(pady=10)
    
    def quit_all():
        print("\n[INFO] Shutting down SafeHome...")
        system.turn_off()
        root.quit()
        root.destroy()
    
    tk.Button(root, text="Quit All", command=quit_all, bg='#e74c3c', fg='white',
              font=('Arial', 11, 'bold'), width=15).pack(pady=20)
    
    try:
        control_panel = SafeHomeControlPanel(root, system)
        control_panel.title("SafeHome Control Panel")
        print("[OK] Control Panel created (OFF state - press 1 to start)")
    except Exception as e:
        print(f"[ERROR] Control Panel: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        system.turn_on()
        web_interface = WebInterface(system, root)
        web_interface.title("SafeHome Web Interface")
        print("[OK] Web Interface created")
    except Exception as e:
        print(f"[ERROR] Web Interface: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("SafeHome Ready!")
    print("=" * 60)
    print("""
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
""")
    print("=" * 60)
    
    root.mainloop()


if __name__ == "__main__":
    main()
