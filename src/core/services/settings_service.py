"""System settings helper."""

from __future__ import annotations

from typing import Optional

from ...configuration import ConfigurationManager, SystemSettings, ValidationError
from ..logging.system_logger import SystemLogger


class SettingsService:
    def __init__(self, config_manager: ConfigurationManager, logger: SystemLogger):
        self._config_manager = config_manager
        self._logger = logger
        self._settings: SystemSettings = self._config_manager.get_system_settings()

    def get_settings(self) -> SystemSettings:
        return self._settings

    def update_settings(
        self,
        *,
        delay_time: Optional[int] = None,
        monitor_phone: Optional[str] = None,
        homeowner_phone: Optional[str] = None,
        system_lock_time: Optional[int] = None,
        max_login_attempts: Optional[int] = None,
        session_timeout: Optional[int] = None,
        user: Optional[str] = None,
    ):
        if delay_time is not None:
            self._settings.alarm_delay_time = delay_time
        if monitor_phone is not None:
            self._settings.monitoring_service_phone = monitor_phone
        if homeowner_phone is not None:
            self._settings.homeowner_phone = homeowner_phone
        if system_lock_time is not None:
            self._settings.system_lock_time = system_lock_time
        if max_login_attempts is not None:
            self._settings.max_login_attempts = max_login_attempts
        if session_timeout is not None:
            self._settings.session_timeout = session_timeout

        try:
            success = self._config_manager.update_system_settings(self._settings)
        except ValidationError as exc:
            return {"success": False, "message": str(exc)}
        if success:
            self._logger.add_event(
                "CONFIGURATION", "System settings updated", user=user
            )
            return {"success": True}
        return {"success": False, "message": "Failed to update settings"}

    def reset_to_defaults(self, *, user: Optional[str] = None):
        """Reset all settings to their factory defaults."""
        self._settings = SystemSettings()
        try:
            success = self._config_manager.update_system_settings(self._settings)
        except ValidationError as exc:
            return {"success": False, "message": str(exc)}
        if success:
            self._logger.add_event(
                "CONFIGURATION", "System settings reset to defaults", user=user
            )
            return {"success": True}
        return {"success": False, "message": "Failed to reset settings"}


