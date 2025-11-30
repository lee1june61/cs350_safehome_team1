"""Log-related command implementations."""

from __future__ import annotations

from typing import Dict, Any

from ...configuration.log_manager import LogManager


class LogHandler:
    """Returns intrusion logs."""

    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def get_intrusion_log(self, **_) -> Dict[str, Any]:
        logs = self._log_manager.get_logs(limit=100)
        log_data = [
            {
                "timestamp": (
                    log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp else ""
                ),
                "event": log.event_type,
                "detail": log.description,
                "severity": log.severity,
            }
            for log in logs
        ]
        return {"success": True, "data": log_data}


