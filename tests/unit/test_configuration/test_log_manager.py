"""Unit tests for LogManager class."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
from src.configuration.log_manager import LogManager
from src.configuration.log import Log


class TestLogManager(unittest.TestCase):
    """Test LogManager event log management."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_storage = Mock()
        self.log_manager = LogManager(self.mock_storage)

    def test_log_manager_creation(self):
        """Test LogManager instantiation."""
        self.assertIsNotNone(self.log_manager)
        self.assertEqual(self.log_manager._storage_manager, self.mock_storage)

    def test_create_log_basic(self):
        """Test creating a basic log entry."""
        log = self.log_manager.create_log(
            event_type="SYSTEM", description="System started"
        )

        self.assertIsInstance(log, Log)
        self.assertEqual(log.event_type, "SYSTEM")
        self.assertEqual(log.description, "System started")
        self.assertEqual(log.severity, "INFO")

    def test_create_log_with_severity(self):
        """Test creating log with custom severity."""
        log = self.log_manager.create_log(
            event_type="ERROR", description="Connection failed", severity="CRITICAL"
        )

        self.assertEqual(log.severity, "CRITICAL")

    def test_create_log_with_user(self):
        """Test creating log with user."""
        log = self.log_manager.create_log(
            event_type="LOGIN", description="User logged in", user="testuser"
        )

        self.assertEqual(log.user, "testuser")

    def test_save_log(self):
        """Test saving log to storage."""
        log = Log(event_type="SYSTEM", description="Test event")
        self.mock_storage.save_log = Mock(return_value=True)

        result = self.log_manager.save_log(log)

        self.assertTrue(result)
        self.mock_storage.save_log.assert_called_once()

    def test_save_log_calls_storage_with_dict(self):
        """Test that save_log passes dictionary to storage."""
        log = Log(event_type="TEST", description="Test")
        self.mock_storage.save_log = Mock(return_value=True)

        self.log_manager.save_log(log)

        # Verify dict was passed
        call_args = self.mock_storage.save_log.call_args[0][0]
        self.assertIsInstance(call_args, dict)
        self.assertEqual(call_args["event_type"], "TEST")

    def test_get_logs_default_limit(self):
        """Test retrieving logs with default limit."""
        mock_logs = [
            {"event_type": "SYSTEM", "description": "Log 1", "severity": "INFO"},
            {"event_type": "LOGIN", "description": "Log 2", "severity": "INFO"},
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_logs()

        self.assertEqual(len(logs), 2)
        self.mock_storage.get_logs.assert_called_once_with(limit=100)

    def test_get_logs_custom_limit(self):
        """Test retrieving logs with custom limit."""
        self.mock_storage.get_logs = Mock(return_value=[])

        self.log_manager.get_logs(limit=50)

        self.mock_storage.get_logs.assert_called_once_with(limit=50)

    def test_get_logs_with_event_type_filter(self):
        """Test retrieving logs filtered by event type."""
        mock_logs = [
            {"event_type": "SYSTEM", "description": "Log 1", "severity": "INFO"},
            {"event_type": "LOGIN", "description": "Log 2", "severity": "INFO"},
            {"event_type": "SYSTEM", "description": "Log 3", "severity": "INFO"},
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_logs(event_type="SYSTEM")

        self.assertEqual(len(logs), 2)
        self.assertTrue(all(log.event_type == "SYSTEM" for log in logs))

    def test_get_logs_returns_log_objects(self):
        """Test that get_logs returns Log objects."""
        mock_logs = [
            {"event_type": "SYSTEM", "description": "Test", "severity": "INFO"},
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_logs()

        self.assertIsInstance(logs[0], Log)

    def test_get_logs_by_date_range(self):
        """Test retrieving logs within date range."""
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        two_days_ago = now - timedelta(days=2)

        mock_logs = [
            {
                "event_type": "SYSTEM",
                "description": "Recent",
                "severity": "INFO",
                "timestamp": now.isoformat(),
            },
            {
                "event_type": "SYSTEM",
                "description": "Old",
                "severity": "INFO",
                "timestamp": two_days_ago.isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_logs_by_date_range(yesterday, now)

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].description, "Recent")

    def test_get_logs_by_date_range_inclusive(self):
        """Test that date range is inclusive."""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)

        mock_logs = [
            {
                "event_type": "TEST",
                "description": "On start",
                "severity": "INFO",
                "timestamp": datetime(2024, 1, 1).isoformat(),
            },
            {
                "event_type": "TEST",
                "description": "On end",
                "severity": "INFO",
                "timestamp": datetime(2024, 1, 31).isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_logs_by_date_range(start, end)

        self.assertEqual(len(logs), 2)

    def test_get_intrusion_logs(self):
        """Test retrieving intrusion-specific logs."""
        mock_logs = [
            {
                "event_type": "INTRUSION",
                "description": "Motion detected",
                "severity": "WARNING",
            },
            {"event_type": "SYSTEM", "description": "System on", "severity": "INFO"},
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        logs = self.log_manager.get_intrusion_logs()

        # Should filter to only INTRUSION events
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].event_type, "INTRUSION")

    def test_clear_old_logs(self):
        """Test clearing old logs."""
        now = datetime.utcnow()
        old_date = now - timedelta(days=40)

        mock_logs = [
            {
                "log_id": 1,
                "event_type": "SYSTEM",
                "description": "Old log",
                "severity": "INFO",
                "timestamp": old_date.isoformat(),
            },
            {
                "log_id": 2,
                "event_type": "SYSTEM",
                "description": "Recent log",
                "severity": "INFO",
                "timestamp": now.isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        count = self.log_manager.clear_old_logs(days_to_keep=30)

        # Should count logs older than 30 days
        self.assertEqual(count, 1)

    def test_clear_old_logs_custom_days(self):
        """Test clearing logs with custom retention period."""
        now = datetime.utcnow()
        ten_days_ago = now - timedelta(days=10)

        mock_logs = [
            {
                "log_id": 1,
                "event_type": "SYSTEM",
                "description": "Old",
                "severity": "INFO",
                "timestamp": ten_days_ago.isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        count = self.log_manager.clear_old_logs(days_to_keep=7)

        self.assertEqual(count, 1)

    def test_clear_old_logs_no_logs_to_delete(self):
        """Test clearing logs when none are old enough."""
        now = datetime.utcnow()

        mock_logs = [
            {
                "log_id": 1,
                "event_type": "SYSTEM",
                "description": "Recent",
                "severity": "INFO",
                "timestamp": now.isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        count = self.log_manager.clear_old_logs(days_to_keep=30)

        self.assertEqual(count, 0)

    def test_clear_old_logs_skips_logs_without_id(self):
        """Test that logs without log_id are not counted for deletion."""
        old_date = datetime.utcnow() - timedelta(days=40)

        mock_logs = [
            {
                "log_id": None,  # No ID
                "event_type": "SYSTEM",
                "description": "No ID",
                "severity": "INFO",
                "timestamp": old_date.isoformat(),
            },
        ]
        self.mock_storage.get_logs = Mock(return_value=mock_logs)

        count = self.log_manager.clear_old_logs(days_to_keep=30)

        self.assertEqual(count, 0)

    def test_create_and_save_workflow(self):
        """Test complete workflow of creating and saving a log."""
        self.mock_storage.save_log = Mock(return_value=True)

        # Create log
        log = self.log_manager.create_log(
            event_type="CONFIGURATION",
            description="Settings updated",
            severity="INFO",
            user="admin",
        )

        # Save log
        result = self.log_manager.save_log(log)

        self.assertTrue(result)
        self.mock_storage.save_log.assert_called_once()

    def test_get_logs_empty_result(self):
        """Test retrieving logs when none exist."""
        self.mock_storage.get_logs = Mock(return_value=[])

        logs = self.log_manager.get_logs()

        self.assertEqual(len(logs), 0)
        self.assertIsInstance(logs, list)

    def test_multiple_event_types(self):
        """Test creating logs with various event types."""
        event_types = ["SYSTEM", "LOGIN", "INTRUSION", "CONFIGURATION", "ERROR"]

        for event_type in event_types:
            log = self.log_manager.create_log(
                event_type=event_type, description=f"Test {event_type}"
            )
            self.assertEqual(log.event_type, event_type)

    def test_multiple_severity_levels(self):
        """Test creating logs with various severity levels."""
        severities = ["INFO", "WARNING", "ERROR", "CRITICAL"]

        for severity in severities:
            log = self.log_manager.create_log(
                event_type="TEST", description="Test", severity=severity
            )
            self.assertEqual(log.severity, severity)


if __name__ == "__main__":
    unittest.main()
