"""Main screen for Control Panel - BUTTONS ONLY (NO FLOOR PLAN).

Following SRS requirements:
- Control Panel is for LOCAL access only
- Simple button interface (Home/Away/Panic/Code)
- 4-digit password authentication
- Status display (text only)

Reference: SRS Section V.1.a (Log onto system through control panel)
"""

import tkinter as tk
from typing import Callable, Optional


class MainScreen:
    """Main control panel screen with buttons only.

    This screen follows the SRS specification for Control Panel:
    - NO floor plan (floor plan is Web Interface only)
    - Simple button controls (Home/Away/Code/Panic)
    - Status display
    - Master password change functionality
    """

    def __init__(
        self,
        parent: tk.Widget,
        username: str,
        on_home: Callable[[], None],
        on_away: Callable[[], None],
        on_code: Callable[[], None],
        on_panic: Callable[[], None],
        on_logout: Callable[[], None],
    ):
        """Initialize main screen.

        Args:
            parent: Parent widget
            username: Logged in username
            on_home: Callback for Home button
            on_away: Callback for Away button
            on_code: Callback for Code button (password change)
            on_panic: Callback for Panic button (*, #)
            on_logout: Callback for logout
        """
        self.parent = parent
        self.username = username
        self.on_home = on_home
        self.on_away = on_away
        self.on_code = on_code
        self.on_panic = on_panic
        self.on_logout = on_logout

        # Components
        self.status_label: Optional[tk.Label] = None
        self.system_status_label: Optional[tk.Label] = None
        self.status_indicator: Optional[tk.Label] = None

    def build(self) -> tk.Frame:
        """Build main screen with buttons only.

        Returns:
            Frame containing the main screen
        """
        frame = tk.Frame(self.parent, bg="#ffffff")

        # Header
        self._create_header(frame)

        # Main content - CENTER BUTTONS
        content = tk.Frame(frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # System status display
        self._create_status_display(content)

        # Control buttons (centered)
        self._create_control_buttons(content)

        # Bottom status bar
        self._create_status_bar(frame)

        return frame

    def _create_header(self, parent: tk.Frame) -> None:
        """Create header with title and user info."""
        header = tk.Frame(parent, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Title
        tk.Label(
            header,
            text="SafeHome Control Panel",
            font=("Arial", 18, "bold"),
            fg="#ffffff",
            bg="#2c3e50",
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # User info
        user_frame = tk.Frame(header, bg="#2c3e50")
        user_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            user_frame,
            text=f"User: {self.username}",
            font=("Arial", 11),
            fg="#ffffff",
            bg="#2c3e50",
        ).pack()

    def _create_status_display(self, parent: tk.Frame) -> None:
        """Create system status display area."""
        status_frame = tk.LabelFrame(
            parent,
            text="System Status",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )
        status_frame.pack(fill=tk.X, pady=(0, 20))

        # Status indicator
        indicator_frame = tk.Frame(status_frame, bg="#ffffff")
        indicator_frame.pack(pady=15)

        # Status light (red/green)
        self.status_indicator = tk.Label(
            indicator_frame,
            text="⚫",
            font=("Arial", 48),
            bg="#ffffff",
        )
        self.status_indicator.pack(side=tk.LEFT, padx=20)

        # Status text
        status_text_frame = tk.Frame(indicator_frame, bg="#ffffff")
        status_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            status_text_frame,
            text="System:",
            font=("Arial", 11),
            bg="#ffffff",
        ).pack(anchor=tk.W)

        self.system_status_label = tk.Label(
            status_text_frame,
            text="DISARMED",
            font=("Arial", 16, "bold"),
            fg="#27ae60",
            bg="#ffffff",
        )
        self.system_status_label.pack(anchor=tk.W)

    def _create_control_buttons(self, parent: tk.Frame) -> None:
        """Create control buttons panel.

        Following SRS: Control Panel has HOME, AWAY, CODE, PANIC buttons
        """
        buttons_frame = tk.LabelFrame(
            parent,
            text="Control Buttons",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Create button grid
        button_container = tk.Frame(buttons_frame, bg="#ffffff")
        button_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Row 1: HOME and AWAY
        row1 = tk.Frame(button_container, bg="#ffffff")
        row1.pack(pady=10)

        self._create_button(
            row1,
            "🏠 HOME",
            self.on_home,
            "#27ae60",
        ).pack(side=tk.LEFT, padx=10)

        self._create_button(
            row1,
            "🚗 AWAY",
            self.on_away,
            "#f39c12",
        ).pack(side=tk.LEFT, padx=10)

        # Row 2: CODE and PANIC
        row2 = tk.Frame(button_container, bg="#ffffff")
        row2.pack(pady=10)

        self._create_button(
            row2,
            "🔐 CODE",
            self.on_code,
            "#3498db",
        ).pack(side=tk.LEFT, padx=10)

        self._create_button(
            row2,
            "🚨 PANIC",
            self.on_panic,
            "#e74c3c",
        ).pack(side=tk.LEFT, padx=10)

        # Instructions
        instructions = tk.Label(
            button_container,
            text=(
                "HOME: Disarm system | AWAY: Arm system\n"
                "CODE: Change password | PANIC: Emergency call"
            ),
            font=("Arial", 9),
            bg="#ffffff",
            fg="#7f8c8d",
            justify=tk.CENTER,
        )
        instructions.pack(pady=20)

    def _create_button(
        self,
        parent: tk.Frame,
        text: str,
        command: Callable[[], None],
        bg_color: str,
    ) -> tk.Button:
        """Create a styled button."""
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg=bg_color,
            fg="#ffffff",
            width=12,
            height=2,
            relief=tk.RAISED,
            borderwidth=3,
            command=command,
            cursor="hand2",
        )

    def _create_status_bar(self, parent: tk.Frame) -> None:
        """Create status bar at bottom."""
        status_bar = tk.Frame(parent, bg="#ecf0f1", height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            font=("Arial", 9),
            bg="#ecf0f1",
            anchor=tk.W,
        )
        self.status_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Logout button
        tk.Button(
            status_bar,
            text="Logout",
            font=("Arial", 9),
            command=self.on_logout,
            relief=tk.FLAT,
            bg="#ecf0f1",
        ).pack(side=tk.RIGHT, padx=10)

    def update_system_status(self, armed: bool) -> None:
        """Update system armed/disarmed status."""
        if armed:
            self.status_indicator.config(text="🔴", fg="#e74c3c")
            self.system_status_label.config(
                text="ARMED",
                fg="#e74c3c",
            )
        else:
            self.status_indicator.config(text="🟢", fg="#27ae60")
            self.system_status_label.config(
                text="DISARMED",
                fg="#27ae60",
            )

    def update_status(self, message: str) -> None:
        """Update status bar message."""
        if self.status_label:
            self.status_label.config(text=message)

    def show_message(self, title: str, message: str, msg_type: str = "info") -> None:
        """Show a message dialog."""
        import tkinter.messagebox as messagebox

        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
