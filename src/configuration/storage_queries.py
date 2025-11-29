"""Query methods for StorageManager - separated for clarity."""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .storage_manager import StorageManager


class StorageQueries:
    """Mixin class containing all query methods for StorageManager."""

    def get_login_interface(
        self: "StorageManager", username: str, interface: str
    ) -> Optional[Dict[str, Any]]:
        rows = self.execute_query(
            "SELECT * FROM login_interfaces WHERE username = ? AND interface = ?",
            (username, interface),
        )
        return dict(rows[0]) if rows else None

    def save_login_interface(
        self: "StorageManager", login_data: Dict[str, Any]
    ) -> bool:
        username, interface = login_data["username"], login_data["interface"]
        existing = self.get_login_interface(username, interface)
        if existing:
            self.execute_update(
                """UPDATE login_interfaces SET password_hash=?, access_level=?, login_attempts=?, is_locked=?, last_login=? WHERE username=? AND interface=?""",
                (
                    login_data["password_hash"],
                    login_data["access_level"],
                    login_data["login_attempts"],
                    login_data["is_locked"],
                    login_data.get("last_login"),
                    username,
                    interface,
                ),
            )
        else:
            self.execute_insert(
                """INSERT INTO login_interfaces (username, password_hash, interface, access_level, login_attempts, is_locked, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    username,
                    login_data["password_hash"],
                    interface,
                    login_data["access_level"],
                    login_data["login_attempts"],
                    login_data["is_locked"],
                    login_data.get("created_at"),
                ),
            )
        return True

    def get_system_settings(self: "StorageManager") -> Optional[Dict[str, Any]]:
        rows = self.execute_query(
            "SELECT setting_key, setting_value FROM system_settings"
        )
        return (
            {row["setting_key"]: row["setting_value"] for row in rows} if rows else None
        )

    def save_system_settings(self: "StorageManager", settings: Dict[str, Any]) -> bool:
        for key, value in settings.items():
            self.execute_query(
                "INSERT OR REPLACE INTO system_settings (setting_key, setting_value) VALUES (?, ?)",
                (key, str(value)),
            )
        return True

    def get_safehome_modes(self: "StorageManager") -> List[Dict[str, Any]]:
        rows = self.execute_query("SELECT * FROM safehome_modes ORDER BY mode_id")
        return rows or []

    def save_safehome_mode(self: "StorageManager", mode: Dict[str, Any]) -> bool:
        sensor_ids_json = json.dumps(mode.get("sensor_ids", []))
        mode_id = mode.get("mode_id")
        self.execute_query(
            """INSERT OR REPLACE INTO safehome_modes (mode_id, mode_name, sensor_ids, is_active, description) VALUES (?, ?, ?, ?, ?)""",
            (
                mode_id,
                mode["mode_name"],
                sensor_ids_json,
                mode.get("is_active", True),
                mode.get("description"),
            ),
        )
        return True
