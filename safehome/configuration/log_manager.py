"""LogManager implementation for SafeHome.

Responsible for creating and querying application‑level log entries.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional

from .log import Log
from .storage_manager import StorageManager


class LogManager:
    """High‑level interface for system event logs."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager

    def create_log(
        self, event_type: str, description: str, severity: str = "INFO", user: Optional[str] = None
    ) -> Log:
        """Create a new :class:`Log` instance (not persisted)."""
        return Log(event_type=event_type, description=description, severity=severity, user=user)

    def save_log(self, log: Log) -> bool:
        """Persist a log entry using :class:`StorageManager`."""
        self._storage_manager.save_log(log.to_dict())
        return True

    def get_logs(self, limit: int = 100, event_type: str | None = None) -> List[Log]:
        """Return recent logs, optionally filtered by event type."""
        if event_type is None:
            rows = self._storage_manager.get_logs(limit=limit)
        else:
            rows = self._storage_manager.execute_query(
                """
                SELECT log_id,
                       timestamp,
                       event_type,
                       description,
                       severity,
                       user
                FROM logs
                WHERE event_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (event_type, limit),
            ) or []
        return [Log.from_dict(row) for row in rows]

    def get_logs_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Log]:
        """Return logs within the specified date/time range."""
        rows = self._storage_manager.execute_query(
            """
            SELECT log_id,
                   timestamp,
                   event_type,
                   description,
                   severity,
                   user
            FROM logs
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
            """,
            (start_date.isoformat(), end_date.isoformat()),
        ) or []
        return [Log.from_dict(row) for row in rows]

    def get_intrusion_logs(self) -> List[Log]:
        """Return logs related to intrusion events."""
        rows = self._storage_manager.execute_query(
            """
            SELECT log_id,
                   timestamp,
                   event_type,
                   description,
                   severity,
                   user
            FROM logs
            WHERE event_type = 'INTRUSION'
            ORDER BY timestamp DESC
            """,
        ) or []
        return [Log.from_dict(row) for row in rows]

    def clear_old_logs(self, days_to_keep: int = 30) -> int:
        """Delete logs older than ``days_to_keep`` days.

        Returns:
            Number of deleted log entries.
        """
        cutoff = datetime.utcnow() - timedelta(days=days_to_keep)
        affected = self._storage_manager.execute_update(
            "DELETE FROM logs WHERE timestamp < ?", (cutoff.isoformat(),)
        )
        return affected



