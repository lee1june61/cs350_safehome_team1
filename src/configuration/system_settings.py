"""SystemSettings manages system-wide configuration."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

from .exceptions import ValidationError
from .storage_manager import StorageManager


@dataclass
class SystemSettings:
    """System-wide settings for SafeHome."""

    DEFAULT_MONITOR_PHONE = "010-1234-1234"

    monitoring_service_phone: str = DEFAULT_MONITOR_PHONE
    homeowner_phone: str = ""
    system_lock_time: int = 60
    alarm_delay_time: int = 30
    max_login_attempts: int = 3
    session_timeout: int = 30

    _EMERGENCY_NUMBERS = {"911", "112", "119"}

    def load_from_database(self, storage_manager: StorageManager) -> bool:
        """Load settings from database."""
        data = storage_manager.get_system_settings()
        if not data:
            return False
        self.monitoring_service_phone = data.get(
            "monitoring_service_phone", self.DEFAULT_MONITOR_PHONE
        ) or self.DEFAULT_MONITOR_PHONE
        self.homeowner_phone = data.get("homeowner_phone", "")
        self.system_lock_time = int(data.get("system_lock_time", 60))
        self.alarm_delay_time = int(data.get("alarm_delay_time", 30))
        self.max_login_attempts = int(data.get("max_login_attempts", 3))
        self.session_timeout = int(data.get("session_timeout", 30))
        return True

    def save_to_database(self, storage_manager: StorageManager) -> bool:
        """Save settings to database."""
        error = self._validate_settings_error()
        if error:
            raise ValidationError(error)
        return storage_manager.save_system_settings(asdict(self))

    def _normalize_phone(self, phone: str) -> str:
        return "".join(ch for ch in (phone or "") if ch.isdigit())

    def validate_phone_number(self, phone: str, *, allow_emergency: bool = False) -> bool:
        """Validate phone number format."""
        if not phone:
            return True
        trimmed = phone.strip()
        digits = self._normalize_phone(trimmed)
        if allow_emergency and trimmed in self._EMERGENCY_NUMBERS:
            return True
        if not digits:
            return False
        return 10 <= len(digits) <= 15

    def validate_settings(self) -> bool:
        """Validate all settings; return False if invalid, True if valid."""
        return self._validate_settings_error() is None

    def _validate_settings_error(self) -> Optional[str]:
        if not self.validate_phone_number(
            self.monitoring_service_phone, allow_emergency=True
        ):
            return (
                "Monitoring service phone must be 911, 112, 119 or a 10-15 digit "
                "number (optional leading +)."
            )
        if not self.validate_phone_number(self.homeowner_phone):
            return "Homeowner phone must be a 10-15 digit number (optional leading +)."
        if not (30 <= self.system_lock_time <= 300):
            return "System lock time must be between 30 and 300 seconds."
        if not (5 <= self.alarm_delay_time <= 60):
            return "Alarm delay time must be between 5 and 60 seconds."
        return None

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
