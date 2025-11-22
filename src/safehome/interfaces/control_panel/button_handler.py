"""Button Handler with Context-Aware Functionality.

Same buttons perform different functions based on panel state.
"""

from typing import TYPE_CHECKING, Optional, Any
from .constants import (
    STATE_IDLE,
    STATE_LOGGED_IN,
    STATE_ALARM,
    STATE_LOCKED,
    STATE_ARMED_AWAY,
    STATE_ARMED_STAY,
    STATE_CHANGE_PASSWORD,
    STATE_ENTER_OLD_PASSWORD,
    STATE_ENTER_NEW_PASSWORD,
    STATE_CONFIRM_NEW_PASSWORD,
    STATE_DISARMING,
    PASSWORD_LENGTH,
    MAX_LOGIN_ATTEMPTS,
    MSG_PANIC,
    MSG_CALLING_SERVICE,
    MSG_CANNOT_CANCEL,
    MSG_INPUT_CLEARED,
    MSG_ENTER_PASSWORD,
    MSG_WRONG_PASSWORD,
    MSG_LOGIN_OK,
    MSG_ARM_MENU,
    MSG_FUNCTION_MENU_1,
    MSG_FUNCTION_MENU_2,
    MSG_ARMED_AWAY,
    MSG_ARMED_STAY,
    MSG_PRESS_EXIT,
    MSG_SYSTEM_LOCKED,
    MSG_WAIT,
    MSG_CHANGE_PASSWORD,
    MSG_ENTER_OLD_PASS,
    MSG_ENTER_NEW_PASS,
    MSG_CONFIRM_NEW_PASS,
    MSG_PASSWORD_CHANGED,
    MSG_PASSWORD_MISMATCH,
    MSG_SYSTEM_RESET,
    MSG_SHUTTING_DOWN,
    MSG_SYSTEM_OFF,
    MSG_CALL_SERVICE,
    MSG_SERVICE_CALLED,
    MSG_INVALID_OPTION,
    MSG_ENTER_TO_DISARM,
    MSG_SYSTEM_DISARMED,
    DEMO_MASTER_PASSWORD,
    DEMO_GUEST_PASSWORD,
)

if TYPE_CHECKING:
    from .safehome_control_panel import SafeHomeControlPanel


