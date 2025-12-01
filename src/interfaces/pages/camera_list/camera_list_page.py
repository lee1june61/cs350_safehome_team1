"""CameraListPage - Pick camera from list/floorplan (SRS V.3.a)."""
import tkinter as tk
from ...components.page import Page
from .ui_builder import CameraListUIBuilder
from .access_manager import CameraAccessManager


class CameraListPage(Page):
    """Pick a camera from list or floorplan."""

    def __init__(self, parent, web_interface):
        super().__init__(parent, web_interface)
        self._cams = []
        self._selected = None
        self._access = CameraAccessManager(self)
        self._floorplan = None
        self._list = None
        self._info = None
        self._btn = None

    def _build_ui(self):
        builder = CameraListUIBuilder(self)
        builder.build()

    def _on_map_click(self, dev_id, dev_type):
        if dev_type == "camera":
            for c in self._cams:
                if c["id"] == dev_id:
                    self._select(c)
                    self._view()
                    break

    def _on_select(self, event):
        sel = self._list.curselection()
        if sel and sel[0] < len(self._cams):
            self._select(self._cams[sel[0]])

    def _select(self, cam):
        self._selected = cam
        self._btn.config(state="normal")
        en = "On" if cam.get("enabled") else "Off"
        pw = "Yes" if cam.get("password") else "No"
        self._info.config(text=f"{cam['id']} @ {cam['location']}\nStatus: {en}, Password: {pw}")

    def _view(self):
        if not self._selected:
            return
        cam_id = self._selected["id"]

        if self._access.is_locked(cam_id):
            return
        if self._selected.get("password") and not self._access.verify_password(cam_id):
            return

        self._web_interface.set_context("camera_id", cam_id)
        self._web_interface.set_context("camera_back_page", "camera_list")
        self.navigate_to("single_camera_view")

    def _load(self):
        self._list.delete(0, tk.END)
        res = self.send_to_system("get_cameras")
        self._cams = res.get("data", []) if res.get("success") else []
        for c in self._cams:
            status = "✓" if c.get("enabled") else "✗"
            lock = "🔒" if c.get("password") else ""
            self._list.insert(tk.END, f"{status} {c['id']}: {c['location']} {lock}")

    def on_show(self):
        self._load()
        self._selected = None
        self._btn.config(state="disabled")
