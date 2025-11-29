"""SafeHome mode command implementations."""

from __future__ import annotations

from typing import Dict, Any, List

from ..services.mode_service import ModeService


class ModeHandler:
    """Handles mode configuration queries and updates."""

    def __init__(self, mode_service: ModeService, auth_service):
        self._mode_service = mode_service
        self._auth_service = auth_service

    def get_mode_configuration(self, mode="", **_) -> Dict[str, Any]:
        return self._mode_service.get_mode_configuration(mode)

    def configure_mode(self, mode="", sensors=None, **_) -> Dict[str, Any]:
        sensors = sensors or []
        return self._mode_service.configure_mode(
            mode, sensors, self._auth_service.current_user
        )

    def get_all_modes(self, **_) -> Dict[str, Any]:
        return self._mode_service.get_all_modes()