class ButtonHandler:
    """Handles context-aware button press events."""
    
    def __init__(
        self,
        panel: 'SafeHomeControlPanel',
        system: Optional[Any] = None
    ) -> None:
        """Initialize button handler.
        
        Args:
            panel: Control panel instance
            system: System instance (from backend team)
        """
        self.panel = panel
        self.system = system
    
    def handle_numeric(self, digit: str) -> None:
        """Handle numeric button (0-9) - context aware.
        
        Args:
            digit: Digit pressed
        """
        state = self.panel.state.current_state
        
        if self.panel.state.is_locked:
            return
        
        # Context 1: IDLE - Login
        if state == STATE_IDLE:
            self._handle_login_input(digit)
        
        # Context 2: LOGGED_IN - Menu selection
        elif state == STATE_LOGGED_IN:
            self._handle_menu_selection(digit)
        
        # Context 3: ARMED - Disarm input
        elif state in [STATE_ARMED_AWAY, STATE_ARMED_STAY]:
            self._handle_disarm_input(digit)
        
        # Context 4: Password change - New password input
        elif state in [
            STATE_ENTER_OLD_PASSWORD,
            STATE_ENTER_NEW_PASSWORD,
            STATE_CONFIRM_NEW_PASSWORD
        ]:
            self._handle_password_change_input(digit)
    
    def handle_panic(self) -> None:
        """Handle panic button (*) - always same function."""
        print("[PANEL] PANIC!")
        
        self.panel.state.current_state = STATE_ALARM
        self.panel.display.set_armed_led(True)
        self.panel.display.show_message(MSG_PANIC, MSG_CALLING_SERVICE)
        
        if self.system:
            self.system.call_monitoring_service(panic=True)
    
    def handle_reset(self) -> None:
        """Handle reset button (#) - context aware."""
        state = self.panel.state.current_state
        
        # Cannot cancel panic
        if state == STATE_ALARM:
            self.panel.display.show_message("", MSG_CANNOT_CANCEL)
            return
        
        if self.panel.state.is_locked:
            return
        
        # Context 1: IDLE - Clear input
        if state == STATE_IDLE:
            self._handle_clear_input()
        
        # Context 2: LOGGED_IN - Logout
        elif state == STATE_LOGGED_IN:
            self._handle_logout()
        
        # Context 3: ARMED - Cancel
        elif state in [STATE_ARMED_AWAY, STATE_ARMED_STAY]:
            self._handle_cancel_disarm()
        
        # Context 4: Password change - Cancel
        elif self.panel.state.is_changing_password():
            self._handle_cancel_password_change()
    
    # Login Context
    
    def _handle_login_input(self, digit: str) -> None:
        """Handle numeric input during login."""
        state = self.panel.state
        state.add_digit(digit)
        
        password_len = len(state.password_buffer)
        self.panel.display.show_masked_password(password_len)
        
        if state.is_password_complete(PASSWORD_LENGTH):
            self._attempt_login()
    
    def _attempt_login(self) -> None:
        """Attempt login with System."""
        state = self.panel.state
        password = state.get_password()
        
        if self.system:
            success = self.system.login_control_panel(password)
        else:
            success = password in [
                DEMO_MASTER_PASSWORD,
                DEMO_GUEST_PASSWORD
            ]
        
        if success:
            state.reset_attempts()
            state.current_state = STATE_LOGGED_IN
            self.panel.display.show_message(MSG_LOGIN_OK, MSG_ARM_MENU)
            self.panel.display.show_message(MSG_FUNCTION_MENU_1)
            self.panel.display.show_message(MSG_FUNCTION_MENU_2)
        else:
            attempts = state.increment_attempts()
            if attempts >= MAX_LOGIN_ATTEMPTS:
                self._lock_system()
            else:
                remaining = MAX_LOGIN_ATTEMPTS - attempts
                self.panel.display.show_message(
                    MSG_WRONG_PASSWORD,
                    f"{remaining} tries left"
                )
    
    def _lock_system(self) -> None:
        """Lock system after max attempts."""
        state = self.panel.state
        state.is_locked = True
        state.current_state = STATE_LOCKED
        
        self.panel.display.show_message(MSG_SYSTEM_LOCKED, MSG_WAIT)
        
        if self.system:
            self.system.lock_system()
    
    def _handle_clear_input(self) -> None:
        """Clear login input."""
        self.panel.state.reset_password()
        self.panel.display.show_message(MSG_INPUT_CLEARED, MSG_ENTER_PASSWORD)
    
    # Menu Context (Logged In)
    
    def _handle_menu_selection(self, digit: str) -> None:
        """Handle menu selection when logged in.
        
        1: Arm Away
        2: Arm Stay
        3: Change Password
        4: Call Monitoring Service
        5: System Settings (future)
        9: Reset System
        0: Turn Off System
        """
        if digit == '1':
            self.arm_away()
        elif digit == '2':
            self.arm_stay()
        elif digit == '3':
            self._start_password_change()
        elif digit == '4':
            self._call_monitoring_service()
        elif digit == '5':
            self._show_settings_menu()
        elif digit == '9':
            self._reset_system()
        elif digit == '0':
            self._turn_off_system()
        else:
            self.panel.display.show_message(MSG_INVALID_OPTION)
    
    def arm_away(self) -> None:
        """Arm system in away mode."""
        if self.system:
            success = self.system.arm_system(mode="away")
        else:
            success = True
        
        if success:
            self.panel.state.current_state = STATE_ARMED_AWAY
            self.panel.display.set_armed_led(True)
            self.panel.display.set_away_mode(True)
            self.panel.display.set_stay_mode(False)
            self.panel.display.show_message(MSG_ARMED_AWAY, MSG_PRESS_EXIT)
    
    def arm_stay(self) -> None:
        """Arm system in stay mode."""
        if self.system:
            success = self.system.arm_system(mode="stay")
        else:
            success = True
        
        if success:
            self.panel.state.current_state = STATE_ARMED_STAY
            self.panel.display.set_armed_led(True)
            self.panel.display.set_away_mode(False)
            self.panel.display.set_stay_mode(True)
            self.panel.display.show_message(MSG_ARMED_STAY, MSG_PRESS_EXIT)
    
    def _start_password_change(self) -> None:
        """Start password change process."""
        self.panel.state.current_state = STATE_ENTER_OLD_PASSWORD
        self.panel.display.show_message(
            MSG_CHANGE_PASSWORD,
            MSG_ENTER_OLD_PASS
        )
    
    def _call_monitoring_service(self) -> None:
        """Call monitoring service (non-panic)."""
        self.panel.display.show_message(MSG_CALL_SERVICE, MSG_CALLING_SERVICE)
        
        if self.system:
            self.system.call_monitoring_service(panic=False)
        
        self.panel.display.show_message(MSG_SERVICE_CALLED)
    
    def _show_settings_menu(self) -> None:
        """Show system settings menu (placeholder)."""
        self.panel.display.show_message("Settings", "Coming Soon")
    
    def _reset_system(self) -> None:
        """Reset system."""
        self.panel.display.show_message(MSG_SYSTEM_RESET, "Please wait...")
        
        if self.system:
            self.system.reset_system()
        
        # Reinitialize after reset
        self.panel.state.current_state = STATE_IDLE
        self.panel._initialize()
    
    def _turn_off_system(self) -> None:
        """Turn off system."""
        self.panel.display.show_message(MSG_SYSTEM_OFF, MSG_SHUTTING_DOWN)
        
        if self.system:
            self.system.turn_off()
        
        # In real implementation, would close the program
        print("[PANEL] System turned off")
    
    def _handle_logout(self) -> None:
        """Logout user."""
        self.panel.state.current_state = STATE_IDLE
        self.panel._initialize()
    
    # Armed Context (Disarming)
    
    def _handle_disarm_input(self, digit: str) -> None:
        """Handle disarm code input."""
        state = self.panel.state
        state.add_digit(digit)
        
        password_len = len(state.password_buffer)
        self.panel.display.show_masked_password(password_len)
        
        if state.is_password_complete(PASSWORD_LENGTH):
            self._attempt_disarm()
    
    def _attempt_disarm(self) -> None:
        """Attempt to disarm with password."""
        state = self.panel.state
        password = state.get_password()
        
        # Verify password
        if self.system:
            success = self.system.login_control_panel(password)
        else:
            success = password in [
                DEMO_MASTER_PASSWORD,
                DEMO_GUEST_PASSWORD
            ]
        
        if success:
            # Disarm system
            if self.system:
                self.system.disarm_system()
            
            state.current_state = STATE_LOGGED_IN
            self.panel.display.set_armed_led(False)
            self.panel.display.clear_mode_indicators()
            self.panel.display.show_message(
                MSG_SYSTEM_DISARMED,
                MSG_ARM_MENU
            )
        else:
            state.reset_password()
            self.panel.display.show_message(
                MSG_WRONG_PASSWORD,
                MSG_ENTER_TO_DISARM
            )
    
    def _handle_cancel_disarm(self) -> None:
        """Cancel disarm attempt."""
        self.panel.state.reset_password()
        self.panel.display.show_message("", MSG_PRESS_EXIT)
    
    # Password Change Context
    
    def _handle_password_change_input(self, digit: str) -> None:
        """Handle password change input."""
        state = self.panel.state
        current = state.current_state
        
        state.add_digit(digit)
        password_len = len(state.password_buffer)
        self.panel.display.show_masked_password(password_len)
        
        if not state.is_password_complete(PASSWORD_LENGTH):
            return
        
        password = state.get_password()
        
        if current == STATE_ENTER_OLD_PASSWORD:
            # Verify old password
            if self.system:
                success = self.system.verify_password(password)
            else:
                success = password == DEMO_MASTER_PASSWORD
            
            if success:
                state.old_password = password
                state.current_state = STATE_ENTER_NEW_PASSWORD
                self.panel.display.show_message(
                    MSG_CHANGE_PASSWORD,
                    MSG_ENTER_NEW_PASS
                )
            else:
                state.reset_password_change()
                state.current_state = STATE_LOGGED_IN
                self.panel.display.show_message(
                    MSG_WRONG_PASSWORD,
                    MSG_ARM_MENU
                )
        
        elif current == STATE_ENTER_NEW_PASSWORD:
            state.new_password = password
            state.current_state = STATE_CONFIRM_NEW_PASSWORD
            self.panel.display.show_message(
                MSG_CHANGE_PASSWORD,
                MSG_CONFIRM_NEW_PASS
            )
        
        elif current == STATE_CONFIRM_NEW_PASSWORD:
            if password == state.new_password:
                # Change password
                if self.system:
                    self.system.change_password(
                        state.old_password,
                        state.new_password
                    )
                
                state.reset_password_change()
                state.current_state = STATE_LOGGED_IN
                self.panel.display.show_message(
                    MSG_PASSWORD_CHANGED,
                    MSG_ARM_MENU
                )
            else:
                state.reset_password_change()
                state.current_state = STATE_LOGGED_IN
                self.panel.display.show_message(
                    MSG_PASSWORD_MISMATCH,
                    MSG_ARM_MENU
                )
    
    def _handle_cancel_password_change(self) -> None:
        """Cancel password change."""
        self.panel.state.reset_password_change()
        self.panel.state.current_state = STATE_LOGGED_IN
        self.panel.display.show_message("Cancelled", MSG_ARM_MENU)