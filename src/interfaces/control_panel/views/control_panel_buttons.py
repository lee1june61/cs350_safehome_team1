"""Control panel buttons view."""

import tkinter as tk
from typing import Callable
from ..config.ui_config import UIConfig


class ControlPanelButtons:
    """Control panel buttons sidebar.

    Following the control panel UI design from SDS.
    """

    def __init__(self, parent: tk.Widget):
        """Initialize control buttons.

        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.frame: tk.Frame = None

        # Callbacks
        self.on_security_mode: Callable[[str], None] = None
        self.on_create_zone: Callable = None
        self.on_manage_zones: Callable = None
        self.on_all_cameras: Callable = None
        self.on_all_sensors: Callable = None
        self.on_settings: Callable = None
        self.on_view_log: Callable = None
        self.on_change_password: Callable = None
        self.on_panic: Callable = None
        self.on_power_off: Callable = None

    def create(self) -> tk.Frame:
        """Create control buttons panel.

        Returns:
            Frame containing control buttons
        """
        self.frame = tk.Frame(self.parent, width=UIConfig.CONTROL_PANEL_WIDTH)
        self.frame.pack_propagate(False)

        # Security modes section
        self._create_security_section()

        # Safety zones section
        self._create_zones_section()

        # Devices section
        self._create_devices_section()

        # System section
        self._create_system_section()

        # Emergency button
        self._create_emergency_button()

        # Power button
        self._create_power_button()

        return self.frame

    def _create_security_section(self):
        """Create security modes section."""
        sec_frame = tk.LabelFrame(
            self.frame, text="🛡️ Security", font=("Arial", 9, "bold")
        )
        sec_frame.pack(fill=tk.X, pady=2)

        modes = [
            ("🏠 Home", "ARMED_HOME"),
            ("🚗 Away", "ARMED_AWAY"),
            ("🌙 Night", "ARMED_NIGHT"),
            ("✈️ Vacation", "ARMED_VACATION"),
            ("⛔ Disarm", "DISARMED"),
        ]

        for label, mode in modes:
            tk.Button(
                sec_frame,
                text=label,
                font=UIConfig.FONT_BUTTON_SMALL,
                width=UIConfig.BUTTON_WIDTH,
                command=lambda m=mode: (
                    self.on_security_mode(m) if self.on_security_mode else None
                ),
            ).pack(pady=1, padx=2)

    def _create_zones_section(self):
        """Create safety zones section."""
        zone_frame = tk.LabelFrame(
            self.frame, text="🔒 Safety Zones", font=("Arial", 9, "bold")
        )
        zone_frame.pack(fill=tk.X, pady=2)

        tk.Button(
            zone_frame,
            text="➕ Create Zone",
            font=UIConfig.FONT_BUTTON_SMALL,
            width=UIConfig.BUTTON_WIDTH,
            command=self.on_create_zone if self.on_create_zone else None,
        ).pack(pady=1, padx=2)

        tk.Button(
            zone_frame,
            text="📝 Manage Zones",
            font=UIConfig.FONT_BUTTON_SMALL,
            width=UIConfig.BUTTON_WIDTH,
            command=self.on_manage_zones if self.on_manage_zones else None,
        ).pack(pady=1, padx=2)

    def _create_devices_section(self):
        """Create devices section."""
        dev_frame = tk.LabelFrame(
            self.frame, text="📱 Devices", font=("Arial", 9, "bold")
        )
        dev_frame.pack(fill=tk.X, pady=2)

        tk.Button(
            dev_frame,
            text="📹 All Cameras",
            font=UIConfig.FONT_BUTTON_SMALL,
            width=UIConfig.BUTTON_WIDTH,
            command=self.on_all_cameras if self.on_all_cameras else None,
        ).pack(pady=1, padx=2)

        tk.Button(
            dev_frame,
            text="🔍 All Sensors",
            font=UIConfig.FONT_BUTTON_SMALL,
            width=UIConfig.BUTTON_WIDTH,
            command=self.on_all_sensors if self.on_all_sensors else None,
        ).pack(pady=1, padx=2)

    def _create_system_section(self):
        """Create system section."""
        sys_frame = tk.LabelFrame(
            self.frame, text="⚙️ System", font=("Arial", 9, "bold")
        )
        sys_frame.pack(fill=tk.X, pady=2)

        buttons = [
            ("⚙️ Settings", self.on_settings),
            ("📋 View Log", self.on_view_log),
            ("🔒 Change Password", self.on_change_password),
        ]

        for text, callback in buttons:
            tk.Button(
                sys_frame,
                text=text,
                font=UIConfig.FONT_BUTTON_SMALL,
                width=UIConfig.BUTTON_WIDTH,
                command=callback if callback else None,
            ).pack(pady=1, padx=2)

    def _create_emergency_button(self):
        """Create emergency panic button."""
        tk.Button(
            self.frame,
            text="🚨 PANIC",
            font=("Arial", 10, "bold"),
            width=UIConfig.BUTTON_WIDTH,
            height=2,
            bg=UIConfig.COLOR_DANGER,
            fg=UIConfig.COLOR_WHITE,
            command=self.on_panic if self.on_panic else None,
        ).pack(pady=6)

    def _create_power_button(self):
        """Create power off button."""
        tk.Button(
            self.frame,
            text="⚡ POWER OFF",
            font=UIConfig.FONT_BUTTON_SMALL,
            width=UIConfig.BUTTON_WIDTH,
            bg="#757575",
            fg=UIConfig.COLOR_WHITE,
            command=self.on_power_off if self.on_power_off else None,
        ).pack(pady=2)
