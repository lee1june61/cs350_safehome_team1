"""StorageManager implementation for SafeHome configuration subsystem.

This class acts as the repository/DAO layer and encapsulates all direct
SQLite access. It is implemented as a process-wide singleton and is
thread-safe for concurrent access from multiple threads.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .exceptions import DatabaseError


class StorageManager:
    """Thread-safe, singleton storage manager using SQLite.

    The API is intentionally minimal and works with dictionaries so that
    higher layers remain decoupled from SQL and persistence details.
    """

    _instance: Optional["StorageManager"] = None
    _instance_lock = threading.Lock()

    def __new__(cls, db_config: Dict[str, Any]) -> "StorageManager":  # type: ignore[override]
        """Enforce singleton semantics.

        Args:
            db_config: Configuration dictionary. Supported keys:
                - "db_path": Path to SQLite database file. Defaults to ":memory:".

        Returns:
            The singleton instance of :class:`StorageManager`.
        """
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_config: Dict[str, Any]) -> None:
        # Guard against repeated __init__ calls due to singleton.
        if getattr(self, "_initialized", False):
            return

        self.db_host: str = db_config.get("db_host", "")
        self.db_port: int = int(db_config.get("db_port", 0) or 0)
        self.db_name: str = db_config.get("db_name", "")
        self.db_user: str = db_config.get("db_user", "")
        self.db_password: str = db_config.get("db_password", "")
        self.db_path: str = db_config.get("db_path", ":memory:")

        self.connection: Optional[sqlite3.Connection] = None
        self._connection_lock = threading.RLock()
        self._in_transaction = False

        self._initialized = True

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------
    def connect(self) -> bool:
        """Establish a database connection if not already connected.

        Returns:
            True if the connection is open or has been successfully opened.

        Raises:
            DatabaseError: If the connection attempt fails.
        """
        with self._connection_lock:
            if self.connection is not None:
                return True

            try:
                self.connection = sqlite3.connect(
                    self.db_path,
                    detect_types=sqlite3.PARSE_DECLTYPES,
                    check_same_thread=False,
                )
                self.connection.row_factory = sqlite3.Row
                self._ensure_schema()
                return True
            except sqlite3.Error as exc:  # pragma: no cover - defensive
                raise DatabaseError(f"Failed to connect to database: {exc}") from exc

    def disconnect(self) -> bool:
        """Close the active database connection, if any."""
        with self._connection_lock:
            if self.connection is None:
                return True
            try:
                if self._in_transaction:
                    self.connection.rollback()
                    self._in_transaction = False
                self.connection.close()
                self.connection = None
                return True
            except sqlite3.Error as exc:  # pragma: no cover - defensive
                raise DatabaseError(f"Failed to disconnect from database: {exc}") from exc

    def is_connected(self) -> bool:
        """Return True if there is an active database connection."""
        return self.connection is not None

    # ------------------------------------------------------------------
    # Generic query helpers
    # ------------------------------------------------------------------
    def execute_query(
        self,
        query: str,
        params: Tuple[Any, ...] | None = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query and return a list of dictionaries.

        Args:
            query: SQL query string with parameter placeholders.
            params: Tuple of parameters for the query.

        Returns:
            List of rows as dictionaries, or None if an error occurs.

        Raises:
            DatabaseError: If execution fails.
        """
        with self._connection_lock:
            self.connect()
            assert self.connection is not None  # for type checkers
            try:
                cursor = self.connection.execute(query, params or ())
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            except sqlite3.Error as exc:
                raise DatabaseError(f"Failed to execute query: {exc}") from exc

    def execute_update(
        self,
        query: str,
        params: Tuple[Any, ...] | None = None,
    ) -> int:
        """Execute an UPDATE or DELETE statement.

        Args:
            query: SQL query string.
            params: Optional parameters.

        Returns:
            Number of affected rows.

        Raises:
            DatabaseError: If execution fails.
        """
        with self._connection_lock:
            self.connect()
            assert self.connection is not None
            try:
                cursor = self.connection.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
            except sqlite3.Error as exc:
                self.connection.rollback()
                raise DatabaseError(f"Failed to execute update: {exc}") from exc

    def execute_insert(
        self,
        query: str,
        params: Tuple[Any, ...] | None = None,
    ) -> Optional[int]:
        """Execute an INSERT statement and return the new row ID."""
        with self._connection_lock:
            self.connect()
            assert self.connection is not None
            try:
                cursor = self.connection.execute(query, params or ())
                self.connection.commit()
                return int(cursor.lastrowid)
            except sqlite3.Error as exc:
                self.connection.rollback()
                raise DatabaseError(f"Failed to execute insert: {exc}") from exc

    # ------------------------------------------------------------------
    # Transaction control
    # ------------------------------------------------------------------
    def begin_transaction(self) -> bool:
        """Begin a database transaction."""
        with self._connection_lock:
            self.connect()
            assert self.connection is not None
            if self._in_transaction:
                return True
            try:
                self.connection.execute("BEGIN")
                self._in_transaction = True
                return True
            except sqlite3.Error as exc:
                raise DatabaseError(f"Failed to begin transaction: {exc}") from exc

    def commit_transaction(self) -> bool:
        """Commit the active transaction."""
        with self._connection_lock:
            if not self._in_transaction or self.connection is None:
                return True
            try:
                self.connection.commit()
                self._in_transaction = False
                return True
            except sqlite3.Error as exc:
                raise DatabaseError(f"Failed to commit transaction: {exc}") from exc

    def rollback_transaction(self) -> bool:
        """Rollback the active transaction."""
        with self._connection_lock:
            if not self._in_transaction or self.connection is None:
                return True
            try:
                self.connection.rollback()
                self._in_transaction = False
                return True
            except sqlite3.Error as exc:
                raise DatabaseError(f"Failed to rollback transaction: {exc}") from exc

    # ------------------------------------------------------------------
    # Specific data access methods
    # ------------------------------------------------------------------
    # Login interfaces --------------------------------------------------
    def get_login_interface(self, username: str, interface: str) -> Optional[Dict[str, Any]]:
        """Retrieve login interface record for the given user and interface."""
        rows = self.execute_query(
            """
            SELECT username,
                   password_hash,
                   interface,
                   access_level,
                   login_attempts,
                   is_locked,
                   last_login
            FROM login_interfaces
            WHERE username = ? AND interface = ?
            """,
            (username, interface),
        )
        if not rows:
            return None
        return rows[0]

    def save_login_interface(self, login_data: Dict[str, Any]) -> bool:
        """Insert or update login interface information."""
        last_login = login_data.get("last_login")
        if isinstance(last_login, datetime):
            last_login_value: Any = last_login.isoformat()
        else:
            last_login_value = last_login

        self.execute_insert(
            """
            INSERT INTO login_interfaces (
                username,
                password_hash,
                interface,
                access_level,
                login_attempts,
                is_locked,
                last_login
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username, interface) DO UPDATE SET
                password_hash = excluded.password_hash,
                access_level = excluded.access_level,
                login_attempts = excluded.login_attempts,
                is_locked = excluded.is_locked,
                last_login = excluded.last_login
            """,
            (
                login_data.get("username"),
                login_data.get("password_hash"),
                login_data.get("interface"),
                int(login_data.get("access_level", 0)),
                int(login_data.get("login_attempts", 0)),
                bool(login_data.get("is_locked", False)),
                last_login_value,
            ),
        )
        return True

    # System settings ---------------------------------------------------
    def get_system_settings(self) -> Optional[Dict[str, Any]]:
        """Return system settings as a flat key/value dictionary."""
        rows = self.execute_query(
            """
            SELECT setting_key, setting_value
            FROM system_settings
            """,
        )
        if rows is None:
            return None
        return {row["setting_key"]: row["setting_value"] for row in rows}

    def save_system_settings(self, settings: Dict[str, Any]) -> bool:
        """Persist system settings key/value pairs."""
        for key, value in settings.items():
            self.execute_insert(
                """
                INSERT INTO system_settings (setting_key, setting_value)
                VALUES (?, ?)
                ON CONFLICT(setting_key) DO UPDATE SET
                    setting_value = excluded.setting_value
                """,
                (key, str(value)),
            )
        return True

    # SafeHome modes ----------------------------------------------------
    def get_safehome_modes(self) -> List[Dict[str, Any]]:
        """Return all SafeHome modes."""
        rows = self.execute_query(
            """
            SELECT mode_id,
                   mode_name,
                   sensor_ids,
                   is_active
            FROM safehome_modes
            ORDER BY mode_id
            """,
        )
        return rows or []

    def save_safehome_mode(self, mode: Dict[str, Any]) -> bool:
        """Insert or update a SafeHome mode."""
        sensor_ids_json = json.dumps(mode.get("sensor_ids", []))
        self.execute_insert(
            """
            INSERT INTO safehome_modes (
                mode_id,
                mode_name,
                sensor_ids,
                is_active
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(mode_id) DO UPDATE SET
                mode_name = excluded.mode_name,
                sensor_ids = excluded.sensor_ids,
                is_active = excluded.is_active
            """,
            (
                int(mode.get("mode_id")),
                mode.get("mode_name"),
                sensor_ids_json,
                bool(mode.get("is_active", True)),
            ),
        )
        return True

    # Safety zones ------------------------------------------------------
    def get_safety_zones(self) -> List[Dict[str, Any]]:
        """Return all safety zones."""
        rows = self.execute_query(
            """
            SELECT zone_id,
                   zone_name,
                   sensor_ids,
                   is_armed,
                   description
            FROM safety_zones
            ORDER BY zone_id
            """,
        )
        return rows or []

    def save_safety_zone(self, zone: Dict[str, Any]) -> bool:
        """Insert or update a safety zone."""
        sensor_ids_json = json.dumps(zone.get("sensor_ids", []))
        zone_id = zone.get("zone_id")
        if zone_id is None:
            new_id = self.execute_insert(
                """
                INSERT INTO safety_zones (
                    zone_name,
                    sensor_ids,
                    is_armed,
                    description
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    zone.get("zone_name"),
                    sensor_ids_json,
                    bool(zone.get("is_armed", False)),
                    zone.get("description"),
                ),
            )
            if new_id is not None:
                zone["zone_id"] = new_id
        else:
            self.execute_update(
                """
                UPDATE safety_zones
                SET zone_name = ?,
                    sensor_ids = ?,
                    is_armed = ?,
                    description = ?
                WHERE zone_id = ?
                """,
                (
                    zone.get("zone_name"),
                    sensor_ids_json,
                    bool(zone.get("is_armed", False)),
                    zone.get("description"),
                    int(zone_id),
                ),
            )
        return True

    def delete_safety_zone(self, zone_id: int) -> bool:
        """Delete a safety zone by identifier."""
        affected = self.execute_update(
            "DELETE FROM safety_zones WHERE zone_id = ?",
            (zone_id,),
        )
        return affected > 0

    # Logs --------------------------------------------------------------
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Return the most recent log entries."""
        rows = self.execute_query(
            """
            SELECT log_id,
                   timestamp,
                   event_type,
                   description,
                   severity,
                   user
            FROM logs
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        return rows or []

    def save_log(self, log: Dict[str, Any]) -> bool:
        """Persist a log record."""
        timestamp = log.get("timestamp")
        if isinstance(timestamp, datetime):
            timestamp_value: Any = timestamp.isoformat()
        else:
            timestamp_value = timestamp

        self.execute_insert(
            """
            INSERT INTO logs (
                timestamp,
                event_type,
                description,
                severity,
                user
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                timestamp_value,
                log.get("event_type"),
                log.get("description"),
                log.get("severity"),
                log.get("user"),
            ),
        )
        return True

    # ------------------------------------------------------------------
    # Schema bootstrap
    # ------------------------------------------------------------------
    def _ensure_schema(self) -> None:
        """Create required tables if they do not already exist.

        This uses the schema defined in the SDS/SRS, adapted for SQLite
        with IF NOT EXISTS guards. It is intentionally minimal so that
        integration tests can rely on a clean, working schema without
        requiring an external setup script.
        """
        assert self.connection is not None
        cursor = self.connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS login_interfaces (
                username TEXT,
                password_hash TEXT,
                interface TEXT,
                access_level INTEGER,
                login_attempts INTEGER,
                is_locked BOOLEAN,
                last_login TIMESTAMP,
                PRIMARY KEY (username, interface)
            );

            CREATE TABLE IF NOT EXISTS system_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT
            );

            CREATE TABLE IF NOT EXISTS safehome_modes (
                mode_id INTEGER PRIMARY KEY,
                mode_name TEXT,
                sensor_ids TEXT,
                is_active BOOLEAN
            );

            CREATE TABLE IF NOT EXISTS safety_zones (
                zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                zone_name TEXT,
                sensor_ids TEXT,
                is_armed BOOLEAN,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                event_type TEXT,
                description TEXT,
                severity TEXT,
                user TEXT
            );
            """
        )
        self.connection.commit()


