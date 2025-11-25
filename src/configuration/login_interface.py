"""Authentication data model for SafeHome users.

This module defines the :class:`LoginInterface` entity and the
corresponding :class:`AccessLevel` enumeration. It encapsulates all
password handling and account state for a single user/interface pair.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, Optional

from .exceptions import ValidationError


class AccessLevel(IntEnum):
    """Access levels used throughout the system."""

    MASTER_ACCESS = 0x01
    USER_ACCESS = 0x02
    GUEST_ACCESS = 0x03


def _hash_password(raw_password: str) -> str:
    """Return a SHA‑256 hash of the given password.

    For this educational implementation we avoid storing plaintext
    passwords but do not model full production‑grade password hashing
    (e.g., bcrypt, per‑user salts). The hashing strategy can be swapped
    out in one place without affecting callers.
    """
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


@dataclass
class LoginInterface:
    """Represents credentials and state for a single login interface.

    Attributes:
        username: Unique user name.
        password_hash: Hashed password (never plaintext).
        interface: Interface identifier, e.g. "control_panel" or "web".
        access_level: User's access level.
        login_attempts: Number of failed login attempts.
        is_locked: Whether the account is locked.
        password_min_length: Minimum allowed password length.
        password_requires_digit: Whether at least one digit is required.
        password_requires_special: Whether at least one non‑alphanumeric
            character is required.
        created_at: Creation timestamp.
        last_login: Timestamp of last successful login, if any.
    """

    username: str
    password_hash: str
    interface: str
    access_level: int
    login_attempts: int = 0
    is_locked: bool = False
    password_min_length: int = 8
    password_requires_digit: bool = True
    password_requires_special: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    def __init__(
        self,
        username: str,
        password: str,
        interface: str,
        access_level: int,
    ) -> None:
        self.username = username
        self.interface = interface
        self.access_level = int(access_level)
        self.login_attempts = 0
        self.is_locked = False
        self.password_min_length = 8
        self.password_requires_digit = True
        self.password_requires_special = False
        self.created_at = datetime.utcnow()
        self.last_login = None
        # Set initial password using policy.
        self.password_hash = ""
        self.set_password(password)

    # ------------------------------------------------------------------
    # Password operations
    # ------------------------------------------------------------------
    def verify_password(self, password: str) -> bool:
        """Check whether the provided password matches the stored hash."""
        return self.password_hash == _hash_password(password)

    def _validate_password_policy(self, new_password: str) -> None:
        """Validate password against policy; raise on failure."""
        if len(new_password) < self.password_min_length:
            raise ValidationError("Password is shorter than minimum length.")
        if self.password_requires_digit and not any(ch.isdigit() for ch in new_password):
            raise ValidationError("Password must contain at least one digit.")
        if self.password_requires_special and not any(
            not ch.isalnum() for ch in new_password
        ):
            raise ValidationError(
                "Password must contain at least one special character."
            )

    def set_password(self, new_password: str) -> bool:
        """Set a new password after validating the policy."""
        self._validate_password_policy(new_password)
        self.password_hash = _hash_password(new_password)
        return True

    # ------------------------------------------------------------------
    # Login attempt tracking
    # ------------------------------------------------------------------
    def increment_attempts(self) -> int:
        """Increment failed login attempts and return the new value."""
        self.login_attempts += 1
        return self.login_attempts

    def reset_attempts(self) -> None:
        """Reset failed login attempts counter."""
        self.login_attempts = 0

    # ------------------------------------------------------------------
    # Locking helpers
    # ------------------------------------------------------------------
    def lock_account(self) -> None:
        """Lock the account."""
        self.is_locked = True

    def unlock_account(self) -> None:
        """Unlock the account and reset attempts."""
        self.is_locked = False
        self.reset_attempts()

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation suitable for persistence."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["last_login"] = (
            self.last_login.isoformat() if self.last_login is not None else None
        )
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LoginInterface":
        """Create a :class:`LoginInterface` from a persisted dictionary."""
        # Bypass __init__ to avoid re‑hashing the password.
        obj = object.__new__(LoginInterface)
        obj.username = data["username"]
        obj.password_hash = data["password_hash"]
        obj.interface = data["interface"]
        obj.access_level = int(data.get("access_level", AccessLevel.USER_ACCESS))
        obj.login_attempts = int(data.get("login_attempts", 0))
        obj.is_locked = bool(data.get("is_locked", False))
        obj.password_min_length = int(data.get("password_min_length", 8))
        obj.password_requires_digit = bool(data.get("password_requires_digit", True))
        obj.password_requires_special = bool(
            data.get("password_requires_special", False)
        )
        created_at_raw = data.get("created_at")
        if isinstance(created_at_raw, datetime):
            obj.created_at = created_at_raw
        elif created_at_raw:
            obj.created_at = datetime.fromisoformat(str(created_at_raw))
        else:
            obj.created_at = datetime.utcnow()
        last_login_raw = data.get("last_login")
        if isinstance(last_login_raw, datetime):
            obj.last_login = last_login_raw
        elif last_login_raw:
            obj.last_login = datetime.fromisoformat(str(last_login_raw))
        else:
            obj.last_login = None
        return obj



