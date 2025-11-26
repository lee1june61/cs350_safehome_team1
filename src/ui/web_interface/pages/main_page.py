"""Main page for Web Interface - WITH FLOOR PLAN.

Following SRS requirements:
- Web Interface is for REMOTE access
- Floor plan based interface
- User ID + 2-level 8-character password authentication
- Safety zone configuration via floor plan
- Camera selection via floor plan

Reference: SRS Section V.2.b (Log onto system through web browser)
         SRS Section V.3.a (Display specific camera view)
"""

import tkinter as tk
from tkinter import messagebox
from typing import Callable, List, Optional


class MainPage:
    """Main web interface page with floor plan.

    This page follows the SRS specification for Web Interface:
    - Floor plan display (Web Interface ONLY)
    - Device icons on floor plan
    - Click devices to control/view
    - Safety zone visualization
    """

    def __init__(
        self,
        parent: tk.Widget,
        username: str,
        on_device_click: Callable[[str, str], None],
        on_security: Callable[[], None],
        on_surveillance: Callable[[], None],
        on_settings: Callable[[], None],
        on_logout: Callable[[], None],
    ):
        """Initialize main page.

        Args:
            parent: Parent widget
            username: Logged in username
            on_device_click: Callback for device icon click (device_type, device_id)
            on_security: Callback for Security button
            on_surveillance: Callback for Surveillance button
            on_settings: Callback for Settings button
            on_logout: Callback for logout
        """
        self.parent = parent
        self.username = username
        self.on_device_click = on_device_click
        self.on_security = on_security
        self.on_surveillance = on_surveillance
        self.on_settings = on_settings
        self.on_logout = on_logout

        # Components
        self.floor_plan_canvas: Optional[tk.Canvas] = None
        self.status_label: Optional[tk.Label] = None
        self.system_mode_label: Optional[tk.Label] = None
        self.device_items = {}  # device_id -> canvas_item_id

    def build(self) -> tk.Frame:
        """Build main page with floor plan.

        Returns:
            Frame containing the main page
        """
        frame = tk.Frame(self.parent, bg="#ffffff")

        # Header
        self._create_header(frame)

        # Main content
        content = tk.Frame(frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Floor plan
        left_panel = self._create_floor_plan_panel(content)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right: Function buttons and status
        right_panel = self._create_control_panel(content)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # Status bar
        self._create_status_bar(frame)

        return frame

    def _create_header(self, parent: tk.Frame) -> None:
        """Create header with title and user info."""
        header = tk.Frame(parent, bg="#2c3e50", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Title
        title_frame = tk.Frame(header, bg="#2c3e50")
        title_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            title_frame,
            text="SafeHome Web Interface",
            font=("Arial", 18, "bold"),
            fg="#ffffff",
            bg="#2c3e50",
        ).pack()

        tk.Label(
            title_frame,
            text="Remote Access & Monitoring",
            font=("Arial", 10),
            fg="#bdc3c7",
            bg="#2c3e50",
        ).pack()

        # User info
        user_frame = tk.Frame(header, bg="#2c3e50")
        user_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            user_frame,
            text=f"👤 {self.username}",
            font=("Arial", 12),
            fg="#ffffff",
            bg="#2c3e50",
        ).pack()

        tk.Button(
            user_frame,
            text="Logout",
            font=("Arial", 9),
            command=self.on_logout,
            bg="#e74c3c",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=3,
        ).pack(pady=(5, 0))

    def _create_floor_plan_panel(self, parent: tk.Frame) -> tk.LabelFrame:
        """Create floor plan panel.

        Following SRS: "The system displays the floor plan of the house"

        Returns:
            LabelFrame containing floor plan
        """
        panel = tk.LabelFrame(
            parent,
            text="🏠 House Floor Plan - Click devices to control",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )

        # Legend
        legend_frame = tk.Frame(panel, bg="#ecf0f1", height=35)
        legend_frame.pack(fill=tk.X, padx=5, pady=5)
        legend_frame.pack_propagate(False)

        tk.Label(
            legend_frame,
            text=(
                "Legend: 🔴 Armed  🟢 Disarmed  |  "
                "🟥 Window/Door  🟦 Motion  📹 Camera  🔔 Alarm"
            ),
            font=("Arial", 9),
            bg="#ecf0f1",
        ).pack(pady=7)

        # Floor plan canvas
        canvas_frame = tk.Frame(panel, bg="#ffffff")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.floor_plan_canvas = tk.Canvas(
            canvas_frame,
            width=800,
            height=600,
            bg="#f5f5f5",
            highlightthickness=1,
            highlightbackground="#bdc3c7",
        )
        self.floor_plan_canvas.pack(fill=tk.BOTH, expand=True)

        # Draw placeholder floor plan
        self._draw_placeholder_floor_plan()

        # Bind click event
        self.floor_plan_canvas.bind("<Button-1>", self._handle_canvas_click)

        # Instructions
        instructions = tk.Label(
            panel,
            text="Click on device icons to view details or control them",
            font=("Arial", 9, "italic"),
            bg="#ffffff",
            fg="#7f8c8d",
        )
        instructions.pack(pady=5)

        return panel

    def _draw_placeholder_floor_plan(self) -> None:
        """Draw a placeholder floor plan."""
        # Draw rooms
        rooms = [
            ("Living Room", 50, 50, 350, 250),
            ("Kitchen", 50, 270, 250, 450),
            ("Bedroom 1", 370, 50, 550, 250),
            ("Bedroom 2", 370, 270, 550, 450),
            ("Bathroom", 270, 270, 350, 350),
            ("Hallway", 270, 50, 350, 250),
        ]

        for name, x1, y1, x2, y2 in rooms:
            # Room rectangle
            self.floor_plan_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#ecf0f1",
                outline="#34495e",
                width=2,
                tags="floor_plan",
            )

            # Room label
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            self.floor_plan_canvas.create_text(
                center_x, center_y,
                text=name,
                font=("Arial", 10, "bold"),
                fill="#7f8c8d",
                tags="floor_plan",
            )

    def _create_control_panel(self, parent: tk.Frame) -> tk.Frame:
        """Create control panel with function buttons."""
        panel = tk.Frame(parent, bg="#ffffff", width=250)
        panel.pack_propagate(False)

        # System status
        status_frame = tk.LabelFrame(
            panel,
            text="System Status",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )
        status_frame.pack(fill=tk.X, pady=(0, 15))

        # Mode indicator
        mode_container = tk.Frame(status_frame, bg="#ffffff")
        mode_container.pack(pady=10)

        tk.Label(
            mode_container,
            text="Current Mode:",
            font=("Arial", 10),
            bg="#ffffff",
        ).pack()

        self.system_mode_label = tk.Label(
            mode_container,
            text="HOME",
            font=("Arial", 14, "bold"),
            fg="#27ae60",
            bg="#ffffff",
        )
        self.system_mode_label.pack(pady=5)

        # Function buttons
        functions_frame = tk.LabelFrame(
            panel,
            text="Main Functions",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )
        functions_frame.pack(fill=tk.X, pady=(0, 15))

        # Security button
        self._create_function_button(
            functions_frame,
            "🔒 Security",
            "Configure security\nand safety zones",
            self.on_security,
            "#3498db",
        ).pack(pady=8, padx=10, fill=tk.X)

        # Surveillance button
        self._create_function_button(
            functions_frame,
            "📹 Surveillance",
            "View cameras",
            self.on_surveillance,
            "#9b59b6",
        ).pack(pady=8, padx=10, fill=tk.X)

        # Settings button
        self._create_function_button(
            functions_frame,
            "⚙️ Settings",
            "System settings",
            self.on_settings,
            "#95a5a6",
        ).pack(pady=8, padx=10, fill=tk.X)

        return panel

    def _create_function_button(
        self,
        parent: tk.Frame,
        text: str,
        description: str,
        command: Callable[[], None],
        bg_color: str,
    ) -> tk.Frame:
        """Create a function button with description."""
        button_frame = tk.Frame(parent, bg="#ffffff")

        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 11, "bold"),
            bg=bg_color,
            fg="#ffffff",
            relief=tk.RAISED,
            borderwidth=3,
            command=command,
            cursor="hand2",
            height=2,
        )
        button.pack(fill=tk.X)

        tk.Label(
            button_frame,
            text=description,
            font=("Arial", 8),
            fg="#7f8c8d",
            bg="#ffffff",
            justify=tk.CENTER,
        ).pack(pady=(3, 0))

        return button_frame

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
        self.status_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH)

        # Connection indicator
        tk.Label(
            status_bar,
            text="🟢 Connected",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#27ae60",
        ).pack(side=tk.RIGHT, padx=10)

    def _handle_canvas_click(self, event) -> None:
        """Handle canvas click event."""
        # Find clicked item
        items = self.floor_plan_canvas.find_overlapping(
            event.x - 5, event.y - 5,
            event.x + 5, event.y + 5
        )

        for item in items:
            tags = self.floor_plan_canvas.gettags(item)
            for tag in tags:
                if tag.startswith("device_"):
                    device_id = tag.replace("device_", "")
                    # Find device info
                    for dev_id, info in self.device_items.items():
                        if dev_id == device_id:
                            self.on_device_click(info["type"], device_id)
                            break
                    break

    def add_device_icon(
        self,
        device_type: str,
        device_id: str,
        x: int,
        y: int,
        armed: bool = False,
    ) -> None:
        """Add device icon to floor plan."""
        # Device symbols and colors
        symbols = {
            "window_door_sensor": "🟥",
            "motion_sensor": "🟦",
            "camera": "📹",
            "alarm": "🔔",
        }

        colors = {
            "window_door_sensor": "#e74c3c" if armed else "#bdc3c7",
            "motion_sensor": "#3498db" if armed else "#bdc3c7",
            "camera": "#9b59b6" if armed else "#bdc3c7",
            "alarm": "#e67e22" if armed else "#bdc3c7",
        }

        symbol = symbols.get(device_type, "⚫")
        color = colors.get(device_type, "#95a5a6")

        # Draw device
        circle_id = self.floor_plan_canvas.create_oval(
            x - 15, y - 15,
            x + 15, y + 15,
            fill=color,
            outline="#2c3e50",
            width=2,
            tags=("device", f"device_{device_id}"),
        )

        # Draw symbol
        text_id = self.floor_plan_canvas.create_text(
            x, y,
            text=symbol,
            font=("Arial", 14),
            tags=("device", f"device_{device_id}"),
        )

        # Draw label
        label_id = self.floor_plan_canvas.create_text(
            x, y + 25,
            text=device_id,
            font=("Arial", 8),
            fill="#2c3e50",
            tags=("device", f"device_{device_id}"),
        )

        # Store device info
        self.device_items[device_id] = {
            "type": device_type,
            "armed": armed,
            "circle": circle_id,
            "text": text_id,
            "label": label_id,
        }

    def update_status(self, message: str) -> None:
        """Update status bar message."""
        if self.status_label:
            self.status_label.config(text=message)
