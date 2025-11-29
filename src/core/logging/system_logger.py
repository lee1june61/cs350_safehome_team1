"""Wrapper utilities for consistent logging."""

from __future__ import annotations

from typing import Any, List, Optional

from ...configuration.log_manager import LogManager


class SystemLogger:
    """Simplifies LogManager usage and ensures consistent severity labels."""

    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def add_event(
        self,
        event: str,
        detail: str,
        severity: Optional[str] = None,
        user: Optional[str] = None,
    ) -> Any:
        """Create and persist a log entry."""
        severity = severity or (
            "ERROR" if event in {"INTRUSION", "PANIC", "ALARM"} else "INFO"
        )
        log = self._log_manager.create_log(event, detail, severity, user)
        self._log_manager.save_log(log)
        return log

    def latest(self, limit: int = 1) -> List[Any]:
        """Return the most recent log entries."""
        return self._log_manager.get_logs(limit=limit)


