"""Specialized login flows."""

from __future__ import annotations

from typing import Callable

from ....configuration import AccessLevel
from .login_handler import ControlPanelLoginHandler, WebLoginHandler


class ControlPanelLoginFlow:
    """Handles control panel login attempts and logging."""

    def __init__(
        self,
        handler: ControlPanelLoginHandler,
        logger,
        record_success: Callable[[str, int, str], None],
    ):
        self._handler = handler
        self._logger = logger
        self._record_success = record_success

    def login(self, username: str, password: str, login_fn) -> dict:
        result = self._handler.attempt(username, password, login_fn, self._record_success)
        if result.get("success"):
            self._logger.add_event("LOGIN", f"Control panel login: {username}", user=username)
        return result


class WebLoginFlow:
    """Handles web login attempts."""

    def __init__(
        self,
        handler: WebLoginHandler,
        logger,
        record_success: Callable[[str, int, str], None],
    ):
        self._handler = handler
        self._logger = logger
        self._record_success = record_success

    def login(self, user_id: str, password: str, password1: str, password2: str, login_fn) -> dict:
        result = self._handler.attempt(user_id, password, password1, password2, login_fn, self._record_success)
        if result.get("success"):
            self._logger.add_event("LOGIN", f"Web login: {user_id}", user=user_id)
        return result

