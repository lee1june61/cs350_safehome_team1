"""
Unit tests for ControlPanelLoginHandler and WebLoginHandler with branch coverage focus.
"""

from unittest.mock import Mock

import pytest

from src.configuration import AccessLevel
from src.core.services.auth.lock_manager import LockManager
from src.core.services.auth.login_handler import (
    ControlPanelLoginHandler,
    WebLoginHandler,
)
from src.core.services.auth.user_resolver import ControlPanelUserResolver


class TestControlPanelLoginHandler:
    def _handler(self):
        lock = Mock(spec=LockManager)
        resolver = Mock(spec=ControlPanelUserResolver)
        handler = ControlPanelLoginHandler(lock, resolver)
        return handler, lock, resolver

    def test_attempt_returns_lock_state_when_locked(self):
        handler, lock, resolver = self._handler()
        lock.check_lock.return_value = {"locked": True}

        response = handler.attempt("user", "1234", Mock(), Mock())

        assert response == {"locked": True}
        resolver.resolve.assert_not_called()

    def test_attempt_success_returns_master_level(self):
        handler, lock, resolver = self._handler()
        lock.check_lock.return_value = None
        resolver.resolve.return_value = ["master", "guest"]
        login_fn = Mock(side_effect=[AccessLevel.MASTER_ACCESS])
        on_success = Mock()

        response = handler.attempt("", "1234", login_fn, on_success)

        assert response == {"success": True, "access_level": "MASTER"}
        login_fn.assert_called_once_with("master", "1234", "control_panel")
        on_success.assert_called_once_with("master", AccessLevel.MASTER_ACCESS, "control_panel")
        lock.record_failure.assert_not_called()

    def test_attempt_skips_duplicates_and_returns_failure(self):
        handler, lock, resolver = self._handler()
        lock.check_lock.return_value = None
        resolver.resolve.return_value = ["guest", "guest"]
        login_fn = Mock(return_value=None)
        lock.record_failure.return_value = {"success": False}

        response = handler.attempt("", "0000", login_fn, Mock())

        assert response == {"success": False}
        assert login_fn.call_count == 1  # duplicate skipped
        lock.record_failure.assert_called_once_with()

    def test_attempt_returns_guest_level_when_access_is_guest(self):
        handler, lock, resolver = self._handler()
        lock.check_lock.return_value = None
        resolver.resolve.return_value = ["guest"]
        login_fn = Mock(return_value=AccessLevel.GUEST_ACCESS)
        on_success = Mock()

        response = handler.attempt("", "0000", login_fn, on_success)

        assert response == {"success": True, "access_level": "GUEST"}
        on_success.assert_called_once()


class TestWebLoginHandler:
    def _handler(self):
        lock = Mock(spec=LockManager)
        handler = WebLoginHandler(lock)
        return handler, lock

    def test_attempt_returns_lock_when_locked(self):
        handler, lock = self._handler()
        lock.check_lock.return_value = {"locked": True}

        response = handler.attempt("user", "", "", "", Mock(), Mock())

        assert response == {"locked": True}

    @pytest.mark.parametrize(
        "password1,password2,message",
        [
            ("1234", "", "Enter both passwords"),
            ("", "1234", "Enter both passwords"),
            ("abcd", "efgh", "Passwords do not match"),
        ],
    )
    def test_attempt_password_pair_validation(self, password1, password2, message):
        handler, lock = self._handler()
        lock.check_lock.return_value = None
        lock.record_failure.return_value = {"success": False, "message": message}

        response = handler.attempt("user", "", password1, password2, Mock(), Mock())

        assert response["message"] == message

    def test_attempt_requires_password_when_none_provided(self):
        handler, lock = self._handler()
        lock.check_lock.return_value = None
        lock.record_failure.return_value = {"success": False, "message": "Password required"}

        response = handler.attempt("user", "", "", "", Mock(), Mock())

        assert response["message"] == "Password required"

    def test_attempt_success_invokes_callback(self):
        handler, lock = self._handler()
        lock.check_lock.return_value = None
        login_fn = Mock(return_value=AccessLevel.MASTER_ACCESS)
        on_success = Mock()

        response = handler.attempt("user", "base", "", "", login_fn, on_success)

        assert response == {"success": True}
        login_fn.assert_called_once_with("user", "base", "web")
        on_success.assert_called_once_with("user", AccessLevel.MASTER_ACCESS, "web")

    def test_attempt_failure_records_failure(self):
        handler, lock = self._handler()
        lock.check_lock.return_value = None
        login_fn = Mock(return_value=None)
        lock.record_failure.return_value = {"success": False}

        response = handler.attempt("user", "bad", "", "", login_fn, Mock())

        assert response == {"success": False}
        lock.record_failure.assert_called_once_with()


