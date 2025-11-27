"""Main panel controller."""

import tkinter as tk
from tkinter import messagebox
from typing import Optional
from ..models.panel_state import PanelState
from ..views.system_off_screen import SystemOffScreen
from ..views.booting_screen import BootingScreen
from ..views.login_screen import LoginScreen
from ..views.main_screen import MainScreen
from ..services.security_service import SecurityService
from ..services.device_service import DeviceService
from ..services.zone_service import ZoneService
from ..services.resource_loader import ResourceLoader
from ..config.ui_config import UIConfig


class PanelController:
    """Main controller for control panel.

    Coordinates between views, services, and system.
    Following MVP pattern.
    """

    def __init__(self, system):
        """Initialize panel controller.

        Args:
            system: SafeHome system instance
        """
        self.system = system

        # Services
        self.security_service = SecurityService(system)
        self.device_service = DeviceService(system)
        self.zone_service = ZoneService(system)
        self.resource_loader = ResourceLoader()

        # State
        self._state = PanelState.SYSTEM_OFF
        self._current_user: Optional[str] = None

        # UI
        self._window: Optional[tk.Tk] = None
        self._current_screen = None

        # Sub-controllers
        self.floor_plan_controller = None
        self.device_controller = None
        self.zone_controller = None

    def start(self):
        """Start the control panel."""
        self._setup_window()
        self._transition_to(PanelState.SYSTEM_OFF)
        self._window.mainloop()

    def stop(self):
        """Stop the control panel."""
        if self._window:
            self._window.quit()

    def _setup_window(self):
        """Setup main window."""
        self._window = tk.Tk()
        self._window.title(UIConfig.WINDOW_TITLE)
        self._window.geometry(f"{UIConfig.WINDOW_WIDTH}x{UIConfig.WINDOW_HEIGHT}")
        self._window.configure(bg=UIConfig.WINDOW_BG)
        self._window.protocol("WM_DELETE_WINDOW", self.stop)

    def _transition_to(self, new_state: PanelState):
        """Transition to new state.

        Args:
            new_state: Target state
        """
        self._state = new_state
        self._show_screen_for_state()

    def _show_screen_for_state(self):
        """Show appropriate screen for current state."""
        # Destroy current screen
        if self._current_screen:
            self._current_screen.destroy()

        # Create and show new screen
        if self._state == PanelState.SYSTEM_OFF:
            self._show_system_off()
        elif self._state == PanelState.BOOTING:
            self._show_booting()
        elif self._state == PanelState.READY:
            self._show_login()
        elif self._state == PanelState.LOGGED_IN:
            self._show_main()

    def _show_system_off(self):
        """Show system OFF screen."""
        self._current_screen = SystemOffScreen(
            self._window, on_power_on=self._handle_power_on
        )
        self._current_screen.show()

    def _show_booting(self):
        """Show booting screen."""
        self._current_screen = BootingScreen(self._window)
        self._current_screen.show()

        # Auto-transition to READY after delay
        self._window.after(
            UIConfig.BOOT_DELAY_MS, lambda: self._transition_to(PanelState.READY)
        )

    def _show_login(self):
        """Show login screen."""
        self._current_screen = LoginScreen(
            self._window,
            on_submit=self._handle_login_submit,
            on_keypad_press=lambda key: None,  # Handled internally
        )
        self._current_screen.show()

    def _show_main(self):
        """Show main screen."""
        # Initialize devices
        devices = self.device_service.initialize_devices()

        # Create main screen
        self._current_screen = MainScreen(
            self._window,
            username=self._current_user or "Master",
            on_logout=self._handle_logout,
        )
        self._current_screen.show()

        # Load floor plan
        image, photo = self.resource_loader.load_floor_plan()
        if image and photo:
            self._current_screen.floor_plan_canvas.set_floor_plan(image, photo)

        # Initialize sub-controllers (will do this next)
        from .floor_plan_controller import FloorPlanController
        from .device_controller import DeviceController
        from .zone_controller import ZoneController

        self.floor_plan_controller = FloorPlanController(
            self._current_screen.floor_plan_canvas, self.device_service
        )

        self.device_controller = DeviceController(
            self._window, self.device_service, self.system
        )

        self.zone_controller = ZoneController(
            self._window, self.zone_service, self.device_service
        )

        # Connect floor plan events to device controller
        self.floor_plan_controller.on_device_click = (
            self.device_controller.show_device_window
        )

        # Connect control buttons
        buttons = self._current_screen.control_buttons
        buttons.on_security_mode = self._handle_security_mode
        buttons.on_create_zone = self.zone_controller.start_zone_creation
        buttons.on_manage_zones = self._handle_manage_zones
        buttons.on_all_cameras = self._handle_all_cameras
        buttons.on_all_sensors = self._handle_all_sensors
        buttons.on_settings = self._handle_settings
        buttons.on_view_log = self._handle_view_log
        buttons.on_change_password = self._handle_change_password
        buttons.on_panic = self._handle_panic
        buttons.on_power_off = self._handle_power_off

        # Initial draw
        self.floor_plan_controller.draw()

        # Update status
        mode = self.security_service.get_security_mode()
        self._current_screen.update_status(f"Mode: {mode} | Ready")

    # Event handlers

    def _handle_power_on(self):
        """Handle power on."""
        self.system.turn_on()
        self._transition_to(PanelState.BOOTING)

    def _handle_login_submit(self, password: str):
        """Handle login submission.

        Args:
            password: Entered password
        """
        if len(password) != UIConfig.PASSWORD_LENGTH:
            messagebox.showerror(
                "Error", f"Password must be {UIConfig.PASSWORD_LENGTH} digits"
            )
            return

        if self.security_service.login(password):
            self._current_user = "Master"
            self._transition_to(PanelState.LOGGED_IN)
        else:
            messagebox.showerror("Login Failed", "Invalid password")
            self._current_screen.clear_password()

    def _handle_logout(self):
        """Handle logout."""
        self.security_service.logout()
        self._current_user = None
        self._transition_to(PanelState.READY)

    def _handle_security_mode(self, mode: str):
        """Handle security mode change.

        Args:
            mode: Security mode
        """
        if self.security_service.set_security_mode(mode):
            self._current_screen.update_status(f"Mode: {mode}")
            messagebox.showinfo("Mode Changed", f"Security mode set to: {mode}")
            self.floor_plan_controller.draw()  # Refresh display

    def _handle_manage_zones(self):
        """Handle manage zones."""
        zones = self.zone_service.get_all_zones()
        msg = "Safety Zones:\n\n"
        if zones:
            for zone in zones:
                sensor_count = len(zone.get("sensors", []))
                msg += f"• {zone.get('name')} ({sensor_count} sensors)\n"
        else:
            msg += "No zones configured"
        messagebox.showinfo("Safety Zones", msg)

    def _handle_all_cameras(self):
        """Handle show all cameras."""
        cameras = self.device_service.get_cameras()
        msg = f"Total Cameras: {len(cameras)}\n\n"
        for cam in cameras:
            status = "Enabled" if cam.is_enabled else "Disabled"
            msg += f"• {cam.name} - {status}\n"
        messagebox.showinfo("Cameras", msg)

    def _handle_all_sensors(self):
        """Handle show all sensors."""
        sensors = self.device_service.get_sensors()
        msg = f"Total Sensors: {len(sensors)}\n\n"
        for sensor in sensors:
            status = "Armed" if sensor.is_armed else "Disarmed"
            msg += f"• {sensor.name} - {status}\n"
        messagebox.showinfo("Sensors", msg)

    def _handle_settings(self):
        """Handle settings."""
        messagebox.showinfo("Settings", "System settings (not implemented)")

    def _handle_view_log(self):
        """Handle view log."""
        logs = self.system.view_intrusion_log()
        messagebox.showinfo("Log", f"Total events: {len(logs)}")

    def _handle_change_password(self):
        """Handle change password."""
        from tkinter import simpledialog

        dialog = tk.Toplevel(self._window)
        dialog.title("Change Password")
        dialog.geometry("280x200")

        tk.Label(dialog, text="Current Password:").pack(pady=5)
        old_pw = tk.Entry(dialog, show="*")
        old_pw.pack()

        tk.Label(dialog, text="New Password (4 digits):").pack(pady=5)
        new_pw = tk.Entry(dialog, show="*")
        new_pw.pack()

        tk.Label(dialog, text="Confirm Password:").pack(pady=5)
        confirm_pw = tk.Entry(dialog, show="*")
        confirm_pw.pack()

        def submit():
            if new_pw.get() != confirm_pw.get():
                messagebox.showerror("Error", "Passwords don't match", parent=dialog)
                return

            if self.security_service.change_password(old_pw.get(), new_pw.get()):
                messagebox.showinfo("Success", "Password changed", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror(
                    "Error", "Failed to change password", parent=dialog
                )

        tk.Button(dialog, text="Change", command=submit).pack(pady=10)

    def _handle_panic(self):
        """Handle panic button."""
        if messagebox.askyesno("EMERGENCY", "Call monitoring service?", icon="warning"):
            self.security_service.call_monitoring_service("PANIC")
            messagebox.showwarning("EMERGENCY", "Monitoring service called!")

    def _handle_power_off(self):
        """Handle power off."""
        if messagebox.askyesno("Confirm", "Turn off system?"):
            self.system.turn_off()
            self._transition_to(PanelState.SYSTEM_OFF)
