"""Unit tests for Log class."""

import unittest
from datetime import datetime, timedelta
from src.configuration.log import Log


class TestLog(unittest.TestCase):
    """Test Log event entry class."""

    def test_log_creation_basic(self):
        """Test basic log creation with required fields."""
        log = Log(event_type="SYSTEM", description="System started")

        self.assertEqual(log.event_type, "SYSTEM")
        self.assertEqual(log.description, "System started")
        self.assertEqual(log.severity, "INFO")
        self.assertIsNone(log.log_id)
        self.assertIsInstance(log.timestamp, datetime)

    def test_log_creation_with_severity(self):
        """Test log creation with custom severity."""
        log = Log(
            event_type="ERROR",
            description="Database connection failed",
            severity="CRITICAL",
        )

        self.assertEqual(log.severity, "CRITICAL")

    def test_log_creation_with_all_fields(self):
        """Test log creation with all optional fields."""
        timestamp = datetime.utcnow()
        log = Log(
            event_type="LOGIN",
            description="User logged in",
            severity="INFO",
            log_id=123,
            timestamp=timestamp,
            user="testuser",
        )

        self.assertEqual(log.log_id, 123)
        self.assertEqual(log.timestamp, timestamp)
        self.assertEqual(log.user, "testuser")

    def test_log_timestamp_default(self):
        """Test that timestamp is set automatically if not provided."""
        before = datetime.utcnow()
        log = Log(event_type="SYSTEM", description="Test event")
        after = datetime.utcnow()

        self.assertIsInstance(log.timestamp, datetime)
        self.assertGreaterEqual(log.timestamp, before)
        self.assertLessEqual(log.timestamp, after)

    def test_log_to_dict(self):
        """Test serialization to dictionary."""
        log = Log(
            event_type="INTRUSION",
            description="Motion detected",
            severity="WARNING",
            user="admin",
        )

        data = log.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["event_type"], "INTRUSION")
        self.assertEqual(data["description"], "Motion detected")
        self.assertEqual(data["severity"], "WARNING")
        self.assertEqual(data["user"], "admin")
        self.assertIn("timestamp", data)

    def test_log_to_dict_with_timestamp(self):
        """Test that timestamp is serialized to ISO format."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        log = Log(
            event_type="SYSTEM",
            description="Test",
            timestamp=timestamp,
        )

        data = log.to_dict()
        self.assertEqual(data["timestamp"], timestamp.isoformat())

    def test_log_from_dict(self):
        """Test deserialization from dictionary."""
        original = Log(
            event_type="LOGIN",
            description="User login attempt",
            severity="INFO",
            user="testuser",
        )
        data = original.to_dict()

        restored = Log.from_dict(data)

        self.assertEqual(restored.event_type, original.event_type)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.severity, original.severity)
        self.assertEqual(restored.user, original.user)

    def test_log_from_dict_with_timestamp_string(self):
        """Test deserialization with ISO timestamp string."""
        data = {
            "event_type": "SYSTEM",
            "description": "Test event",
            "severity": "INFO",
            "timestamp": "2024-01-15T10:30:00",
        }

        log = Log.from_dict(data)

        self.assertIsInstance(log.timestamp, datetime)
        self.assertEqual(log.timestamp.year, 2024)
        self.assertEqual(log.timestamp.month, 1)
        self.assertEqual(log.timestamp.day, 15)

    def test_log_from_dict_with_datetime_object(self):
        """Test deserialization with datetime object."""
        timestamp = datetime(2024, 3, 20, 15, 45, 30)
        data = {
            "event_type": "CONFIGURATION",
            "description": "Settings updated",
            "timestamp": timestamp,
        }

        log = Log.from_dict(data)
        self.assertEqual(log.timestamp, timestamp)

    def test_log_from_dict_missing_timestamp(self):
        """Test deserialization when timestamp is missing."""
        data = {
            "event_type": "ERROR",
            "description": "Something went wrong",
        }

        log = Log.from_dict(data)
        # When timestamp is missing/None, Log.__init__ sets it to current time
        self.assertIsNotNone(log.timestamp)
        self.assertIsInstance(log.timestamp, datetime)

    def test_log_str_representation(self):
        """Test string representation of log."""
        log = Log(
            event_type="INTRUSION",
            description="Door sensor triggered",
            severity="WARNING",
        )

        str_repr = str(log)
        self.assertIn("WARNING", str_repr)
        self.assertIn("INTRUSION", str_repr)
        self.assertIn("Door sensor triggered", str_repr)

    def test_log_event_types(self):
        """Test various event types."""
        event_types = ["SYSTEM", "LOGIN", "INTRUSION", "CONFIGURATION", "ERROR"]

        for event_type in event_types:
            log = Log(event_type=event_type, description="Test")
            self.assertEqual(log.event_type, event_type)

    def test_log_severity_levels(self):
        """Test various severity levels."""
        severity_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]

        for severity in severity_levels:
            log = Log(event_type="SYSTEM", description="Test", severity=severity)
            self.assertEqual(log.severity, severity)

    def test_log_none_user(self):
        """Test log with no user specified."""
        log = Log(event_type="SYSTEM", description="Automatic event")
        self.assertIsNone(log.user)

    def test_log_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        original = Log(
            event_type="CONFIGURATION",
            description="Mode changed to AWAY",
            severity="INFO",
            log_id=456,
            user="admin",
        )

        # Serialize and deserialize
        data = original.to_dict()
        restored = Log.from_dict(data)

        # Check all fields match
        self.assertEqual(restored.event_type, original.event_type)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.severity, original.severity)
        self.assertEqual(restored.log_id, original.log_id)
        self.assertEqual(restored.user, original.user)


if __name__ == "__main__":
    unittest.main()
