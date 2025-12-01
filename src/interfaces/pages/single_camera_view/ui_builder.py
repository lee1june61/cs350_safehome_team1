"""UI builder for single camera view page."""
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class SingleCameraViewUIBuilder:
    """Builds the UI for single camera view page."""

    def __init__(self, page: "SingleCameraViewPage"):
        self._page = page

    def build(self):
        """Build the complete UI."""
        header = self._page._create_header("Camera View", back_page="camera_list")
        self._page._back_nav.register_button(getattr(header, "back_button", None))

        content = ttk.Frame(self._page._frame)
        content.pack(expand=True, fill="both", padx=20, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=1)

        self._build_video_panel(content)
        self._build_control_panel(content)

    def _build_video_panel(self, parent):
        """Build left video panel."""
        left = ttk.LabelFrame(parent, text="Live View", padding=5)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._page._video = ttk.Label(left, anchor="center")
        self._page._video.pack(expand=True, fill="both")

    def _build_control_panel(self, parent):
        """Build right control panel."""
        right = ttk.Frame(parent)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_info_section(right)
        self._build_ptz_section(right)
        self._build_actions_section(right)
        self._build_password_section(right)

    def _build_info_section(self, parent):
        """Build camera info section."""
        info = ttk.LabelFrame(parent, text="Camera Info", padding=8)
        info.pack(fill="x", pady=5)
        self._page._info = ttk.Label(info, text="")
        self._page._info.pack(anchor="w")

    def _build_ptz_section(self, parent):
        """Build pan/tilt/zoom controls."""
        ptz = ttk.LabelFrame(parent, text="Pan/Tilt/Zoom", padding=8)
        ptz.pack(fill="x", pady=5)

        # Pan controls
        pf = ttk.Frame(ptz)
        pf.pack()
        ttk.Label(pf, text="Pan:", font=('Arial', 9)).pack(side="left", padx=2)
        ttk.Button(pf, text="◄ L", command=lambda: self._page.controls.pan("L"), width=6).pack(side="left", padx=2)
        ttk.Button(pf, text="R ►", command=lambda: self._page.controls.pan("R"), width=6).pack(side="left", padx=2)

        # Tilt controls
        tf = ttk.Frame(ptz)
        tf.pack(pady=5)
        ttk.Label(tf, text="Tilt:", font=('Arial', 9)).pack(side="left", padx=2)
        ttk.Button(tf, text="↑ Up", command=lambda: self._page.controls.tilt("up"), width=6).pack(side="left", padx=2)
        ttk.Button(tf, text="↓ Down", command=lambda: self._page.controls.tilt("down"), width=6).pack(side="left", padx=2)

        # Zoom controls
        zf = ttk.Frame(ptz)
        zf.pack(pady=5)
        ttk.Label(zf, text="Zoom:", font=('Arial', 9)).pack(side="left", padx=2)
        ttk.Button(zf, text="+ In", command=lambda: self._page.controls.zoom("in"), width=6).pack(side="left", padx=2)
        ttk.Button(zf, text="- Out", command=lambda: self._page.controls.zoom("out"), width=6).pack(side="left", padx=2)

    def _build_actions_section(self, parent):
        """Build enable/disable actions."""
        act = ttk.LabelFrame(parent, text="Actions", padding=8)
        act.pack(fill="x", pady=5)
        self._page._btn_en = ttk.Button(act, text="Enable", command=self._page.controls.enable, width=12)
        self._page._btn_en.pack(pady=2)
        self._page._btn_dis = ttk.Button(act, text="Disable", command=self._page.controls.disable, width=12)
        self._page._btn_dis.pack(pady=2)

    def _build_password_section(self, parent):
        """Build password controls."""
        pw = ttk.LabelFrame(parent, text="Password", padding=8)
        pw.pack(fill="x", pady=5)
        ttk.Button(pw, text="Set Password", command=self._page._pw_manager.set_password, width=12).pack(pady=2)
        ttk.Button(pw, text="Delete Password", command=self._page._pw_manager.delete_password, width=12).pack(pady=2)

