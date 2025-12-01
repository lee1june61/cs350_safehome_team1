"""
Unit tests for password handler logic covering both change and control-panel flows.
"""

from unittest.mock import Mock

import pytest

from src.configuration import AccessLevel, LoginInterface
from src.core.services.auth.lock_manager import LockManager
from src.core.services.auth.password_handler import (
    ControlPanelPasswordHandler,
    PasswordChangeHandler,
)


class TestPasswordChangeHandler:
    def _handler(self):
        login_manager = Mock()
        logger = Mock()
        lock_manager = Mock(spec=LockManager)
        handler = PasswordChangeHandler(login_manager, logger, lock_manager)
        return handler, login_manager, logger

    def test_change_requires_login_when_not_authenticated(self):
        handler, login_manager, logger = self._handler()
        ensure_auth = Mock(return_value=False)

        result = handler.change(
            current_user=None,
            username="guest",
            current_password="0000",
            new_password="1234",
            interface="control_panel",
            ensure_auth_fn=ensure_auth,
        )

        assert result == {"success": False, "message": "Must be logged in"}
        login_manager.change_password.assert_not_called()
        logger.add_event.assert_not_called()

    def test_change_success_logs_event(self):
        handler, login_manager, logger = self._handler()
        ensure_auth = Mock(return_value=True)
        login_manager.change_password.return_value = True

        result = handler.change(
            current_user="master",
            username="",
            current_password="oldpass",
            new_password="newpass1",
            interface="control_panel",
            ensure_auth_fn=ensure_auth,
        )

        assert result == {"success": True}
        login_manager.change_password.assert_called_once_with(
            "master", "oldpass", "newpass1", "control_panel"
        )
        logger.add_event.assert_called_once()

    def test_change_failure_returns_message(self):
        handler, login_manager, logger = self._handler()
        ensure_auth = Mock(return_value=True)
        login_manager.change_password.return_value = False

        result = handler.change(
            current_user="master",
            username="guest",
            current_password="oldpass",
            new_password="newpass1",
            interface="control_panel",
            ensure_auth_fn=ensure_auth,
        )

        assert result == {"success": False, "message": "Password change failed"}

    def test_change_handles_exception(self):
        handler, login_manager, logger = self._handler()
        ensure_auth = Mock(return_value=True)
        login_manager.change_password.side_effect = RuntimeError("boom")

        result = handler.change(
            current_user="master",
            username="guest",
            current_password="oldpass",
            new_password="newpass1",
            interface="control_panel",
            ensure_auth_fn=ensure_auth,
        )

        assert result == {"success": False, "message": "boom"}

    def test_change_prevents_duplicate_master_guest_pins(self):
        handler, login_manager, logger = self._handler()
        ensure_auth = Mock(return_value=True)
        storage = Mock(spec=StorageManager)
        handler._login_manager._storage_manager = storage
        # simulate other user (guest) already using "0000"
        other_login = LoginInterface("guest", "0000", "control_panel", AccessLevel.GUEST_ACCESS)
        storage.get_login_interface.return_value = other_login.to_dict()

        result = handler.change(
            current_user="master",
            username="master",
            current_password="oldpass",
            new_password="0000",
            interface="control_panel",
            ensure_auth_fn=ensure_auth,
        )

        assert result == {"success": False, "message": "PIN already in use by another account"}
        login_manager.change_password.assert_not_called()


class StubStorage:
    def __init__(self):
        self.records = {}
        self.saved = []

    def add_user(self, username: str, password: str):
        login_if = LoginInterface(
            username=username,
            password=password,
            interface="control_panel",
            access_level=AccessLevel.USER_ACCESS,
        )
        self.records[(username, "control_panel")] = login_if.to_dict()

    def get_login_interface(self, username, interface):
        return self.records.get((username, interface))

    def save_login_interface(self, data):
        self.saved.append(data)
        self.records[(data["username"], data["interface"])] = data


class TestControlPanelPasswordHandler:
    def _handler(self):
        storage = StubStorage()
        lock = Mock(spec=LockManager)
        handler = ControlPanelPasswordHandler(storage, lock)
        return handler, storage, lock

    def test_verify_short_circuits_when_locked(self):
        handler, storage, lock = self._handler()
        lock.check_lock.return_value = {"locked": True}

        result = handler.verify("1234", True, Mock())

        assert result == {"locked": True}

    def test_verify_requires_password(self):
        handler, storage, lock = self._handler()
        lock.check_lock.return_value = None
        lock.record_failure.return_value = {"success": False, "message": "Password required"}

        result = handler.verify("", True, Mock())

        assert result["message"] == "Password required"

    def test_verify_success_and_failure_paths(self):
        handler, storage, lock = self._handler()
        lock.check_lock.return_value = None
        validator = Mock(side_effect=[True, False])
        lock.record_failure.return_value = {"success": False, "message": "Incorrect password"}

        success = handler.verify("1111", True, validator)
        assert success == {"success": True}
        lock.record_success.assert_called_once_with()

        failure = handler.verify("0000", False, validator)
        assert failure["message"] == "Incorrect password"

    def test_update_passwords_updates_existing_records(self):
        handler, storage, lock = self._handler()
        storage.add_user("master", "master11")
        storage.add_user("guest", "guest22A")

        result = handler.update_passwords(master_password="1234", guest_password="5678")

        assert result == {"success": True}
        assert storage.records[("master", "control_panel")]["password_hash"] != storage.records[
            ("guest", "control_panel")
        ]["password_hash"]

    def test_update_passwords_handles_missing_users(self):
        handler, storage, lock = self._handler()

        result = handler.update_passwords(master_password=None, guest_password="5678")

        assert result == {"success": False, "message": "Guest PIN not found."}

    def test_update_passwords_blocks_matching_pins(self):
        handler, storage, lock = self._handler()
        storage.add_user("master", "master11")
        storage.add_user("guest", "guest22A")

        # Attempt to change master to current guest PIN -> should be rejected
        result = handler.update_passwords(master_password="guest22A", guest_password=None)
        assert result["success"] is False
        assert "Master PIN unchanged" in result["message"]

        # Master remains original; attempting to set guest equal to master should fail
        result = handler.update_passwords(master_password=None, guest_password="master11")
        assert result["success"] is False
        assert "Guest PIN unchanged" in result["message"]

