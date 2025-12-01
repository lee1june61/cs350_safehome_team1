"""LoginManager - manages login workflow and lockout UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .controllers.login_attempt_guard import LoginAttemptGuard


class LoginManager:
    MAX_ATTEMPTS = 3
    LOCK_SECONDS = 60

    def __init__(
        self,
        page,
        user_var: tk.StringVar,
        pw1_var: tk.StringVar,
        pw2_var: tk.StringVar,
        login_btn: ttk.Button,
        status_msg: ttk.Label,
    ):
        self.page = page
        self._user_var = user_var
        self._pw1_var = pw1_var
        self._pw2_var = pw2_var
        self._login_btn = login_btn
        self._status_msg = status_msg
        self._guard = LoginAttemptGuard(self.MAX_ATTEMPTS, self.LOCK_SECONDS)

    def login(self):
        if self._guard.is_locked():
            return

        user = self._user_var.get().strip()
        p1 = self._pw1_var.get()
        p2 = self._pw2_var.get()

        if not user or not p1 or not p2:
            self._status_msg.config(text="Fill all fields")
            return

        res = self.page.send_to_system("login_web", user_id=user, password1=p1, password2=p2)
        if res.get("success"):
            self._user_var.set("")
            self._pw1_var.set("")
            self._pw2_var.set("")
            self.page._web_interface.set_context("user_id", user)
            self.page.navigate_to("major_function")
            self._guard.reset_attempts()
        else:
            if self._guard.record_failure():
                self._lock()
            else:
                self._status_msg.config(text=f"Failed. {self._guard.remaining_attempts()} left")

    def _lock(self):
        self._login_btn.config(state="disabled")
        self._guard.start_countdown(
            self._schedule,
            tick_fn=lambda remaining: self._status_msg.config(text=f"LOCKED - {remaining}s"),
            unlock_fn=self._unlock,
        )

    def _unlock(self):
        self._guard.reset_attempts()
        self._login_btn.config(state="normal")
        self._status_msg.config(text="Unlocked")

    def _schedule(self, delay_ms: int | str, callback=None) -> str | None:
        """
        Wrapper around after/after_cancel.
        If delay_ms == 'cancel', callback is treated as job id to cancel.
        """
        if delay_ms == "cancel" and callback:
            self.page._frame.after_cancel(callback)
            return None
        return self.page._frame.after(delay_ms, callback)

    def on_show(self):
        """Reset login state when page appears."""
        self._guard.reset_attempts()
        self._login_btn.config(state="normal")
        self._status_msg.config(text="")
