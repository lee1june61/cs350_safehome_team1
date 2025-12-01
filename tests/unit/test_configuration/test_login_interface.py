"""Unit tests for LoginInterface class."""

import unittest
from datetime import datetime
from src.configuration.login_interface import LoginInterface, AccessLevel
from src.configuration.exceptions import ValidationError


class TestLoginInterface(unittest.TestCase):
    """Test LoginInterface authentication data model."""

    def test_login_interface_creation(self):
        """Test basic LoginInterface instantiation."""
        login_if = LoginInterface(
            "testuser", "password123", "control_panel", AccessLevel.USER_ACCESS
        )

        self.assertEqual(login_if.username, "testuser")
        self.assertEqual(login_if.interface, "control_panel")
        self.assertEqual(login_if.access_level, AccessLevel.USER_ACCESS)
        self.assertEqual(login_if.login_attempts, 0)
        self.assertFalse(login_if.is_locked)
        self.assertIsNone(login_if.last_login)

    def test_password_hashing_on_creation(self):
        """Test that password is hashed during initialization."""
        login_if = LoginInterface(
            "user", "password123", "web", AccessLevel.GUEST_ACCESS
        )

        # Password should be hashed, not stored in plaintext
        self.assertNotEqual(login_if.password_hash, "password123")
        self.assertTrue(len(login_if.password_hash) > 0)

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)
        self.assertTrue(login_if.verify_password("password123"))

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)
        self.assertFalse(login_if.verify_password("wrongpassword"))

    def test_set_password(self):
        """Test changing password."""
        login_if = LoginInterface(
            "user", "oldpassword123", "web", AccessLevel.USER_ACCESS
        )

        # Change password
        result = login_if.set_password("newpassword456")
        self.assertTrue(result)

        # Old password should not work
        self.assertFalse(login_if.verify_password("oldpassword123"))

        # New password should work
        self.assertTrue(login_if.verify_password("newpassword456"))

    def test_set_password_validation_too_short(self):
        """Test that short passwords are rejected."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        with self.assertRaises(ValidationError):
            login_if.set_password("short")

    def test_set_password_validation_no_digit(self):
        """Test that passwords without digits are rejected when required."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)
        login_if.password_requires_digit = True

        with self.assertRaises(ValidationError):
            login_if.set_password("passwordonly")

    def test_increment_attempts(self):
        """Test incrementing login attempts."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        self.assertEqual(login_if.login_attempts, 0)
        count = login_if.increment_attempts()
        self.assertEqual(count, 1)
        self.assertEqual(login_if.login_attempts, 1)

        count = login_if.increment_attempts()
        self.assertEqual(count, 2)

    def test_reset_attempts(self):
        """Test resetting login attempts."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        login_if.increment_attempts()
        login_if.increment_attempts()
        self.assertEqual(login_if.login_attempts, 2)

        login_if.reset_attempts()
        self.assertEqual(login_if.login_attempts, 0)

    def test_lock_account(self):
        """Test locking user account."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        self.assertFalse(login_if.is_locked)
        login_if.lock_account()
        self.assertTrue(login_if.is_locked)

    def test_unlock_account(self):
        """Test unlocking user account."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        login_if.lock_account()
        login_if.increment_attempts()
        login_if.increment_attempts()

        self.assertTrue(login_if.is_locked)
        self.assertEqual(login_if.login_attempts, 2)

        login_if.unlock_account()
        self.assertFalse(login_if.is_locked)
        self.assertEqual(login_if.login_attempts, 0)

    def test_to_dict(self):
        """Test serialization to dictionary."""
        login_if = LoginInterface(
            "user", "password123", "web", AccessLevel.MASTER_ACCESS
        )

        data = login_if.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["username"], "user")
        self.assertEqual(data["interface"], "web")
        self.assertEqual(data["access_level"], AccessLevel.MASTER_ACCESS)
        self.assertIn("password_hash", data)
        self.assertIn("created_at", data)

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        login_if = LoginInterface(
            "user", "password123", "control_panel", AccessLevel.USER_ACCESS
        )
        data = login_if.to_dict()

        # Create new instance from dict
        restored = LoginInterface.from_dict(data)

        self.assertEqual(restored.username, login_if.username)
        self.assertEqual(restored.interface, login_if.interface)
        self.assertEqual(restored.access_level, login_if.access_level)
        self.assertEqual(restored.password_hash, login_if.password_hash)
        self.assertTrue(restored.verify_password("password123"))

    def test_access_levels(self):
        """Test different access levels."""
        master = LoginInterface(
            "master", "password123", "web", AccessLevel.MASTER_ACCESS
        )
        user = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)
        guest = LoginInterface("guest", "password123", "web", AccessLevel.GUEST_ACCESS)

        self.assertEqual(master.access_level, 0x01)
        self.assertEqual(user.access_level, 0x02)
        self.assertEqual(guest.access_level, 0x03)

    def test_created_at_timestamp(self):
        """Test that created_at timestamp is set."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        self.assertIsInstance(login_if.created_at, datetime)
        self.assertLessEqual(
            (datetime.utcnow() - login_if.created_at).total_seconds(), 1
        )

    def test_password_policy_configuration(self):
        """Test password policy configuration attributes."""
        login_if = LoginInterface("user", "password123", "web", AccessLevel.USER_ACCESS)

        self.assertEqual(login_if.password_min_length, 8)
        self.assertTrue(login_if.password_requires_digit)
        self.assertFalse(login_if.password_requires_special)

        # Change policy
        login_if.password_min_length = 12
        login_if.password_requires_special = True

        # Now short password without special char should fail
        with self.assertRaises(ValidationError):
            login_if.set_password("password123")


if __name__ == "__main__":
    unittest.main()
