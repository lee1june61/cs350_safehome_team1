"""Unit tests for custom exception classes in the configuration module."""

import unittest
from src.configuration.exceptions import (
    ConfigurationError,
    DatabaseError,
    AuthenticationError,
    ValidationError,
)


class TestExceptions(unittest.TestCase):
    """Test custom exception classes."""

    def test_configuration_error_creation(self):
        """Test that ConfigurationError can be instantiated with a message."""
        error = ConfigurationError("Configuration failed")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Configuration failed")

    def test_database_error_creation(self):
        """Test that DatabaseError can be instantiated with a message."""
        error = DatabaseError("Database connection failed")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Database connection failed")

    def test_authentication_error_creation(self):
        """Test that AuthenticationError can be instantiated with a message."""
        error = AuthenticationError("Invalid credentials")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Invalid credentials")

    def test_validation_error_creation(self):
        """Test that ValidationError can be instantiated with a message."""
        error = ValidationError("Invalid input")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Invalid input")

    def test_exceptions_are_raisable(self):
        """Test that all custom exceptions can be raised and caught."""
        with self.assertRaises(ConfigurationError):
            raise ConfigurationError("Test")

        with self.assertRaises(DatabaseError):
            raise DatabaseError("Test")

        with self.assertRaises(AuthenticationError):
            raise AuthenticationError("Test")

        with self.assertRaises(ValidationError):
            raise ValidationError("Test")

    def test_exceptions_inherit_from_exception(self):
        """Test that all custom exceptions inherit from Exception."""
        self.assertTrue(issubclass(ConfigurationError, Exception))
        self.assertTrue(issubclass(DatabaseError, Exception))
        self.assertTrue(issubclass(AuthenticationError, Exception))
        self.assertTrue(issubclass(ValidationError, Exception))


if __name__ == "__main__":
    unittest.main()
