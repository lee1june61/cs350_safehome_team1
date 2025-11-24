"""Input validation utilities."""


def validate_password(password: str, required_length: int = 4) -> tuple[bool, str]:
    """Validate password format.

    Args:
        password: Password to validate
        required_length: Required password length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"

    if len(password) != required_length:
        return False, f"Password must be {required_length} digits"

    if not password.isdigit():
        return False, "Password must contain only digits"

    return True, ""


def validate_zone_name(name: str) -> tuple[bool, str]:
    """Validate safety zone name.

    Args:
        name: Zone name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Zone name cannot be empty"

    if len(name) > 50:
        return False, "Zone name too long (max 50 characters)"

    return True, ""
