"""Log entity for SafeHome.

Represents a single log entry in the system's event log.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Log:
    """Represents a system event log entry."""

    log_id: Optional[int] = None
    timestamp: datetime = datetime.utcnow()
    event_type: str = "SYSTEM"
    description: str = ""
    severity: str = "INFO"
    user: Optional[str] = None

    def __init__(
        self,
        event_type: str,
        description: str,
        severity: str = "INFO",
        user: Optional[str] = None,
        log_id: Optional[int] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        self.log_id = log_id
        self.timestamp = timestamp or datetime.utcnow()
        self.event_type = event_type
        self.description = description
        self.severity = severity
        self.user = user

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary suitable for persistence."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Log":
        """Create a :class:`Log` from a dictionary (DB row)."""
        ts_raw = data.get("timestamp")
        if isinstance(ts_raw, datetime):
            ts = ts_raw
        elif ts_raw:
            ts = datetime.fromisoformat(str(ts_raw))
        else:
            ts = datetime.utcnow()

        return Log(
            log_id=int(data.get("log_id")) if data.get("log_id") is not None else None,
            timestamp=ts,
            event_type=str(data.get("event_type", "")),
            description=str(data.get("description", "")),
            severity=str(data.get("severity", "INFO")),
            user=data.get("user"),
        )

    def __str__(self) -> str:
        """Return human‑readable representation."""
        return (
            f"[{self.timestamp.isoformat()}] "
            f"{self.severity} {self.event_type}: {self.description}"
        )



