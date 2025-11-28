"""Device detail windows."""

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Callable
from ..models.device_icon import DeviceIcon
from ..config.ui_config import UIConfig


class SensorWindow:
    """Sensor detail window.

    Following the device control use cases from SRS document.
    """

    def __init__(
        self,
        parent: tk.Widget,
        device: DeviceIcon,
        on_arm: Callable,
        on_disarm: Callable,
    ):
        """Initialize sensor window.

        Args:
            parent: Parent widget
            device: Device icon
            on_arm: Callback to arm sensor
            on_disarm: Callback to disarm sensor
        """
        self.parent = parent
        self.device = device
        self.on_arm = on_arm
        self.on_disarm = on_disarm
        self.window: tk.Toplevel = None
        self.status_label: tk.Label = None

    def show(self):
        """Show sensor window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Sensor - {self.device.name}")
        self.window.geometry("380x280")

        # Title
        sensor_type = (
            "Window/Door Sensor"
            if self.device.device_type == "window_door"
            else "Motion Sensor"
        )
        icon = "🟥" if self.device.device_type == "window_door" else "🟦"

        tk.Label(
            self.window, text=f"{icon} {sensor_type}", font=("Arial", 13, "bold")
        ).pack(pady=8)

        tk.Label(self.window, text=self.device.name, font=("Arial", 11)).pack()

        tk.Label(
            self.window, text=f"ID: {self.device.device_id}", font=("Arial", 9)
        ).pack()

        # Status
        status_frame = tk.LabelFrame(
            self.window, text="Status", font=("Arial", 10, "bold")
        )
        status_frame.pack(fill=tk.X, padx=15, pady=8)

        status_text = "🔴 ARMED" if self.device.is_armed else "⚪ DISARMED"
        status_color = "red" if self.device.is_armed else "gray"

        self.status_label = tk.Label(
            status_frame, text=status_text, font=("Arial", 15, "bold"), fg=status_color
        )
        self.status_label.pack(pady=8)

        # Controls
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=8)

        if self.device.is_armed:
            tk.Button(
                control_frame,
                text="⛔ Disarm Sensor",
                font=("Arial", 11),
                width=18,
                bg=UIConfig.COLOR_INFO,
                command=self._handle_disarm,
            ).pack(pady=4)
        else:
            tk.Button(
                control_frame,
                text="✅ Arm Sensor",
                font=("Arial", 11),
                width=18,
                bg=UIConfig.COLOR_SENSOR_ARMED,
                fg=UIConfig.COLOR_WHITE,
                command=self._handle_arm,
            ).pack(pady=4)

        tk.Button(
            control_frame,
            text="📊 View Details",
            font=("Arial", 11),
            width=18,
            command=self._show_details,
        ).pack(pady=4)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=8)

    def _handle_arm(self):
        """Handle arm button."""
        if self.on_arm(self.device.device_id):
            self.device.is_armed = True
            self.status_label.config(text="🔴 ARMED", fg="red")
            messagebox.showinfo(
                "Success", f"Sensor {self.device.device_id} armed", parent=self.window
            )
            self.window.destroy()

    def _handle_disarm(self):
        """Handle disarm button."""
        if self.on_disarm(self.device.device_id):
            self.device.is_armed = False
            self.status_label.config(text="⚪ DISARMED", fg="gray")
            messagebox.showinfo(
                "Success",
                f"Sensor {self.device.device_id} disarmed",
                parent=self.window,
            )
            self.window.destroy()

    def _show_details(self):
        """Show sensor details."""
        sensor_type = (
            "Window/Door" if self.device.device_type == "window_door" else "Motion"
        )
        msg = f"Sensor ID: {self.device.device_id}\n"
        msg += f"Name: {self.device.name}\n"
        msg += f"Type: {sensor_type}\n"
        msg += f"Status: {'ARMED' if self.device.is_armed else 'DISARMED'}"
        messagebox.showinfo("Sensor Details", msg, parent=self.window)


class CameraWindow:
    """Camera detail window.

    Following camera control use cases from SRS document.
    """

    def __init__(
        self,
        parent: tk.Widget,
        device: DeviceIcon,
        on_enable: Callable,
        on_disable: Callable,
        on_view_feed: Callable,
        on_ptz: Callable,
        on_set_password: Callable,
    ):
        """Initialize camera window.

        Args:
            parent: Parent widget
            device: Device icon
            on_enable: Callback to enable camera
            on_disable: Callback to disable camera
            on_view_feed: Callback to view camera feed
            on_ptz: Callback to show PTZ controls
            on_set_password: Callback to set camera password
        """
        self.parent = parent
        self.device = device
        self.on_enable = on_enable
        self.on_disable = on_disable
        self.on_view_feed = on_view_feed
        self.on_ptz = on_ptz
        self.on_set_password = on_set_password
        self.window: tk.Toplevel = None
        self.status_label: tk.Label = None

    def show(self):
        """Show camera window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Camera - {self.device.name}")
        self.window.geometry("450x380")

        # Title
        tk.Label(self.window, text="🟢 Camera", font=("Arial", 13, "bold")).pack(pady=8)

        tk.Label(self.window, text=self.device.name, font=("Arial", 11)).pack()

        tk.Label(
            self.window, text=f"ID: {self.device.device_id}", font=("Arial", 9)
        ).pack()

        # Status
        status_frame = tk.LabelFrame(
            self.window, text="Camera State", font=("Arial", 10, "bold")
        )
        status_frame.pack(fill=tk.X, padx=15, pady=8)

        status_text = "🟢 ENABLED" if self.device.is_enabled else "⚪ DISABLED"
        status_color = "green" if self.device.is_enabled else "gray"

        self.status_label = tk.Label(
            status_frame, text=status_text, font=("Arial", 15, "bold"), fg=status_color
        )
        self.status_label.pack(pady=8)

        # Controls
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=8)

        # View feed button
        if self.device.is_enabled:
            tk.Button(
                control_frame,
                text="📹 View Feed",
                font=("Arial", 11, "bold"),
                width=18,
                bg=UIConfig.COLOR_PRIMARY,
                fg=UIConfig.COLOR_WHITE,
                command=lambda: self.on_view_feed(self.device),
            ).pack(pady=3)
        else:
            tk.Button(
                control_frame,
                text="📹 View Feed (Disabled)",
                font=("Arial", 11),
                width=18,
                bg=UIConfig.COLOR_GRAY,
                state="disabled",
            ).pack(pady=3)

        # PTZ control
        tk.Button(
            control_frame,
            text="🎮 Pan/Tilt/Zoom",
            font=("Arial", 11),
            width=18,
            command=lambda: self.on_ptz(self.device),
        ).pack(pady=3)

        # Enable/Disable
        if self.device.is_enabled:
            tk.Button(
                control_frame,
                text="⏸️ Disable Camera",
                font=("Arial", 11),
                width=18,
                bg=UIConfig.COLOR_WARNING,
                command=self._handle_disable,
            ).pack(pady=3)
        else:
            tk.Button(
                control_frame,
                text="▶️ Enable Camera",
                font=("Arial", 11),
                width=18,
                bg=UIConfig.COLOR_SUCCESS,
                fg=UIConfig.COLOR_WHITE,
                command=self._handle_enable,
            ).pack(pady=3)

        # Set password
        tk.Button(
            control_frame,
            text="🔒 Set Password",
            font=("Arial", 11),
            width=18,
            command=lambda: self.on_set_password(self.device),
        ).pack(pady=3)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=8)

    def _handle_enable(self):
        """Handle enable button."""
        if self.on_enable(self.device.device_id):
            self.device.is_enabled = True
            self.status_label.config(text="🟢 ENABLED", fg="green")
            messagebox.showinfo(
                "Success", f"Camera {self.device.device_id} enabled", parent=self.window
            )
            self.window.destroy()

    def _handle_disable(self):
        """Handle disable button."""
        if self.on_disable(self.device.device_id):
            self.device.is_enabled = False
            self.status_label.config(text="⚪ DISABLED", fg="gray")
            messagebox.showinfo(
                "Success",
                f"Camera {self.device.device_id} disabled",
                parent=self.window,
            )
            self.window.destroy()


