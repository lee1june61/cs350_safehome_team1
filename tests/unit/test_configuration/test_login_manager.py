"""Unit tests for LoginManager class."""

import unittest
import os
import tempfile
from src.configuration.login_manager import LoginManager
from src.configuration.storage_manager import StorageManager
from src.configuration.login_interface import LoginInterface, AccessLevel
from src.configuration.exceptions import AuthenticationError


class TestLoginManager(unittest.TestCase):
    """Test LoginManager authentication management."""

    def setUp(self):
        """Set up test fixtures with real database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Reset singleton
        StorageManager._instance = None

        self.storage = StorageManager({"db_path": self.db_path})
        self.storage.connect()

        self.login_manager = LoginManager(self.storage)

        # Create test user
        self.test_user = LoginInterface(
            "testuser", "password123", "web", AccessLevel.USER_ACCESS
        )
        self.storage.save_login_interface(self.test_user.to_dict())

    def tearDown(self):
        """Clean up test database."""
        if self.storage.is_connected():
            self.storage.disconnect()

        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

        StorageManager._instance = None

    def test_login_manager_creation(self):
        """Test LoginManager instantiation."""
        self.assertIsNotNone(self.login_manager)

    def test_login_success(self):
        """Test successful login."""
        access_level = self.login_manager.login("testuser", "password123", "web")

        self.assertIsNotNone(access_level)
        self.assertEqual(access_level, AccessLevel.USER_ACCESS)

    def test_login_wrong_password(self):
        """Test login with incorrect password."""
        access_level = self.login_manager.login("testuser", "wrongpassword", "web")

        self.assertIsNone(access_level)

    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        access_level = self.login_manager.login("nonexistent", "password123", "web")

        self.assertIsNone(access_level)

    def test_login_wrong_interface(self):
        """Test login with wrong interface."""
        access_level = self.login_manager.login(
            "testuser", "password123", "control_panel"
        )

        self.assertIsNone(access_level)

    def test_login_increments_attempts_on_failure(self):
        """Test that failed login increments login attempts."""
        # First failed attempt
        self.login_manager.login("testuser", "wrongpassword", "web")

        # Check attempts increased
        data = self.storage.get_login_interface("testuser", "web")
        self.assertEqual(data["login_attempts"], 1)

    def test_login_resets_attempts_on_success(self):
        """Test that successful login resets login attempts."""
        # Fail once
        self.login_manager.login("testuser", "wrongpassword", "web")

        # Succeed
        self.login_manager.login("testuser", "password123", "web")

        # Check attempts reset
        data = self.storage.get_login_interface("testuser", "web")
        self.assertEqual(data["login_attempts"], 0)

    def test_login_locks_account_after_max_attempts(self):
        """Test that account is locked after max failed attempts."""
        # Fail 3 times (default max)
        for _ in range(3):
            self.login_manager.login("testuser", "wrongpassword", "web")

        # Check account is locked
        data = self.storage.get_login_interface("testuser", "web")
        self.assertTrue(data["is_locked"])

    def test_login_locked_account_returns_none(self):
        """Test that login on locked account returns None."""
        # Lock account
        for _ in range(3):
            self.login_manager.login("testuser", "wrongpassword", "web")

        # Try to login with correct password
        access_level = self.login_manager.login("testuser", "password123", "web")

        self.assertIsNone(access_level)

    def test_login_without_lockout_enforcement(self):
        """Test login when lockout enforcement is disabled."""
        manager = LoginManager(self.storage, enforce_lockout=False)

        # Lock the account
        for _ in range(3):
            manager.login("testuser", "wrongpassword", "web")

        # Should still be able to login with correct password
        access_level = manager.login("testuser", "password123", "web")

        self.assertIsNotNone(access_level)

    def test_logout(self):
        """Test logout functionality."""
        result = self.login_manager.logout()
        self.assertTrue(result)

    def test_change_password_success(self):
        """Test successful password change."""
        result = self.login_manager.change_password(
            "testuser", "password123", "newpassword456", "web"
        )

        self.assertTrue(result)

        # Verify old password no longer works
        access_level = self.login_manager.login("testuser", "password123", "web")
        self.assertIsNone(access_level)

        # Verify new password works
        access_level = self.login_manager.login("testuser", "newpassword456", "web")
        self.assertIsNotNone(access_level)

    def test_change_password_wrong_old_password(self):
        """Test password change with incorrect old password."""
        with self.assertRaises(AuthenticationError):
            self.login_manager.change_password(
                "testuser", "wrongoldpassword", "newpassword456", "web"
            )

    def test_change_password_nonexistent_user(self):
        """Test password change for non-existent user."""
        with self.assertRaises(AuthenticationError):
            self.login_manager.change_password(
                "nonexistent", "password123", "newpassword456", "web"
            )

    def test_validate_credentials_valid(self):
        """Test credential validation with valid credentials."""
        result = self.login_manager.validate_credentials(
            "testuser", "password123", "web"
        )

        self.assertTrue(result)

    def test_validate_credentials_invalid(self):
        """Test credential validation with invalid credentials."""
        result = self.login_manager.validate_credentials(
            "testuser", "wrongpassword", "web"
        )

        self.assertFalse(result)

    def test_validate_credentials_nonexistent_user(self):
        """Test credential validation for non-existent user."""
        result = self.login_manager.validate_credentials(
            "nonexistent", "password123", "web"
        )

        self.assertFalse(result)

    def test_get_access_level(self):
        """Test getting user access level."""
        access_level = self.login_manager.get_access_level("testuser", "web")

        self.assertEqual(access_level, AccessLevel.USER_ACCESS)

    def test_get_access_level_nonexistent_user(self):
        """Test getting access level for non-existent user."""
        access_level = self.login_manager.get_access_level("nonexistent", "web")

        self.assertIsNone(access_level)

    def test_is_account_locked(self):
        """Test checking if account is locked."""
        # Initially not locked
        self.assertFalse(self.login_manager.is_account_locked("testuser", "web"))

        # Lock account
        for _ in range(3):
            self.login_manager.login("testuser", "wrongpassword", "web")

        # Now should be locked
        self.assertTrue(self.login_manager.is_account_locked("testuser", "web"))

    def test_is_account_locked_nonexistent_user(self):
        """Test checking lock status for non-existent user."""
        result = self.login_manager.is_account_locked("nonexistent", "web")

        self.assertFalse(result)

    def test_configure_lockout_max_attempts(self):
        """Test configuring maximum login attempts."""
        self.login_manager.configure_lockout(max_attempts=5)

        # Fail 4 times - should not lock
        for _ in range(4):
            self.login_manager.login("testuser", "wrongpassword", "web")

        self.assertFalse(self.login_manager.is_account_locked("testuser", "web"))

        # 5th failure should lock
        self.login_manager.login("testuser", "wrongpassword", "web")
        self.assertTrue(self.login_manager.is_account_locked("testuser", "web"))

    def test_configure_lockout_disable_enforcement(self):
        """Test disabling lockout enforcement."""
        self.login_manager.configure_lockout(enforce_lockout=False)

        # Fail many times
        for _ in range(10):
            self.login_manager.login("testuser", "wrongpassword", "web")

        # Account should not be locked
        access_level = self.login_manager.login("testuser", "password123", "web")
        self.assertIsNotNone(access_level)

    def test_multiple_users_different_interfaces(self):
        """Test managing multiple users on different interfaces."""
        # Create another user on different interface
        user2 = LoginInterface(
            "testuser", "password456", "control_panel", AccessLevel.MASTER_ACCESS
        )
        self.storage.save_login_interface(user2.to_dict())

        # Login both
        access1 = self.login_manager.login("testuser", "password123", "web")
        access2 = self.login_manager.login("testuser", "password456", "control_panel")

        self.assertEqual(access1, AccessLevel.USER_ACCESS)
        self.assertEqual(access2, AccessLevel.MASTER_ACCESS)

    def test_master_user_access(self):
        """Test master user login."""
        master = LoginInterface(
            "admin", "masterpass123", "web", AccessLevel.MASTER_ACCESS
        )
        self.storage.save_login_interface(master.to_dict())

        access_level = self.login_manager.login("admin", "masterpass123", "web")

        self.assertEqual(access_level, AccessLevel.MASTER_ACCESS)

    def test_guest_user_access(self):
        """Test guest user login."""
        guest = LoginInterface("guest", "guestpass123", "web", AccessLevel.GUEST_ACCESS)
        self.storage.save_login_interface(guest.to_dict())

        access_level = self.login_manager.login("guest", "guestpass123", "web")

        self.assertEqual(access_level, AccessLevel.GUEST_ACCESS)

    def test_login_updates_last_login_timestamp(self):
        """Test that successful login updates last_login timestamp."""
        # Login
        self.login_manager.login("testuser", "password123", "web")

        # Check last_login is set
        data = self.storage.get_login_interface("testuser", "web")
        self.assertIsNotNone(data["last_login"])


if __name__ == "__main__":
    unittest.main()
