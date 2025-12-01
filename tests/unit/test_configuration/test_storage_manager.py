"""Unit tests for StorageManager class."""

import unittest
import os
import tempfile
from src.configuration.storage_manager import StorageManager
from src.configuration.exceptions import DatabaseError
from src.configuration.login_interface import LoginInterface, AccessLevel


class TestStorageManager(unittest.TestCase):
    """Test StorageManager database operations."""

    def setUp(self):
        """Create temporary database for each test."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Reset singleton for testing
        StorageManager._instance = None

        self.storage = StorageManager({"db_path": self.db_path})

    def tearDown(self):
        """Clean up temporary database."""
        if self.storage.is_connected():
            self.storage.disconnect()

        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

        # Reset singleton
        StorageManager._instance = None

    def test_storage_manager_creation(self):
        """Test StorageManager instantiation."""
        self.assertIsNotNone(self.storage)
        self.assertEqual(self.storage.db_path, self.db_path)

    def test_singleton_pattern(self):
        """Test that StorageManager follows singleton pattern."""
        storage2 = StorageManager({"db_path": self.db_path})
        self.assertIs(self.storage, storage2)

    def test_get_instance(self):
        """Test get_instance class method."""
        StorageManager._instance = None
        storage = StorageManager.get_instance(self.db_path)
        self.assertIsNotNone(storage)

    def test_connect(self):
        """Test database connection."""
        result = self.storage.connect()
        self.assertTrue(result)
        self.assertTrue(self.storage.is_connected())

    def test_connect_twice(self):
        """Test that connecting twice doesn't fail."""
        self.storage.connect()
        result = self.storage.connect()
        self.assertTrue(result)

    def test_disconnect(self):
        """Test database disconnection."""
        self.storage.connect()
        result = self.storage.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.storage.is_connected())

    def test_is_connected_initially_false(self):
        """Test that is_connected is False initially."""
        self.assertFalse(self.storage.is_connected())

    def test_execute_query_without_connection(self):
        """Test that query without connection raises DatabaseError."""
        with self.assertRaises(DatabaseError):
            self.storage.execute_query("SELECT * FROM logs")

    def test_execute_update_without_connection(self):
        """Test that update without connection raises DatabaseError."""
        with self.assertRaises(DatabaseError):
            self.storage.execute_update("UPDATE logs SET severity='INFO'")

    def test_execute_insert_without_connection(self):
        """Test that insert without connection raises DatabaseError."""
        with self.assertRaises(DatabaseError):
            self.storage.execute_insert("INSERT INTO logs (event_type) VALUES ('TEST')")

    def test_save_and_get_login_interface(self):
        """Test saving and retrieving login interface."""
        self.storage.connect()

        login_if = LoginInterface(
            "testuser", "password123", "web", AccessLevel.USER_ACCESS
        )
        login_data = login_if.to_dict()

        # Save
        result = self.storage.save_login_interface(login_data)
        self.assertTrue(result)

        # Retrieve
        retrieved = self.storage.get_login_interface("testuser", "web")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["username"], "testuser")
        self.assertEqual(retrieved["interface"], "web")

    def test_get_nonexistent_login_interface(self):
        """Test retrieving non-existent login interface returns None."""
        self.storage.connect()

        result = self.storage.get_login_interface("nonexistent", "web")
        self.assertIsNone(result)

    def test_update_login_interface(self):
        """Test updating existing login interface."""
        self.storage.connect()

        # Create initial login
        login_if = LoginInterface(
            "testuser", "password123", "web", AccessLevel.USER_ACCESS
        )
        self.storage.save_login_interface(login_if.to_dict())

        # Update login attempts
        login_if.increment_attempts()
        self.storage.save_login_interface(login_if.to_dict())

        # Retrieve and verify
        retrieved = self.storage.get_login_interface("testuser", "web")
        self.assertEqual(retrieved["login_attempts"], 1)

    def test_save_and_get_system_settings(self):
        """Test saving and retrieving system settings."""
        self.storage.connect()

        settings = {
            "monitoring_service_phone": "911",
            "homeowner_phone": "010-1234-5678",
            "system_lock_time": "60",
            "alarm_delay_time": "30",
        }

        # Save
        result = self.storage.save_system_settings(settings)
        self.assertTrue(result)

        # Retrieve
        retrieved = self.storage.get_system_settings()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["monitoring_service_phone"], "911")
        self.assertEqual(retrieved["homeowner_phone"], "010-1234-5678")

    def test_get_system_settings_empty(self):
        """Test retrieving system settings when none exist."""
        self.storage.connect()

        result = self.storage.get_system_settings()
        self.assertIsNone(result)

    def test_save_and_get_safehome_modes(self):
        """Test saving and retrieving SafeHome modes."""
        self.storage.connect()

        mode = {
            "mode_id": 1,
            "mode_name": "HOME",
            "sensor_ids": [1, 2, 3],
            "is_active": True,
            "description": "Home mode",
        }

        # Save
        result = self.storage.save_safehome_mode(mode)
        self.assertTrue(result)

        # Retrieve
        modes = self.storage.get_safehome_modes()
        self.assertEqual(len(modes), 1)
        self.assertEqual(modes[0]["mode_id"], 1)
        self.assertEqual(modes[0]["mode_name"], "HOME")

    def test_get_safehome_modes_empty(self):
        """Test retrieving modes when none exist."""
        self.storage.connect()

        modes = self.storage.get_safehome_modes()
        self.assertEqual(modes, [])

    def test_save_and_get_safety_zones(self):
        """Test saving and retrieving safety zones."""
        self.storage.connect()

        zone = {
            "zone_id": None,  # Auto-increment
            "zone_name": "First Floor",
            "sensor_ids": [10, 20, 30],
            "is_armed": True,
            "description": "Main floor sensors",
        }

        # Save
        result = self.storage.save_safety_zone(zone)
        self.assertTrue(result)

        # Retrieve
        zones = self.storage.get_safety_zones()
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0]["zone_name"], "First Floor")

    def test_update_safety_zone(self):
        """Test updating existing safety zone."""
        self.storage.connect()

        # Create zone
        zone = {
            "zone_id": None,
            "zone_name": "Bedroom",
            "sensor_ids": [1, 2],
            "is_armed": False,
        }
        self.storage.save_safety_zone(zone)

        # Get zone ID
        zones = self.storage.get_safety_zones()
        zone_id = zones[0]["zone_id"]

        # Update zone
        updated_zone = {
            "zone_id": zone_id,
            "zone_name": "Master Bedroom",
            "sensor_ids": [1, 2, 3],
            "is_armed": True,
        }
        self.storage.save_safety_zone(updated_zone)

        # Verify
        zones = self.storage.get_safety_zones()
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0]["zone_name"], "Master Bedroom")
        self.assertTrue(zones[0]["is_armed"])

    def test_delete_safety_zone(self):
        """Test deleting safety zone."""
        self.storage.connect()

        # Create zone
        zone = {
            "zone_id": None,
            "zone_name": "Garage",
            "sensor_ids": [5],
        }
        self.storage.save_safety_zone(zone)

        # Get zone ID
        zones = self.storage.get_safety_zones()
        zone_id = zones[0]["zone_id"]

        # Delete
        result = self.storage.delete_safety_zone(zone_id)
        self.assertTrue(result)

        # Verify deletion
        zones = self.storage.get_safety_zones()
        self.assertEqual(len(zones), 0)

    def test_delete_nonexistent_zone(self):
        """Test deleting non-existent zone returns False."""
        self.storage.connect()

        result = self.storage.delete_safety_zone(999)
        self.assertFalse(result)

    def test_save_and_get_logs(self):
        """Test saving and retrieving logs."""
        self.storage.connect()

        log = {
            "timestamp": "2024-01-15T10:30:00",
            "event_type": "SYSTEM",
            "description": "System started",
            "severity": "INFO",
            "user": None,
        }

        # Save
        result = self.storage.save_log(log)
        self.assertTrue(result)

        # Retrieve
        logs = self.storage.get_logs(limit=10)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["event_type"], "SYSTEM")

    def test_get_logs_with_limit(self):
        """Test retrieving logs with limit."""
        self.storage.connect()

        # Create multiple logs
        for i in range(5):
            log = {
                "event_type": "TEST",
                "description": f"Log {i}",
                "severity": "INFO",
            }
            self.storage.save_log(log)

        # Retrieve with limit
        logs = self.storage.get_logs(limit=3)
        self.assertEqual(len(logs), 3)

    def test_execute_query_returns_list(self):
        """Test that execute_query returns list of dicts."""
        self.storage.connect()

        # Insert test data
        self.storage.save_log(
            {
                "event_type": "TEST",
                "description": "Test log",
            }
        )

        # Query
        results = self.storage.execute_query(
            "SELECT * FROM logs WHERE event_type = ?", ("TEST",)
        )

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], dict)

    def test_execute_update_returns_row_count(self):
        """Test that execute_update returns affected row count."""
        self.storage.connect()

        # Insert test data (use 8+ char password with digit)
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)
        self.storage.save_login_interface(login_if.to_dict())

        # Update
        count = self.storage.execute_update(
            "UPDATE login_interfaces SET login_attempts = ? WHERE username = ?",
            (5, "user"),
        )

        self.assertGreater(count, 0)

    def test_execute_insert_returns_last_row_id(self):
        """Test that execute_insert returns last inserted row ID."""
        self.storage.connect()

        row_id = self.storage.execute_insert(
            "INSERT INTO logs (timestamp, event_type, description) VALUES (?, ?, ?)",
            ("2024-01-01T00:00:00", "TEST", "Test description"),
        )

        self.assertIsNotNone(row_id)
        self.assertGreater(row_id, 0)

    def test_schema_created_on_connect(self):
        """Test that database schema is created on connection."""
        self.storage.connect()

        # Verify tables exist by querying them
        tables = self.storage.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        table_names = [t["name"] for t in tables]
        self.assertIn("login_interfaces", table_names)
        self.assertIn("system_settings", table_names)
        self.assertIn("safehome_modes", table_names)
        self.assertIn("safety_zones", table_names)
        self.assertIn("logs", table_names)


if __name__ == "__main__":
    unittest.main()
