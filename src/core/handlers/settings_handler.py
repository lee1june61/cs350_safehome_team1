"""System settings command implementations."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..services.settings_service import SettingsService
from ..services.alarm_service import AlarmService
from ..services.auth_service import AuthService


class SettingsHandler:
    """Handles system settings queries and updates."""

    def __init__(
        self,
        settings_service: SettingsService,
        alarm_service: AlarmService,
        auth_service: AuthService,
    ):
        self._settings_service = settings_service
        self._alarm_service = alarm_service
        self._auth_service = auth_service

    def get_settings(self, **_) -> Dict[str, Any]:
        settings = self._settings_service.get_settings()
        return {
            "success": True,
            "data": {
                "delay_time": settings.alarm_delay_time,
                "monitor_phone": settings.monitoring_service_phone,
                "homeowner_phone": settings.homeowner_phone,
                "system_lock_time": settings.system_lock_time,
                "max_login_attempts": settings.max_login_attempts,
                "session_timeout": settings.session_timeout,
            },
        }

    def configure_settings(
        self,
        delay_time: Optional[int] = None,
        monitor_phone: Optional[str] = None,
        homeowner_phone: Optional[str] = None,
        system_lock_time: Optional[int] = None,
        max_login_attempts: Optional[int] = None,
        session_timeout: Optional[int] = None,
        master_password: Optional[str] = None,
        guest_password: Optional[str] = None,
        **_,
    ):
        result = self._settings_service.update_settings(
            delay_time=delay_time,
            monitor_phone=monitor_phone,
            homeowner_phone=homeowner_phone,
            system_lock_time=system_lock_time,
            max_login_attempts=max_login_attempts,
            session_timeout=session_timeout,
            user=self._auth_service.current_user,
        )
        if result.get("success"):
            settings = self._settings_service.get_settings()
            self._alarm_service.update_from_settings(
                settings.alarm_delay_time, settings.monitoring_service_phone
            )
            self._auth_service.update_policy(
                max_attempts=settings.max_login_attempts or 3,
                lock_duration=settings.system_lock_time or 60,
            )
            self._auth_service.set_identity_contact(
                settings.monitoring_service_phone
            )
            if master_password or guest_password:
                self._auth_service.update_control_panel_passwords(
                    master_password=master_password, guest_password=guest_password
                )
        return result


