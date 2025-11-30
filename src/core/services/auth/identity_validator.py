"""Identity verification helper."""


class IdentityValidator:
    """Validates phone info for verification flows."""

    def __init__(self):
        self._verified = False
        self._expected_phone: str | None = None

    def reset(self):
        self._verified = False

    @property
    def verified(self) -> bool:
        return self._verified

    def set_expected_phone(self, phone: str):
        self._expected_phone = self._normalize(phone)
        self._verified = False

    def _normalize(self, value: str) -> str:
        return "".join(ch for ch in (value or "") if ch.isdigit())

    def verify(self, value: str):
        digits = self._normalize(value)
        if not digits:
            return False, "Enter the registered phone number"

        if self._expected_phone:
            if digits == self._expected_phone:
                self._verified = True
                return True, None
            return False, "Phone number does not match our records"

        if len(digits) >= 10:
            self._verified = True
            return True, None

        return False, "Phone number must be at least 10 digits"


