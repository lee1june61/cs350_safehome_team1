"""Identity verification controller for SecurityPage."""
from __future__ import annotations

from typing import Sequence
from tkinter import Button, StringVar, ttk

from .action_button_controller import ActionButtonController
from .verification_lock import VerificationLockTimer


class IdentityVerificationController:
    """Handle verification workflow, lock timers, and action availability."""

    CONTEXT_KEY = "security_verified"

    def __init__(
        self,
        page,
        entry_var: StringVar,
        entry: ttk.Entry,
        status_label: ttk.Label,
        verify_button: ttk.Button,
        action_buttons: Sequence[Button],
    ):
        self._page = page
        self._entry_var = entry_var
        self._entry = entry
        self._status = status_label
        self._verify_btn = verify_button
        self._actions = ActionButtonController(action_buttons)
        self._lock = VerificationLockTimer(page._frame, status_label, entry, verify_button)

        self._verify_btn.config(command=self.verify)

    @property
    def _frame(self):
        return self._page._frame

    def verify(self):
        value = (self._entry_var.get() or "").strip()
        res = self._page.send_to_system("verify_identity", value=value)
        if res.get("success"):
            self._set_verified(True)
        else:
            message = res.get("message", "Invalid")
            if res.get("locked"):
                seconds = res.get("seconds_remaining") or res.get("lock_duration")
                self._set_locked_state(message, seconds)
            else:
                self._status.config(text=message, foreground="red")

    def on_show(self):
        """Restore verification state when page becomes visible."""
        self._clear_lock_timer()
        if self._page._web_interface.get_context(self.CONTEXT_KEY):
            self._set_verified(True)
        else:
            self._entry_var.set("")
            self._set_verified(False)

    def _set_verified(self, verified: bool):
        self._clear_lock_timer()
        self._page._web_interface.set_context(self.CONTEXT_KEY, verified)
        if verified:
            self._status.config(text="✓ Verified", foreground="green")
            self._entry.config(state="disabled")
            self._verify_btn.config(state="disabled")
            self._set_action_state(enabled=True)
        else:
            self._status.config(
                text="Enter registered phone number",
                foreground="#555",
            )
            self._entry.config(state="normal")
            self._verify_btn.config(state="normal")
            self._set_action_state(enabled=False)

    def _set_action_state(self, *, enabled: bool):
        self._actions.set_enabled(enabled)

    def _set_locked_state(self, message: str, seconds: int | None):
        message = message or "Verification locked"
        seconds = int(seconds or 0)
        self._lock.start(message, seconds, self._unlock_verification)

    def _unlock_verification(self):
        if not self._page._web_interface.get_context(self.CONTEXT_KEY):
            self._entry.config(state="normal")
            self._verify_btn.config(state="normal")
            self._status.config(
                text="Enter registered phone number",
                foreground="#555",
            )

    def _clear_lock_timer(self):
        self._lock.cancel()

