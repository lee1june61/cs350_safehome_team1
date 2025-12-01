"""Identity verification handler."""

from __future__ import annotations

from typing import Dict

from .identity_validator import IdentityValidator
from .lock_manager import LockManager


class VerificationHandler:
    """Handles identity verification workflow."""

    def __init__(self, validator: IdentityValidator, lock_manager: LockManager):
        self._identity = validator
        self._lock = lock_manager

    def verify(self, value: str) -> Dict:
        lock = self._lock.check_lock()
        if lock:
            return {**lock, "message": lock.get("message", "Verification locked")}
        success, message = self._identity.verify(value)
        if success:
            self._lock.record_success()
            return {"success": True}
        return self._lock.record_failure(message or "Invalid verification")

    def is_verified(self) -> Dict:
        return {"success": True, "verified": self._identity.verified}

    def set_contact(self, phone: str):
        self._identity.set_expected_phone(phone or "")

    def reset(self):
        self._identity.reset()

    @property
    def verified(self) -> bool:
        return self._identity.verified

