"""Security management service."""


class SecurityService:
    """Service for security operations.

    Following the Security-related classes from SDS:
    - LoginManager
    - System security functions
    """

    def __init__(self, system):
        """Initialize security service.

        Args:
            system: SafeHome system instance
        """
        self.system = system
        self._login_attempts = 0
        self._max_attempts = 3

    def login(self, password: str) -> bool:
        """Attempt login with password.

        Args:
            password: Password to attempt

        Returns:
            True if login successful
        """
        try:
            if self.system.login_control_panel(password):
                self._login_attempts = 0
                return True
            else:
                self._login_attempts += 1
                return False
        except Exception as e:
            print(f"Login error: {e}")
            self._login_attempts += 1
            return False

    def logout(self):
        """Logout current user."""
        self.system.logout()
        self._login_attempts = 0

    def is_locked_out(self) -> bool:
        """Check if system is locked due to too many attempts."""
        return self._login_attempts >= self._max_attempts

    def reset_attempts(self):
        """Reset login attempts counter."""
        self._login_attempts = 0

    def get_attempts_remaining(self) -> int:
        """Get remaining login attempts."""
        return max(0, self._max_attempts - self._login_attempts)

    def set_security_mode(self, mode: str) -> bool:
        """Set security mode.

        Args:
            mode: Security mode (ARMED_HOME, ARMED_AWAY, etc.)

        Returns:
            True if successful
        """
        try:
            self.system.set_security_mode(mode)
            return True
        except Exception as e:
            print(f"Error setting security mode: {e}")
            return False

    def get_security_mode(self) -> str:
        """Get current security mode."""
        return self.system.get_security_mode()

    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change master password.

        Args:
            old_password: Current password
            new_password: New password

        Returns:
            True if successful
        """
        return self.system.change_password(old_password, new_password)

    def call_monitoring_service(self, reason: str = "PANIC"):
        """Call monitoring service.

        Args:
            reason: Reason for call
        """
        self.system.call_monitoring_service(reason)
