"""SystemSettings manages system-wide configuration."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Dict

from .exceptions import ValidationError
from .storage_manager import StorageManager


@dataclass
class SystemSettings:
    """System-wide settings for SafeHome."""

    monitoring_service_phone: str = ""
    homeowner_phone: str = ""
    system_lock_time: int = 60
    alarm_delay_time: int = 30
    max_login_attempts: int = 3
    session_timeout: int = 30

    def load_from_database(self, storage_manager: StorageManager) -> bool:
        """Load settings from database."""
        data = storage_manager.get_system_settings()
        if not data:
            return False
        self.monitoring_service_phone = data.get("monitoring_service_phone", "")
        self.homeowner_phone = data.get("homeowner_phone", "")
        self.system_lock_time = int(data.get("system_lock_time", 60))
        self.alarm_delay_time = int(data.get("alarm_delay_time", 30))
        self.max_login_attempts = int(data.get("max_login_attempts", 3))
        self.session_timeout = int(data.get("session_timeout", 30))
        return True

    def save_to_database(self, storage_manager: StorageManager) -> bool:
        """Save settings to database."""
        if not self.validate_settings():
            raise ValidationError("Invalid settings")
        return storage_manager.save_system_settings(asdict(self))

    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format."""
        if not phone:
            return True
        pattern = r"^\+?[0-9]{10,15}$"
        return bool(re.match(pattern, phone))

    def validate_settings(self) -> bool:
        """Validate all settings; return False if invalid, True if valid."""
        if not self.validate_phone_number(self.monitoring_service_phone):
            return False
        if not self.validate_phone_number(self.homeowner_phone):
            return False
        if not (30 <= self.system_lock_time <= 300):
            return False
        if not (10 <= self.alarm_delay_time <= 60):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SystemSettings":
        """Create SystemSettings from dictionary."""
        return SystemSettings(
            monitoring_service_phone=data.get("monitoring_service_phone", ""),
            homeowner_phone=data.get("homeowner_phone", ""),
            system_lock_time=int(data.get("system_lock_time", 60)),
            alarm_delay_time=int(data.get("alarm_delay_time", 30)),
            max_login_attempts=int(data.get("max_login_attempts", 3)),
            session_timeout=int(data.get("session_timeout", 30)),
        )
