"""
Unit tests for IdentityValidator to improve branch coverage.
"""

from src.core.services.auth.identity_validator import IdentityValidator


class TestIdentityValidator:
    def test_set_expected_phone_normalizes_and_requires_match(self):
        validator = IdentityValidator()
        validator.set_expected_phone("010-1234-5678")

        success, error = validator.verify("010 1234 5678")
        assert success is True
        assert error is None
        assert validator.verified is True

        success, error = validator.verify("0000")
        assert success is False
        assert error == "Phone number does not match our records"
        assert validator.verified is True  # previous success persists until reset

    def test_verify_without_expected_phone_requires_length(self):
        validator = IdentityValidator()

        success, error = validator.verify("12345")
        assert success is False
        assert error == "Phone number must be at least 10 digits"
        assert validator.verified is False

        success, error = validator.verify("1112223333")
        assert success is True
        assert error is None
        assert validator.verified is True

    def test_verify_handles_missing_input(self):
        validator = IdentityValidator()
        validator.set_expected_phone("0100000000")

        success, error = validator.verify("")
        assert success is False
        assert error == "Enter the registered phone number"
        assert validator.verified is False



