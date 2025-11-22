"""Panel State Manager.

Manages UI state with context-aware button functionality.
"""

from typing import Dict, Any, Optional
from .constants import (
    STATE_IDLE,
    STATE_ARMED_AWAY,
    STATE_ARMED_STAY,
    STATE_CHANGE_PASSWORD,
)


class PanelState:
    """Manages control panel UI state."""
    
    def __init__(self) -> None:
        """Initialize panel state."""
        self.current_state = STATE_IDLE
        self.previous_state: Optional[str] = None
        self.login_attempts = 0
        self.is_locked = False
        self.password_buffer = ""
        self.old_password = ""
        self.new_password = ""
    
    def save_state(self) -> None:
        """Save current state for restoration."""
        self.previous_state = self.current_state
    
    def restore_state(self) -> None:
        """Restore previous state."""
        if self.previous_state:
            self.current_state = self.previous_state
            self.previous_state = None
    
    def reset_password(self) -> None:
        """Clear password buffer."""
        self.password_buffer = ""
    
    def reset_password_change(self) -> None:
        """Clear password change buffers."""
        self.old_password = ""
        self.new_password = ""
        self.password_buffer = ""
    
    def add_digit(self, digit: str) -> None:
        """Add digit to password buffer.
        
        Args:
            digit: Digit to add (0-9)
        """
        self.password_buffer += digit
    
    def get_password(self) -> str:
        """Get current password and clear buffer.
        
        Returns:
            Password string
        """
        password = self.password_buffer
        self.password_buffer = ""
        return password
    
    def get_masked_password(self, mask_char: str = "*") -> str:
        """Get masked password for display.
        
        Args:
            mask_char: Character to use for masking
            
        Returns:
            Masked password string
        """
        return mask_char * len(self.password_buffer)
    
    def is_password_complete(self, length: int) -> bool:
        """Check if password is complete.
        
        Args:
            length: Required password length
            
        Returns:
            True if complete
        """
        return len(self.password_buffer) >= length
    
    def increment_attempts(self) -> int:
        """Increment and return login attempts.
        
        Returns:
            Current number of attempts
        """
        self.login_attempts += 1
        return self.login_attempts
    
    def reset_attempts(self) -> None:
        """Reset login attempts counter."""
        self.login_attempts = 0
    
    def is_armed(self) -> bool:
        """Check if system is armed.
        
        Returns:
            True if armed
        """
        return self.current_state in [STATE_ARMED_AWAY, STATE_ARMED_STAY]
    
    def is_changing_password(self) -> bool:
        """Check if in password change mode.
        
        Returns:
            True if changing password
        """
        return STATE_CHANGE_PASSWORD in self.current_state
    
    def get_status(self) -> Dict[str, Any]:
        """Get current state status.
        
        Returns:
            Status dictionary
        """
        return {
            'state': self.current_state,
            'is_locked': self.is_locked,
            'login_attempts': self.login_attempts,
            'armed': self.is_armed(),
            'changing_password': self.is_changing_password()
        }