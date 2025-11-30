"""Identity verification helper."""


class IdentityValidator:
    """Validates phone/address info for verification flows."""

    def __init__(self):
        self._verified = False

    def reset(self):
        self._verified = False

    @property
    def verified(self) -> bool:
        return self._verified

    def verify(self, value: str):
        v = value.strip()
        if not v:
            return False, "Please enter address or phone number"

        cleaned = v.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        if cleaned.isdigit():
            if len(cleaned) >= 10:
                self._verified = True
                return True, None
            return False, "Phone number must be at least 10 digits"

        if len(v) >= 5 and any(c.isalpha() for c in v):
            self._verified = True
            return True, None

        return (
            False,
            "Invalid verification. Enter a valid phone number (10+ digits) or address (5+ chars with letters)",
        )


