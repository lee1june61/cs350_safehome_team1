"""Unit tests for password utilities in the configuration module."""

import unittest
from src.configuration.password_utils import hash_password, validate_password_policy
from src.configuration.exceptions import ValidationError


class TestPasswordUtils(unittest.TestCase):
    """Test password hashing and validation utilities."""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        result = hash_password("password123")
        self.assertIsInstance(result, str)

    def test_hash_password_consistent(self):
        """Test that hash_password returns consistent results for same input."""
        password = "testpassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        self.assertEqual(hash1, hash2)

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes."""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        self.assertNotEqual(hash1, hash2)

    def test_hash_password_length(self):
        """Test that hash_password returns expected SHA-256 hash length."""
        result = hash_password("test")
        # SHA-256 produces 64 hex characters
        self.assertEqual(len(result), 64)

    def test_validate_password_policy_valid_password(self):
        """Test that valid passwords pass validation."""
        # Should not raise exception
        validate_password_policy("password123", min_length=8, requires_digit=True)

    def test_validate_password_policy_too_short(self):
        """Test that short passwords fail validation."""
        with self.assertRaises(ValidationError) as cm:
            validate_password_policy("short", min_length=8)
        self.assertIn("at least 8 characters", str(cm.exception))

    def test_validate_password_policy_no_digit(self):
        """Test that passwords without digits fail when required."""
        with self.assertRaises(ValidationError) as cm:
            validate_password_policy("password", requires_digit=True)
        self.assertIn("at least one digit", str(cm.exception))

    def test_validate_password_policy_no_special_char(self):
        """Test that passwords without special chars fail when required."""
        with self.assertRaises(ValidationError) as cm:
            validate_password_policy("password123", requires_special=True)
        self.assertIn("at least one special character", str(cm.exception))

    def test_validate_password_policy_all_requirements(self):
        """Test password validation with all requirements enabled."""
        # Valid password with all requirements
        validate_password_policy(
            "password123!",
            min_length=8,
            requires_digit=True,
            requires_special=True,
        )

    def test_validate_password_policy_custom_min_length(self):
        """Test password validation with custom minimum length."""
        with self.assertRaises(ValidationError):
            validate_password_policy("pass1", min_length=10)

        # Should pass with longer password
        validate_password_policy("password123", min_length=10)

    def test_validate_password_policy_no_requirements(self):
        """Test password validation with minimal requirements."""
        validate_password_policy(
            "abc",
            min_length=3,
            requires_digit=False,
            requires_special=False,
        )


if __name__ == "__main__":
    unittest.main()
