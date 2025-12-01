"""Unit tests for SystemSettings class."""

import unittest
from unittest.mock import Mock, MagicMock
from src.configuration.system_settings import SystemSettings
from src.configuration.exceptions import ValidationError


class TestSystemSettings(unittest.TestCase):
    """Test SystemSettings configuration management."""

    def test_settings_creation_with_defaults(self):
        """Test creating settings with default values."""
        settings = SystemSettings()

        self.assertEqual(settings.monitoring_service_phone, "010-1234-1234")
        self.assertEqual(settings.homeowner_phone, "")
        self.assertEqual(settings.system_lock_time, 60)
        self.assertEqual(settings.alarm_delay_time, 30)
        self.assertEqual(settings.max_login_attempts, 3)
        self.assertEqual(settings.session_timeout, 30)

    def test_settings_creation_with_custom_values(self):
        """Test creating settings with custom values."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="010-5555-6666",
            system_lock_time=120,
            alarm_delay_time=45,
            max_login_attempts=5,
            session_timeout=60,
        )

        self.assertEqual(settings.monitoring_service_phone, "911")
        self.assertEqual(settings.homeowner_phone, "010-5555-6666")
        self.assertEqual(settings.system_lock_time, 120)
        self.assertEqual(settings.alarm_delay_time, 45)
        self.assertEqual(settings.max_login_attempts, 5)
        self.assertEqual(settings.session_timeout, 60)

    def test_validate_phone_number_valid(self):
        """Test phone number validation with valid numbers."""
        settings = SystemSettings()

        # Valid phone numbers
        self.assertTrue(settings.validate_phone_number("010-1234-5678"))
        self.assertTrue(settings.validate_phone_number("01012345678"))
        self.assertTrue(settings.validate_phone_number("+82-10-1234-5678"))
        self.assertTrue(settings.validate_phone_number(""))  # Empty is valid

    def test_validate_phone_number_emergency(self):
        """Test emergency number validation."""
        settings = SystemSettings()

        # Emergency numbers should pass with allow_emergency=True
        self.assertTrue(settings.validate_phone_number("911", allow_emergency=True))
        self.assertTrue(settings.validate_phone_number("112", allow_emergency=True))
        self.assertTrue(settings.validate_phone_number("119", allow_emergency=True))

    def test_validate_phone_number_invalid(self):
        """Test phone number validation with invalid numbers."""
        settings = SystemSettings()

        # Too short
        self.assertFalse(settings.validate_phone_number("123"))

        # Too long
        self.assertFalse(settings.validate_phone_number("1234567890123456"))

        # Non-digit characters only
        self.assertFalse(settings.validate_phone_number("---"))

    def test_validate_settings_valid(self):
        """Test validation of valid settings."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="010-1234-5678",
            system_lock_time=60,
            alarm_delay_time=30,
        )

        self.assertTrue(settings.validate_settings())

    def test_validate_settings_invalid_monitor_phone(self):
        """Test validation fails for invalid monitoring phone."""
        settings = SystemSettings(
            monitoring_service_phone="123",  # Too short
        )

        self.assertFalse(settings.validate_settings())

    def test_validate_settings_invalid_homeowner_phone(self):
        """Test validation fails for invalid homeowner phone."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="abc",  # Invalid
        )

        self.assertFalse(settings.validate_settings())

    def test_validate_settings_system_lock_time_too_short(self):
        """Test validation fails for system lock time below minimum."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            system_lock_time=20,  # Less than 30
        )

        self.assertFalse(settings.validate_settings())

    def test_validate_settings_system_lock_time_too_long(self):
        """Test validation fails for system lock time above maximum."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            system_lock_time=400,  # More than 300
        )

        self.assertFalse(settings.validate_settings())

    def test_validate_settings_alarm_delay_too_short(self):
        """Test validation fails for alarm delay below minimum."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            alarm_delay_time=3,  # Less than 5
        )

        self.assertFalse(settings.validate_settings())

    def test_validate_settings_alarm_delay_too_long(self):
        """Test validation fails for alarm delay above maximum."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            alarm_delay_time=70,  # More than 60
        )

        self.assertFalse(settings.validate_settings())

    def test_save_to_database_valid(self):
        """Test saving valid settings to database."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="010-1234-5678",
        )

        mock_storage = Mock()
        mock_storage.save_system_settings = Mock(return_value=True)

        result = settings.save_to_database(mock_storage)

        self.assertTrue(result)
        mock_storage.save_system_settings.assert_called_once()

    def test_save_to_database_invalid(self):
        """Test that saving invalid settings raises ValidationError."""
        settings = SystemSettings(
            monitoring_service_phone="123",  # Invalid
        )

        mock_storage = Mock()

        with self.assertRaises(ValidationError):
            settings.save_to_database(mock_storage)

    def test_load_from_database_success(self):
        """Test loading settings from database."""
        settings = SystemSettings()

        mock_storage = Mock()
        mock_storage.get_system_settings = Mock(
            return_value={
                "monitoring_service_phone": "119",
                "homeowner_phone": "010-9999-8888",
                "system_lock_time": "90",
                "alarm_delay_time": "25",
                "max_login_attempts": "5",
                "session_timeout": "45",
            }
        )

        result = settings.load_from_database(mock_storage)

        self.assertTrue(result)
        self.assertEqual(settings.monitoring_service_phone, "119")
        self.assertEqual(settings.homeowner_phone, "010-9999-8888")
        self.assertEqual(settings.system_lock_time, 90)
        self.assertEqual(settings.alarm_delay_time, 25)
        self.assertEqual(settings.max_login_attempts, 5)
        self.assertEqual(settings.session_timeout, 45)

    def test_load_from_database_no_data(self):
        """Test loading settings when no data exists."""
        settings = SystemSettings()

        mock_storage = Mock()
        mock_storage.get_system_settings = Mock(return_value=None)

        result = settings.load_from_database(mock_storage)

        self.assertFalse(result)

    def test_load_from_database_partial_data(self):
        """Test loading settings with partial data uses defaults."""
        settings = SystemSettings()

        mock_storage = Mock()
        mock_storage.get_system_settings = Mock(
            return_value={
                "monitoring_service_phone": "112",
            }
        )

        result = settings.load_from_database(mock_storage)

        self.assertTrue(result)
        self.assertEqual(settings.monitoring_service_phone, "112")
        # Other fields should have defaults
        self.assertEqual(settings.system_lock_time, 60)
        self.assertEqual(settings.alarm_delay_time, 30)

    def test_to_dict(self):
        """Test serialization to dictionary."""
        settings = SystemSettings(
            monitoring_service_phone="119",
            homeowner_phone="010-1111-2222",
            system_lock_time=75,
            alarm_delay_time=40,
        )

        data = settings.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["monitoring_service_phone"], "119")
        self.assertEqual(data["homeowner_phone"], "010-1111-2222")
        self.assertEqual(data["system_lock_time"], 75)
        self.assertEqual(data["alarm_delay_time"], 40)

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "monitoring_service_phone": "112",
            "homeowner_phone": "010-3333-4444",
            "system_lock_time": 100,
            "alarm_delay_time": 50,
            "max_login_attempts": 4,
            "session_timeout": 20,
        }

        settings = SystemSettings.from_dict(data)

        self.assertEqual(settings.monitoring_service_phone, "112")
        self.assertEqual(settings.homeowner_phone, "010-3333-4444")
        self.assertEqual(settings.system_lock_time, 100)
        self.assertEqual(settings.alarm_delay_time, 50)
        self.assertEqual(settings.max_login_attempts, 4)
        self.assertEqual(settings.session_timeout, 20)

    def test_from_dict_missing_fields(self):
        """Test deserialization with missing fields uses defaults."""
        data = {
            "monitoring_service_phone": "911",
        }

        settings = SystemSettings.from_dict(data)

        self.assertEqual(settings.monitoring_service_phone, "911")
        self.assertEqual(settings.homeowner_phone, "")
        self.assertEqual(settings.system_lock_time, 60)

    def test_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        original = SystemSettings(
            monitoring_service_phone="119",
            homeowner_phone="010-5555-6666",
            system_lock_time=120,
            alarm_delay_time=35,
            max_login_attempts=4,
            session_timeout=40,
        )

        data = original.to_dict()
        restored = SystemSettings.from_dict(data)

        self.assertEqual(
            restored.monitoring_service_phone, original.monitoring_service_phone
        )
        self.assertEqual(restored.homeowner_phone, original.homeowner_phone)
        self.assertEqual(restored.system_lock_time, original.system_lock_time)
        self.assertEqual(restored.alarm_delay_time, original.alarm_delay_time)
        self.assertEqual(restored.max_login_attempts, original.max_login_attempts)
        self.assertEqual(restored.session_timeout, original.session_timeout)

    def test_normalize_phone(self):
        """Test phone number normalization."""
        settings = SystemSettings()

        self.assertEqual(settings._normalize_phone("010-1234-5678"), "01012345678")
        self.assertEqual(settings._normalize_phone("+82-10-1234-5678"), "821012345678")
        self.assertEqual(settings._normalize_phone("(010) 1234-5678"), "01012345678")
        self.assertEqual(settings._normalize_phone(""), "")

    def test_valid_time_ranges(self):
        """Test valid time range boundaries."""
        # Valid system lock times
        settings = SystemSettings(system_lock_time=30)
        self.assertTrue(settings.validate_settings())

        settings = SystemSettings(system_lock_time=300)
        self.assertTrue(settings.validate_settings())

        # Valid alarm delay times
        settings = SystemSettings(alarm_delay_time=5)
        self.assertTrue(settings.validate_settings())

        settings = SystemSettings(alarm_delay_time=60)
        self.assertTrue(settings.validate_settings())


if __name__ == "__main__":
    unittest.main()
