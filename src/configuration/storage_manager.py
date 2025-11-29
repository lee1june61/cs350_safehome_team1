"""StorageManager - Thread-safe singleton for SQLite access."""

from __future__ import annotations

import sqlite3
import threading
from typing import Any, Dict, List, Optional, Tuple

from .exceptions import DatabaseError
from .storage_schema import SCHEMA_SQL
from .storage_queries import StorageQueries
from .storage_zone_log import StorageZoneLogQueries


class StorageManager(StorageQueries, StorageZoneLogQueries):
    """Thread-safe singleton storage manager using SQLite."""

    _instance: Optional["StorageManager"] = None
    _instance_lock = threading.Lock()

    def __new__(cls, db_config: Dict[str, Any]) -> "StorageManager":  # type: ignore[override]
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls, db_path: str = ":memory:") -> "StorageManager":
        """Get or create singleton instance."""
        return cls({"db_path": db_path})

    def __init__(self, db_config: Dict[str, Any]) -> None:
        if getattr(self, "_initialized", False):
            return
        self.db_path = db_config.get("db_path", ":memory:")
        self.connection: Optional[sqlite3.Connection] = None
        self._connection_lock = threading.Lock()
        self._in_transaction = False
        self._initialized = True

    def connect(self) -> bool:
        """Establish database connection and initialize schema."""
        with self._connection_lock:
            if self.connection is not None:
                return True
            try:
                self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
                self._ensure_schema()
                return True
            except sqlite3.Error as exc:
                raise DatabaseError(f"Failed to connect: {exc}") from exc

    def disconnect(self) -> bool:
        """Close database connection."""
        with self._connection_lock:
            if self.connection:
                if self._in_transaction:
                    self.connection.rollback()
                    self._in_transaction = False
                self.connection.close()
                self.connection = None
            return True

    def is_connected(self) -> bool:
        return self.connection is not None

    def _ensure_schema(self) -> None:
        if self.connection:
            self.connection.executescript(SCHEMA_SQL)
            self.connection.commit()

    def execute_query(
        self, query: str, params: Optional[Tuple] = None
    ) -> List[Dict[str, Any]]:
        if not self.connection:
            raise DatabaseError("Not connected")
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        if not self.connection:
            raise DatabaseError("Not connected")
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor.rowcount

    def execute_insert(
        self, query: str, params: Optional[Tuple] = None
    ) -> Optional[int]:
        if not self.connection:
            raise DatabaseError("Not connected")
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor.lastrowid
