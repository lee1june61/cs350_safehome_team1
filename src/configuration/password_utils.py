"""Password hashing and validation utilities."""

import hashlib
from .exceptions import ValidationError


def hash_password(raw_password: str) -> str:
    """Return SHA-256 hash of password."""
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def validate_password_policy(
    password: str,
    min_length: int = 8,
    requires_digit: bool = True,
    requires_special: bool = False,
) -> None:
    """Validate password against policy; raise ValidationError on failure."""
    if len(password) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters")
    if requires_digit and not any(ch.isdigit() for ch in password):
        raise ValidationError("Password must contain at least one digit")
    if requires_special and not any(not ch.isalnum() for ch in password):
        raise ValidationError("Password must contain at least one special character")
