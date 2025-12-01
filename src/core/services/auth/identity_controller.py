"""Identity verification controller."""

from __future__ import annotations

from typing import Optional

from .identity_validator import IdentityValidator
from .lock_manager import LockManager
from .verification_handler import VerificationHandler


class IdentityController:
    """Encapsulate identity verification and contact updates."""

    def __init__(self, max_attempts: int, lock_duration: int):
        self._verification = VerificationHandler(
            IdentityValidator(),
            LockManager(max_attempts, lock_duration),
        )

    def verify(self, value: str = "") -> dict:
        return self._verification.verify(value)

    def is_verified(self) -> dict:
        return self._verification.is_verified()

    def set_contact(self, phone: Optional[str]):
        self._verification.set_contact(phone or "")

    def reset(self):
        self._verification.reset()

