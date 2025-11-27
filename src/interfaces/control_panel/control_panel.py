"""
SafeHomeControlPanel - Control Panel using DeviceControlPanelAbstract
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from src.devices import DeviceControlPanelAbstract

if TYPE_CHECKING:
    from src.core.system import System


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """SafeHome Control Panel implementation."""
    
    STATE_IDLE = 'idle'
    STATE_ENTERING_PASSWORD = 'entering_password'
    STATE_LOGGED_IN = 'logged_in'
    STATE_CHANGING_PASSWORD = 'changing_password'
    
    def __init__(self, master, system: 'System'):
        super().__init__(master)
        self._system = system
        self._state = self.STATE_IDLE
        self._password_buffer = ''
        self._new_password_buffer = ''
        self._access_level: Optional[str] = None
        self._login_attempts = 3
        
        self._init_display()
    
    def _init_display(self) -> None:
        self.set_powered_led(True)
        self.set_armed_led(False)
        self.set_display_short_message1("Enter password")
        self.set_display_short_message2("")
        self._state = self.STATE_ENTERING_PASSWORD
    
    def _send(self, command: str, **kwargs) -> Dict[str, Any]:
        if not self._system:
            return {'success': False, 'message': 'System not connected'}
        return self._system.handle_request(source='control_panel', command=command, **kwargs)
    
    def _handle_digit(self, digit: str) -> None:
        if self._state == self.STATE_ENTERING_PASSWORD:
            self._password_buffer += digit
            self.set_display_short_message2('*' * len(self._password_buffer))
            
            if len(self._password_buffer) == 4:
                self._try_login()
        
        elif self._state == self.STATE_CHANGING_PASSWORD:
            self._new_password_buffer += digit
            self.set_display_short_message2('*' * len(self._new_password_buffer))
            
            if len(self._new_password_buffer) == 4:
                self._finish_password_change()
    
    def _try_login(self) -> None:
        response = self._send('login_control_panel', password=self._password_buffer)
        self._password_buffer = ''
        
        if response.get('success'):
            self._state = self.STATE_LOGGED_IN
            self._access_level = response.get('access_level', 'GUEST')
            self._login_attempts = 3
            self.set_display_short_message1(f"Welcome ({self._access_level})")
            self.set_display_short_message2("System ready")
            self._update_status()
        else:
            self._login_attempts -= 1
            if self._login_attempts <= 0:
                self.set_display_short_message1("LOCKED")
                self.set_display_short_message2("Wait 60 seconds")
                self.after(60000, self._unlock)
            else:
                self.set_display_short_message1("Wrong password")
                self.set_display_short_message2(f"{self._login_attempts} tries left")
    
    def _unlock(self) -> None:
        self._login_attempts = 3
        self._init_display()
    
    def _update_status(self) -> None:
        response = self._send('get_status')
        if response.get('success'):
            data = response.get('data', {})
            armed = data.get('armed', False)
            mode = data.get('mode')
            
            self.set_armed_led(armed)
            self.set_display_away(mode == 'AWAY')
            self.set_display_stay(mode == 'HOME')
            self.set_display_not_ready(data.get('doors_windows_open', False))
    
    def _arm_system(self, mode: str) -> None:
        if self._state != self.STATE_LOGGED_IN:
            self.set_display_short_message1("Login first")
            return
        
        response = self._send('arm_system', mode=mode)
        if response.get('success'):
            self.set_display_short_message1(f"Armed: {mode}")
            self.set_display_short_message2("")
            self._update_status()
        else:
            self.set_display_short_message1("Cannot arm")
            self.set_display_short_message2(response.get('message', '')[:20])
    
    def _disarm_system(self) -> None:
        if self._state != self.STATE_LOGGED_IN:
            return
        
        response = self._send('disarm_system')
        if response.get('success'):
            self.set_display_short_message1("Disarmed")
            self.set_display_short_message2("")
            self._update_status()
    
    def _trigger_panic(self) -> None:
        response = self._send('panic')
        if response.get('success'):
            self.set_display_short_message1("PANIC!")
            self.set_display_short_message2("Calling service...")
    
    def _start_password_change(self) -> None:
        if self._state != self.STATE_LOGGED_IN:
            return
        if self._access_level != 'MASTER':
            self.set_display_short_message1("Master only")
            return
        
        self._state = self.STATE_CHANGING_PASSWORD
        self._new_password_buffer = ''
        self.set_display_short_message1("New password:")
        self.set_display_short_message2("")
    
    def _finish_password_change(self) -> None:
        response = self._send('change_password', new_password=self._new_password_buffer)
        self._new_password_buffer = ''
        self._state = self.STATE_LOGGED_IN
        
        if response.get('success'):
            self.set_display_short_message1("Password changed")
        else:
            self.set_display_short_message1("Change failed")
        self.set_display_short_message2("")
    
    # Button implementations
    def button1(self):
        if self._state == self.STATE_LOGGED_IN:
            self.set_display_short_message1("System ON")
        else:
            self._handle_digit('1')
    
    def button2(self):
        self._handle_digit('2')
    
    def button3(self):
        if self._state == self.STATE_LOGGED_IN:
            response = self._send('turn_off')
            if response.get('success'):
                self.set_display_short_message1("System OFF")
                self.set_powered_led(False)
        else:
            self._handle_digit('3')
    
    def button4(self):
        self._handle_digit('4')
    
    def button5(self):
        self._handle_digit('5')
    
    def button6(self):
        if self._state == self.STATE_LOGGED_IN:
            response = self._send('reset_system')
            if response.get('success'):
                self.set_display_short_message1("System reset")
                self._update_status()
        else:
            self._handle_digit('6')
    
    def button7(self):
        if self._state == self.STATE_LOGGED_IN:
            self._arm_system('AWAY')
        else:
            self._handle_digit('7')
    
    def button8(self):
        if self._state == self.STATE_LOGGED_IN:
            self._arm_system('HOME')
        else:
            self._handle_digit('8')
    
    def button9(self):
        if self._state == self.STATE_LOGGED_IN:
            self._start_password_change()
        else:
            self._handle_digit('9')
    
    def button0(self):
        self._handle_digit('0')
    
    def button_star(self):
        self._trigger_panic()
    
    def button_sharp(self):
        self._trigger_panic()


def run_control_panel(master, system: 'System') -> SafeHomeControlPanel:
    return SafeHomeControlPanel(master, system)
