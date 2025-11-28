import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Any

class CameraControlsManager:
    """
    Manages the logic for camera controls: pan, zoom, enable/disable, and password.
    """
    def __init__(self, page_instance: Any, cam_id_ref: Any, info_label: ttk.Label, enable_btn: ttk.Button, disable_btn: ttk.Button):
        self._page = page_instance
        self._cam_id_ref = cam_id_ref # Reference to _cam_id in SingleCameraViewPage
        self._info = info_label
        self._btn_en = enable_btn
        self._btn_dis = disable_btn

    @property
    def _cam_id(self) -> str:
        return self._cam_id_ref.get_cam_id()

    def pan(self, direction: str):
        self._page.send_to_system('camera_pan', camera_id=self._cam_id, direction=direction)
        self.update_info()

    def zoom(self, direction: str):
        self._page.send_to_system('camera_zoom', camera_id=self._cam_id, direction=direction)
        self.update_info()

    def enable(self):
        res = self._page.send_to_system('enable_camera', camera_id=self._cam_id)
        if res.get('success'):
            messagebox.showinfo("Success", "Camera enabled")
            self.update_info()
        else:
            messagebox.showerror("Error", res.get('message', "Failed to enable camera"))

    def disable(self):
        res = self._page.send_to_system('disable_camera', camera_id=self._cam_id)
        if res.get('success'):
            messagebox.showinfo("Success", "Camera disabled")
            self.update_info()
        else:
            messagebox.showerror("Error", res.get('message', "Failed to disable camera"))

    def set_password(self):
        pw = simpledialog.askstring("Set Password", "Enter new password:", show='*')
        if pw:
            old_pw = simpledialog.askstring("Verify", "Enter current password (if any):", show='*')
            res = self._page.send_to_system('set_camera_password', camera_id=self._cam_id, old_password=old_pw, password=pw)
            if res.get('success'):
                messagebox.showinfo("Success", "Password set")
                self.update_info()
            else:
                messagebox.showerror("Error", res.get('message', "Failed to set password"))

    def delete_password(self):
        old = simpledialog.askstring("Verify", "Enter current password:", show='*')
        if old is not None:
            res = self._page.send_to_system('delete_camera_password', camera_id=self._cam_id, old_password=old)
            if res.get('success'):
                messagebox.showinfo("Success", "Password deleted")
                self.update_info()
            else:
                messagebox.showerror("Error", res.get('message', "Wrong password"))

    def update_info(self):
        """Update the camera info text display."""
        res = self._page.send_to_system('get_camera', camera_id=self._cam_id)
        if res.get('success'):
            c = res.get('data', {})
            en = c.get('enabled', False)
            pw_status = "Yes" if c.get('password') else "No"
            self._info.config(text=f"ID: {c.get('id')}\nLoc: {c.get('location')}\nPan: {c.get('pan', 0)} Zoom: {c.get('zoom', 1)}x\nStatus: {'On' if en else 'Off'}\nPassword: {pw_status}")
            self._btn_en.config(state='disabled' if en else 'normal')
            self._btn_dis.config(state='normal' if en else 'disabled')
