"""CameraPasswordDialog - Set/Delete camera password dialog"""
import tkinter as tk
from tkinter import ttk
from typing import Dict
from .base_dialog import BaseDialog


class CameraPasswordDialog(BaseDialog):
    """Dialog for setting or deleting camera password"""

    def __init__(self, parent: tk.Widget, web_interface, camera: Dict,
                 mode: str = "set"):
        title = "Set Password" if mode == "set" else "Delete Password"
        height = 280 if mode == "set" else 180
        super().__init__(parent, title, 380, height)
        self._wi = web_interface
        self._cam = camera
        self._mode = mode
        self._build_ui()

    def _build_ui(self) -> None:
        f = ttk.Frame(self, padding=20)
        f.pack(fill="both", expand=True)

        ttk.Label(f, text=f"Camera: {self._cam['name']}",
                  font=("Arial", 11, "bold")).pack(pady=(0, 15))

        if self._mode == "set":
            self._build_set_ui(f)
        else:
            self._build_delete_ui(f)

    def _build_set_ui(self, f):
        if self._cam.get("has_password"):
            ttk.Label(f, text="Current Password:").pack(anchor="w")
            self._old = tk.StringVar()
            ttk.Entry(f, textvariable=self._old, show="*", width=30).pack(pady=5)
        else:
            self._old = None
        ttk.Label(f, text="New Password (4+ chars):").pack(anchor="w")
        self._new = tk.StringVar()
        ttk.Entry(f, textvariable=self._new, show="*", width=30).pack(pady=5)
        ttk.Label(f, text="Confirm:").pack(anchor="w")
        self._confirm = tk.StringVar()
        ttk.Entry(f, textvariable=self._confirm, show="*", width=30).pack(pady=5)
        self._make_buttons(f, "Set", self._set)

    def _build_delete_ui(self, f):
        ttk.Label(f, text="Enter current password:").pack(anchor="w")
        self._pw = tk.StringVar()
        ttk.Entry(f, textvariable=self._pw, show="*", width=30).pack(pady=5)
        self._make_buttons(f, "Delete", self._delete)

    def _make_buttons(self, f, action_text, action_cmd):
        bf = ttk.Frame(f)
        bf.pack(pady=10)
        ttk.Button(bf, text=action_text, command=action_cmd, width=12).pack(side="left", padx=5)
        ttk.Button(bf, text="Cancel", command=self._on_cancel, width=12).pack(side="left", padx=5)

    def _set(self):
        old = self._old.get() if self._old else None
        new, confirm = self._new.get(), self._confirm.get()
        if len(new) < 4:
            return self._show_error("Password must be 4+ characters")
        if new != confirm:
            return self._show_error("Passwords do not match")
        res = self._wi.send_message("set_camera_password",
                                    camera_id=self._cam["id"],
                                    old_password=old, new_password=new)
        self._handle_result(res, "Password set")

    def _delete(self):
        pw = self._pw.get()
        if not pw:
            return self._show_error("Enter password")
        res = self._wi.send_message("delete_camera_password",
                                    camera_id=self._cam["id"], password=pw)
        self._handle_result(res, "Password deleted")

    def _handle_result(self, res, success_msg):
        if res.get("success"):
            self._show_info(success_msg)
            self._on_ok()
        else:
            self._show_error(res.get("message", "Failed"))
