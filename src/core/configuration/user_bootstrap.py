"""Default user provisioning helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from ...configuration import AccessLevel, StorageManager
from ...configuration.password_utils import hash_password


class UserBootstrap:
    """Provision default users for a fresh install."""

    POLICY_FIELDS = (
        "login_attempts",
        "is_locked",
        "password_min_length",
        "password_requires_digit",
        "password_requires_special",
    )

    def __init__(self, storage: StorageManager):
        self._storage = storage

    def ensure_defaults(self):
        self._ensure_user("master", "1234", "control_panel", AccessLevel.MASTER_ACCESS)
        self._ensure_user("guest", "5678", "control_panel", AccessLevel.GUEST_ACCESS)
        self._ensure_user("admin", "password", "web", AccessLevel.MASTER_ACCESS)
        self._ensure_user("homeowner", "password", "web", AccessLevel.MASTER_ACCESS)

    def _ensure_user(
        self,
        username: str,
        password: str,
        interface: str,
        access_level: AccessLevel,
        extra: Optional[Dict] = None,
    ):
        record = self._build_record(username, password, interface, access_level, extra)
        existing = self._storage.get_login_interface(username, interface)
        if existing:
            self._update_if_needed(existing, record)
        else:
            self._storage.save_login_interface(record)

    def _build_record(
        self,
        username: str,
        password: str,
        interface: str,
        access_level: AccessLevel,
        extra: Optional[Dict],
    ) -> Dict:
        record = {
            "username": username,
            "password_hash": hash_password(password),
            "interface": interface,
            "access_level": int(access_level),
            "login_attempts": 0,
            "is_locked": False,
            "password_min_length": 4,
            "password_requires_digit": False,
            "password_requires_special": False,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None,
        }
        if extra:
            record.update(extra)
        return record

    def _update_if_needed(self, existing: Dict, desired: Dict):
        needs_update = False
        updated = existing.copy()
        if not updated.get("password_hash"):
            updated["password_hash"] = desired["password_hash"]
            needs_update = True
        for key in self.POLICY_FIELDS:
            if desired.get(key) is not None and updated.get(key) != desired[key]:
                updated[key] = desired[key]
                needs_update = True
        if needs_update:
            self._storage.save_login_interface(updated)
