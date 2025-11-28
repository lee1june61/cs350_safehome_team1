"""Camera lock management - SRS V.3.c/d Exception 8a."""
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class CameraLockManager:
    """Manages camera password attempt tracking and locking."""

    _attempts: dict = {}
    _locked: dict = {}
    MAX_ATTEMPTS = 3
    LOCK_TIME_MS = 60000

    def __init__(self, page: "SingleCameraViewPage"):
        self._page = page

    @property
    def _cam_id(self):
        return self._page._cam_id

    def is_locked(self) -> bool:
        if self._locked.get(self._cam_id, False):
            messagebox.showerror(
                "Locked",
                f"Password operations for {self._cam_id} locked.\n"
                "Please wait 60 seconds.")
            return True
        return False
    
    def is_locked_silent(self) -> bool:
        """Check if locked without showing messagebox (for UI updates)."""
        return self._locked.get(self._cam_id, False)

    def init_attempts(self):
        if self._cam_id not in self._attempts:
            self._attempts[self._cam_id] = self.MAX_ATTEMPTS

    def handle_failure(self):
        self.init_attempts()
        self._attempts[self._cam_id] -= 1
        remaining = self._attempts[self._cam_id]

        if remaining <= 0:
            self._locked[self._cam_id] = True
            messagebox.showerror(
                "Locked", "Too many attempts.\nLocked for 60 seconds.")
            self._page._frame.after(self.LOCK_TIME_MS, self._unlock)
        else:
            messagebox.showwarning(
                "Wrong Password", f"Incorrect. {remaining} attempts left.")

    def _unlock(self):
        self._locked[self._cam_id] = False
        self._attempts[self._cam_id] = self.MAX_ATTEMPTS

    def reset_attempts(self):
        self._attempts[self._cam_id] = self.MAX_ATTEMPTS

