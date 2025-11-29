"""Log represents a single system event entry."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Log:
    """Represents a single log entry."""

    event_type: str
    description: str
    severity: str = "INFO"
    log_id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    user: Optional[str] = None

    def __init__(
        self,
        event_type: str,
        description: str,
        severity: str = "INFO",
        log_id: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        user: Optional[str] = None,
    ) -> None:
        self.event_type = event_type
        self.description = description
        self.severity = severity
        self.log_id = log_id
        self.timestamp = timestamp or datetime.utcnow()
        self.user = user

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "event_type": self.event_type,
            "description": self.description,
            "severity": self.severity,
            "user": self.user,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Log":
        """Create Log from dictionary."""
        timestamp_raw = data.get("timestamp")
        if isinstance(timestamp_raw, str):
            timestamp = datetime.fromisoformat(timestamp_raw)
        elif isinstance(timestamp_raw, datetime):
            timestamp = timestamp_raw
        else:
            timestamp = None

        return Log(
            event_type=data["event_type"],
            description=data["description"],
            severity=data.get("severity", "INFO"),
            log_id=data.get("log_id"),
            timestamp=timestamp,
            user=data.get("user"),
        )

    def __str__(self) -> str:
        """Return string representation."""
        return f"[{self.severity}] {self.event_type}: {self.description}"