class CameraFeedWindow:
    """Camera feed viewing window."""

    def __init__(self, parent: tk.Widget, device: DeviceIcon, system):
        """Initialize camera feed window.

        Args:
            parent: Parent widget
            device: Camera device
            system: SafeHome system instance
        """
        self.parent = parent
        self.device = device
        self.system = system
        self.window: tk.Toplevel = None

    def show(self):
        """Show camera feed window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Feed - {self.device.name}")
        self.window.geometry("640x480")

        tk.Label(
            self.window, text=f"📹 Live: {self.device.name}", font=("Arial", 13, "bold")
        ).pack(pady=8)

        # Video frame
        video_frame = tk.Frame(
            self.window, bg=UIConfig.COLOR_BLACK, width=600, height=400
        )
        video_frame.pack(padx=20, pady=8)
        video_frame.pack_propagate(False)

        tk.Label(
            video_frame,
            text="[Camera Video Feed]\n1 FPS",
            font=("Arial", 15),
            fg=UIConfig.COLOR_WHITE,
            bg=UIConfig.COLOR_BLACK,
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Request camera view from system
        self.system.get_camera_view(self.device.device_id)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=5)


class CameraPTZWindow:
    """Camera PTZ control window."""

    def __init__(self, parent: tk.Widget, device: DeviceIcon, system):
        """Initialize PTZ control window.

        Args:
            parent: Parent widget
            device: Camera device
            system: SafeHome system instance
        """
        self.parent = parent
        self.device = device
        self.system = system
        self.window: tk.Toplevel = None

    def show(self):
        """Show PTZ control window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"PTZ - {self.device.name}")
        self.window.geometry("280x220")

        tk.Label(self.window, text="🎮 PTZ Control", font=("Arial", 11, "bold")).pack(
            pady=8
        )

        # Pan controls
        pan_frame = tk.Frame(self.window)
        pan_frame.pack(pady=4)
        tk.Label(pan_frame, text="Pan:", width=6).pack(side=tk.LEFT, padx=4)
        tk.Button(
            pan_frame,
            text="⬅️",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, pan=-10
            ),
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            pan_frame,
            text="➡️",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, pan=10
            ),
        ).pack(side=tk.LEFT, padx=2)

        # Tilt controls
        tilt_frame = tk.Frame(self.window)
        tilt_frame.pack(pady=4)
        tk.Label(tilt_frame, text="Tilt:", width=6).pack(side=tk.LEFT, padx=4)
        tk.Button(
            tilt_frame,
            text="⬆️",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, tilt=10
            ),
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            tilt_frame,
            text="⬇️",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, tilt=-10
            ),
        ).pack(side=tk.LEFT, padx=2)

        # Zoom controls
        zoom_frame = tk.Frame(self.window)
        zoom_frame.pack(pady=4)
        tk.Label(zoom_frame, text="Zoom:", width=6).pack(side=tk.LEFT, padx=4)
        tk.Button(
            zoom_frame,
            text="➕",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, zoom=10
            ),
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            zoom_frame,
            text="➖",
            width=4,
            command=lambda: self.system.control_camera_ptz(
                self.device.device_id, zoom=-10
            ),
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=8)
