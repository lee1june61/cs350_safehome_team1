"""Zone and Log query methods for StorageManager."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .storage_manager import StorageManager


class StorageZoneLogQueries:
    """Mixin for safety zone and log queries."""

    def get_safety_zones(self: "StorageManager") -> List[Dict[str, Any]]:
        """Retrieve all safety zones."""
        rows = self.execute_query(
            "SELECT zone_id, zone_name, sensor_ids, is_armed, description FROM safety_zones ORDER BY zone_id"
        )
        return rows or []

    def save_safety_zone(self: "StorageManager", zone: Dict[str, Any]) -> bool:
        """Insert or update a safety zone."""
        sensor_ids_json = json.dumps(zone.get("sensor_ids", []))
        zone_id = zone.get("zone_id")

        if zone_id is None:
            new_id = self.execute_insert(
                """INSERT INTO safety_zones (zone_name, sensor_ids, is_armed, description)
                   VALUES (?, ?, ?, ?)""",
                (
                    zone["zone_name"],
                    sensor_ids_json,
                    zone.get("is_armed", False),
                    zone.get("description"),
                ),
            )
            if new_id:
                zone["zone_id"] = new_id
        else:
            self.execute_update(
                """UPDATE safety_zones SET zone_name=?, sensor_ids=?, is_armed=?, description=?
                   WHERE zone_id=?""",
                (
                    zone["zone_name"],
                    sensor_ids_json,
                    zone.get("is_armed", False),
                    zone.get("description"),
                    zone_id,
                ),
            )
        return True

    def delete_safety_zone(self: "StorageManager", zone_id: int) -> bool:
        """Delete a safety zone."""
        affected = self.execute_update(
            "DELETE FROM safety_zones WHERE zone_id = ?", (zone_id,)
        )
        return affected > 0

    def get_logs(self: "StorageManager", limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent log entries."""
        rows = self.execute_query(
            """SELECT log_id, timestamp, event_type, description, severity, user
               FROM logs ORDER BY log_id DESC LIMIT ?""",
            (limit,),
        )
        return rows or []

    def save_log(self: "StorageManager", log: Dict[str, Any]) -> bool:
        """Save a log entry."""
        timestamp = log.get("timestamp")
        if isinstance(timestamp, datetime):
            timestamp_value = timestamp.isoformat()
        elif timestamp:
            timestamp_value = timestamp
        else:
            timestamp_value = datetime.utcnow().isoformat()

        self.execute_insert(
            """INSERT INTO logs (timestamp, event_type, description, severity, user)
               VALUES (?, ?, ?, ?, ?)""",
            (
                timestamp_value,
                log.get("event_type"),
                log.get("description"),
                log.get("severity"),
                log.get("user"),
            ),
        )
        return True
