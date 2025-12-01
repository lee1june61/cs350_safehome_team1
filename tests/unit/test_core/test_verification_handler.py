"""
Unit tests for VerificationHandler focusing on branch coverage.
"""

from unittest.mock import Mock

from src.core.services.auth.identity_validator import IdentityValidator
from src.core.services.auth.lock_manager import LockManager
from src.core.services.auth.verification_handler import VerificationHandler


class TestVerificationHandler:
    def _handler(self, *, lock_return=None, identity_result=(True, None)):
        validator = Mock(spec=IdentityValidator)
        validator.verify.return_value = identity_result
        validator.verified = False

        lock = Mock(spec=LockManager)
        lock.check_lock.return_value = lock_return
        lock.record_failure.return_value = {"success": False, "locked": False}

        handler = VerificationHandler(validator, lock)
        return handler, validator, lock

    def test_verify_returns_lock_response_when_locked(self):
        lock_info = {"success": False, "locked": True, "message": "System locked"}
        handler, validator, lock = self._handler(lock_return=lock_info)

        response = handler.verify("1234")

        assert response["locked"] is True
        assert response["message"] == "System locked"
        validator.verify.assert_not_called()
        lock.record_success.assert_not_called()

    def test_verify_success_records_success_and_returns_simple_dict(self):
        handler, validator, lock = self._handler()

        response = handler.verify("9999")

        assert response == {"success": True}
        validator.verify.assert_called_once_with("9999")
        lock.record_success.assert_called_once_with()
        lock.record_failure.assert_not_called()

    def test_verify_failure_delegates_to_lock_manager_with_message(self):
        handler, validator, lock = self._handler(identity_result=(False, "bad input"))

        response = handler.verify("bad")

        lock.record_failure.assert_called_once_with("bad input")
        assert response["success"] is False

    def test_is_verified_and_state_helpers(self):
        handler, validator, lock = self._handler()
        validator.verified = True

        assert handler.is_verified() == {"success": True, "verified": True}

        handler.set_contact(" 010-0000-0000 ")
        validator.set_expected_phone.assert_called_once_with(" 010-0000-0000 ")

        handler.reset()
        validator.reset.assert_called_once_with()



