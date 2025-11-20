"""SystemSettings implementation for SafeHome configuration.

This module models global configuration parameters such as phone numbers,
lock times, and alarm delay intervals. It knows how to persist itself
via :class:`StorageManager`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Dict

from .exceptions import ValidationError
from .storage_manager import StorageManager


@dataclass
class SystemSettings:
    """Container for global SafeHome system settings."""

    monitoring_service_phone: str = ""
    homeowner_phone: str = ""
    system_lock_time: int = 60
    alarm_delay_time: int = 30
    max_login_attempts: int = 3
    session_timeout: int = 15

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def load_from_database(self, storage_manager: StorageManager) -> bool:
        """Load settings from the database, falling back to defaults."""
        data = storage_manager.get_system_settings()
        if not data:
            return False

        self.monitoring_service_phone = data.get("monitoring_service_phone", "")
        self.homeowner_phone = data.get("homeowner_phone", "")
        self.system_lock_time = int(data.get("system_lock_time", self.system_lock_time))
        self.alarm_delay_time = int(
            data.get("alarm_delay_time", self.alarm_delay_time)
        )
        self.max_login_attempts = int(
            data.get("max_login_attempts", self.max_login_attempts)
        )
        self.session_timeout = int(data.get("session_timeout", self.session_timeout))
        return True

    def save_to_database(self, storage_manager: StorageManager) -> bool:
        """Persist current settings to the database."""
        if not self.validate_settings():
            raise ValidationError("System settings validation failed.")
        storage_manager.save_system_settings(self.to_dict())
        return True

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format (10–15 digits, optional +)."""
        if not phone:
            return True
        pattern = r"^\+?\d{10,15}$"
        return bool(re.match(pattern, phone))

    def validate_settings(self) -> bool:
        """Validate all settings according to SDS rules."""
        if not self.validate_phone_number(self.monitoring_service_phone):
            return False
        if not self.validate_phone_number(self.homeowner_phone):
            return False

        if not (30 <= self.system_lock_time <= 300):
            return False
        if not (10 <= self.alarm_delay_time <= 60):
            return False
        if self.max_login_attempts <= 0:
            return False
        if self.session_timeout <= 0:
            return False
        return True

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary suitable for persistence."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SystemSettings":
        """Create settings instance from a dictionary."""
        settings = SystemSettings()
        settings.monitoring_service_phone = data.get(
            "monitoring_service_phone", settings.monitoring_service_phone
        )
        settings.homeowner_phone = data.get(
            "homeowner_phone", settings.homeowner_phone
        )
        settings.system_lock_time = int(
            data.get("system_lock_time", settings.system_lock_time)
        )
        settings.alarm_delay_time = int(
            data.get("alarm_delay_time", settings.alarm_delay_time)
        )
        settings.max_login_attempts = int(
            data.get("max_login_attempts", settings.max_login_attempts)
        )
        settings.session_timeout = int(
            data.get("session_timeout", settings.session_timeout)
        )
        return settings



