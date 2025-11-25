"""Custom exception types for the SafeHome configuration module.

All domain-specific exceptions used across the configuration and data
management subsystem are defined here to keep concerns well separated
from business logic and storage layers.
"""


class ConfigurationError(Exception):
    """Raised when a configuration-related operation fails."""


class DatabaseError(Exception):
    """Raised when a database operation fails."""


class AuthenticationError(Exception):
    """Raised when an authentication or authorization operation fails."""


class ValidationError(Exception):
    """Raised when input data fails validation rules."""


