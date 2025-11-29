"""Authentication data model for SafeHome users."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
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
        """Return dictionary representation."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["last_login"] = self.last_login.isoformat() if self.last_login else None
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LoginInterface":
        obj = object.__new__(LoginInterface)
        obj.username, obj.password_hash, obj.interface = (
            data["username"],
            data["password_hash"],
            data["interface"],
        )
        obj.access_level = int(data.get("access_level", AccessLevel.USER_ACCESS))
        obj.login_attempts, obj.is_locked = int(data.get("login_attempts", 0)), bool(
            data.get("is_locked", False)
        )
        obj.password_min_length = int(data.get("password_min_length", 8))
        obj.password_requires_digit = bool(data.get("password_requires_digit", True))
        obj.password_requires_special = bool(
            data.get("password_requires_special", False)
        )
        created = data.get("created_at")
        obj.created_at = (
            datetime.fromisoformat(created)
            if isinstance(created, str)
            else datetime.utcnow()
        )
        obj.last_login = (
            datetime.fromisoformat(data["last_login"])
            if data.get("last_login")
            else None
        )
        return obj
