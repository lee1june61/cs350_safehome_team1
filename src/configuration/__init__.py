"""SafeHome configuration and data management package.

This package contains the core configuration-related components:

* StorageManager        – DB abstraction / repository (SQLite, thread‑safe, singleton)
* ConfigurationManager  – Facade for configuration, modes, zones, and settings
* LoginInterface        – Authentication data model
* LoginManager          – Authentication and access‑level management
* SystemSettings        – Global system configuration
* SafeHomeMode          – Per‑mode sensor configuration
* SafetyZone            – Logical sensor groupings
* Log / LogManager      – Application‑level event logging
* Custom exceptions     – Domain‑specific error types

All public classes are implemented with type hints and Google‑style docstrings
to support unit testing and static analysis.
"""

from .exceptions import (
    ConfigurationError,
    DatabaseError,
    AuthenticationError,
    ValidationError,
)
from .storage_manager import StorageManager
from .configuration_manager import ConfigurationManager
from .login_interface import LoginInterface, AccessLevel
from .login_manager import LoginManager
from .system_settings import SystemSettings
from .safehome_mode import SafeHomeMode
from .safety_zone import SafetyZone
from .log import Log
from .log_manager import LogManager

__all__ = [
    "ConfigurationError",
    "DatabaseError",
    "AuthenticationError",
    "ValidationError",
    "StorageManager",
    "ConfigurationManager",
    "LoginInterface",
    "AccessLevel",
    "LoginManager",
    "SystemSettings",
    "SafeHomeMode",
    "SafetyZone",
    "Log",
    "LogManager",
]


