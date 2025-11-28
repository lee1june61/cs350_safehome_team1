"""Camera access manager - SRS V.3.a Exception 8a."""
from tkinter import messagebox, simpledialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .camera_list_page import CameraListPage


class CameraAccessManager:
    """Manages camera access with password attempts tracking."""

    _attempts: dict = {}
    _locked: dict = {}
    MAX_ATTEMPTS = 3
    LOCK_TIME_MS = 60000

    def __init__(self, page: "CameraListPage"):
        self._page = page

    def is_locked(self, cam_id: str) -> bool:
        """Check if camera is locked."""
        if self._locked.get(cam_id, False):
            messagebox.showerror(
                "Camera Locked",
                f"Camera {cam_id} is locked.\nPlease wait or contact admin."
            )
            return True
        return False

    def verify_password(self, cam_id: str) -> bool:
        """Verify camera password. Returns True if access granted."""
        if cam_id not in self._attempts:
            self._attempts[cam_id] = self.MAX_ATTEMPTS

        pw = simpledialog.askstring("Password", f"Password for {cam_id}:", show="*")
        if not pw:
            return False

        res = self._page.send_to_system(
            "verify_camera_password",
            camera_id=cam_id,
            password=pw
        )

        if res.get("success"):
            self._attempts[cam_id] = self.MAX_ATTEMPTS
            return True

        self._handle_failure(cam_id)
        return False

    def _handle_failure(self, cam_id: str):
        """Handle password failure."""
        self._attempts[cam_id] -= 1
        remaining = self._attempts[cam_id]

        if remaining <= 0:
            self._locked[cam_id] = True
            messagebox.showerror(
                "Camera Locked",
                f"Camera {cam_id} locked for 60 seconds."
            )
            self._page._frame.after(
                self.LOCK_TIME_MS,
                lambda: self._unlock(cam_id)
            )
        else:
            messagebox.showwarning(
                "Wrong Password",
                f"Incorrect. {remaining} attempts left."
            )

    def _unlock(self, cam_id: str):
        """Unlock camera after timeout."""
        self._locked[cam_id] = False
        self._attempts[cam_id] = self.MAX_ATTEMPTS

