"""Camera password manager - SRS V.3.c/d."""
from tkinter import messagebox, simpledialog
from typing import TYPE_CHECKING
from .lock_manager import CameraLockManager

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class CameraPasswordManager(CameraLockManager):
    """Manages camera password operations."""

    def set_password(self):
        """Set camera password - SRS V.3.c."""
        if self.is_locked():
            return
        self.init_attempts()

        pw = simpledialog.askstring("Set Password", "New password:", show="*")
        if not pw:
            return

        pw_confirm = simpledialog.askstring("Confirm", "Re-enter:", show="*")
        if pw != pw_confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        old_pw = simpledialog.askstring(
            "Verify", "Current password (empty if none):", show="*")
        res = self._page.send_to_system(
            "set_camera_password",
            camera_id=self._cam_id, old_password=old_pw, password=pw)

        if res.get("success"):
            messagebox.showinfo("Success", "Password set")
            self.reset_attempts()
            self._page._update_info()
            self._page.blank_video("Password set.\nCamera locked.", pause_feed=True)
        else:
            self.handle_failure()

    def delete_password(self):
        """Delete camera password - SRS V.3.d."""
        if self.is_locked():
            return
        self.init_attempts()

        old = simpledialog.askstring("Verify", "Current password:", show="*")
        if old is None:
            return

        res = self._page.send_to_system(
            "delete_camera_password",
            camera_id=self._cam_id, old_password=old)

        if res.get("success"):
            messagebox.showinfo("Success", "Password deleted")
            self.reset_attempts()
            self._page._update_info()
        else:
            self.handle_failure()
