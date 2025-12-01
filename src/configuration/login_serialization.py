"""Serialization helpers for LoginInterface."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .login_interface import LoginInterface


def to_dict(obj: "LoginInterface") -> Dict[str, Any]:
    """Return dictionary representation of LoginInterface."""
    from dataclasses import asdict
    data = asdict(obj)
    data["created_at"] = obj.created_at.isoformat()
    data["last_login"] = obj.last_login.isoformat() if obj.last_login else None
    return data


def from_dict(data: Dict[str, Any]) -> "LoginInterface":
    """Create LoginInterface from dictionary."""
    from .login_interface import LoginInterface, AccessLevel
    obj = object.__new__(LoginInterface)
    obj.username = data["username"]
    obj.password_hash = data["password_hash"]
    obj.interface = data["interface"]
    obj.access_level = int(data.get("access_level", AccessLevel.USER_ACCESS))
    obj.login_attempts = int(data.get("login_attempts", 0))
    obj.is_locked = bool(data.get("is_locked", False))
    obj.password_min_length = int(data.get("password_min_length", 8))
    obj.password_requires_digit = bool(data.get("password_requires_digit", True))
    obj.password_requires_special = bool(data.get("password_requires_special", False))
    created = data.get("created_at")
    obj.created_at = (
        datetime.fromisoformat(created) if isinstance(created, str) else datetime.utcnow()
    )
    obj.last_login = (
        datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None
    )
    return obj

