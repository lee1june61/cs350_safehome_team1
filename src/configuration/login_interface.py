"""Authentication data model for SafeHome users."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, Optional

from .password_utils import hash_password, validate_password_policy


class AccessLevel(IntEnum):
    """Access levels used throughout the system."""

    MASTER_ACCESS = 0x01
    USER_ACCESS = 0x02
    GUEST_ACCESS = 0x03


@dataclass
class LoginInterface:
    """Represents credentials and state for a single login interface."""

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
        self, username: str, password: str, interface: str, access_level: int
    ) -> None:
        self.username, self.interface, self.access_level = (
            username,
            interface,
            int(access_level),
        )
        self.login_attempts, self.is_locked, self.last_login = 0, False, None
        (
            self.password_min_length,
            self.password_requires_digit,
            self.password_requires_special,
        ) = (8, True, False)
        self.created_at, self.password_hash = datetime.utcnow(), ""
        self.set_password(password)

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hash_password(password)

    def set_password(self, new_password: str) -> bool:
        validate_password_policy(
            new_password,
            self.password_min_length,
            self.password_requires_digit,
            self.password_requires_special,
        )
        self.password_hash = hash_password(new_password)
        return True

    def increment_attempts(self) -> int:
        self.login_attempts += 1
        return self.login_attempts

    def reset_attempts(self) -> None:
        self.login_attempts = 0

    def lock_account(self) -> None:
        self.is_locked = True

    def unlock_account(self) -> None:
        self.is_locked, self.login_attempts = False, 0

    def to_dict(self) -> Dict[str, Any]:
        from .login_serialization import to_dict

        return to_dict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LoginInterface":
        from .login_serialization import from_dict

        return from_dict(data)
