"""
SafeHomeControlPanel - Inherits from DeviceControlPanelAbstract (TA provided).

SRS References:
- V.1.a: Log onto system (4-digit password)
- V.1.d: Turn system on (Button 1 when OFF)
- V.1.e: Turn system off (Button 3 when logged in)
- V.1.f: Reset system (Button 6 when logged in)
- V.1.g: Change master password (Button 9 when logged in as MASTER)
- V.2.a: Arm/disarm system (Button 7=AWAY, Button 8=HOME)
- V.2.k: Call monitoring service (Button * or #, anytime)

Note: stay -> HOME unified (Home = Stay per spec)
"""
from typing import TYPE_CHECKING
from src.devices.device_control_panel_abstract import DeviceControlPanelAbstract

if TYPE_CHECKING:
    from src.core.system import System


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """SafeHome Control Panel - starts in OFF state per SRS V.1.d."""

    STATE_OFF = 'off'
    STATE_BOOTING = 'booting'
    STATE_IDLE = 'idle'
    STATE_LOGGED_IN = 'logged_in'
    STATE_CHANGING_PW = 'changing_pw'
    STATE_LOCKED = 'locked'

    def __init__(self, master, system: 'System'):
        super().__init__(master)
        self._system = system
        self._state = self.STATE_OFF
        self._pw_buffer = ''
        self._new_pw_buffer = ''
        self._access_level = None
        self._attempts = 3
        self._init_off()

    def _init_off(self):
        """Initialize to OFF state."""
        self._state = self.STATE_OFF
        self._pw_buffer = ''
        self._access_level = None
        self.set_powered_led(False)
        self.set_armed_led(False)
        self.set_display_short_message1("System OFF")
        self.set_display_short_message2("Press 1 to start")
        self.set_display_away(False)
        self.set_display_stay(False)  # HOME mode uses stay display

    def _req(self, cmd: str, **kw) -> dict:
        """Send request to system."""
        if not self._system:
            return {'success': False, 'message': 'System not connected'}
        return self._system.handle_request('control_panel', cmd, **kw)

    def send_command(self, cmd: str, **kw) -> dict:
        """A test helper method to directly send a command to the system."""
        return self._req(cmd, **kw)


    def _digit(self, d: str):
        """Handle digit input for password entry."""
        if self._state == self.STATE_IDLE:
            self._pw_buffer += d
            self.set_display_short_message2('*' * len(self._pw_buffer))
            if len(self._pw_buffer) == 4:
                self._try_login()
        elif self._state == self.STATE_CHANGING_PW:
            self._new_pw_buffer += d
            self.set_display_short_message2('*' * len(self._new_pw_buffer))
            if len(self._new_pw_buffer) == 4:
                self._finish_pw_change()

    def _try_login(self):
        """Attempt login with current password buffer."""
        res = self._req('login_control_panel', password=self._pw_buffer)
        self._pw_buffer = ''
        if res.get('success'):
            self._state = self.STATE_LOGGED_IN
            self._access_level = res.get('access_level', 'GUEST')
            self._attempts = 3
            self.set_display_short_message1(f"Welcome ({self._access_level})")
            self.set_display_short_message2("7=Away 8=Home")
            self._update_leds()
        else:
            self._attempts -= 1
            if self._attempts <= 0:
                self._state = self.STATE_LOCKED
                self.set_display_short_message1("LOCKED")
                self.set_display_short_message2("Wait 60 sec")
                self.after(60000, self._unlock)
            else:
                self.set_display_short_message1("Wrong password")
                self.set_display_short_message2(f"{self._attempts} tries left")

    def _unlock(self):
        """Unlock after timeout."""
        self._attempts = 3
        self._state = self.STATE_IDLE
        self.set_display_short_message1("Enter password")
        self.set_display_short_message2("")

    def _update_leds(self):
        """Update LED and display status from system."""
        res = self._req('get_status')
        if res.get('success'):
            d = res.get('data', {})
            armed = d.get('armed', False)
            mode = d.get('mode', 'DISARMED')
            self.set_armed_led(armed)
            self.set_display_away(mode == 'AWAY')
            self.set_display_stay(mode == 'HOME')  # HOME mode

    def _turn_on(self):
        """Turn system on - SRS V.1.d."""
        if self._state != self.STATE_OFF:
            return
        self._state = self.STATE_BOOTING
        self.set_display_short_message1("Starting...")
        self.set_display_short_message2("Please wait")
        self.set_powered_led(True)
        self.after(1000, self._boot_done)

    def _boot_done(self):
        """Complete boot sequence."""
        self._req('turn_on')
        self._state = self.STATE_IDLE
        self.set_display_short_message1("Enter password")
        self.set_display_short_message2("")

    def _turn_off(self):
        """Turn system off - SRS V.1.e."""
        if self._state != self.STATE_LOGGED_IN:
            return
        self.set_display_short_message1("Stopping...")
        self.set_display_short_message2("Please wait")
        self.after(500, self._complete_off)

    def _complete_off(self):
        self._req('turn_off')
        self._access_level = None
        self._init_off()

    def _reset(self):
        """Reset system - SRS V.1.f."""
        if self._state != self.STATE_LOGGED_IN:
            return
        self.set_display_short_message1("Resetting...")
        self.set_display_short_message2("Please wait")
        self.after(500, self._complete_reset)

    def _complete_reset(self):
        self._req('reset_system')
        self._init_off()
        self.after(300, self._turn_on)

    def _arm(self, mode: str):
        """Arm system - SRS V.2.a."""
        if self._state != self.STATE_LOGGED_IN:
            return
        res = self._req('arm_system', mode=mode)
        if res.get('success'):
            self.set_display_short_message1(f"Armed: {mode}")
            self.set_display_short_message2("")
        else:
            self.set_display_short_message1("Cannot arm")
            msg = res.get('message', '')[:20]
            self.set_display_short_message2(msg)
        self._update_leds()

    def _disarm(self):
        """Disarm to HOME mode - SRS V.2.a."""
        if self._state != self.STATE_LOGGED_IN:
            return
        self._req('disarm_system')
        self.set_display_short_message1("HOME mode")
        self.set_display_short_message2("Disarmed")
        self._update_leds()

    def _start_pw_change(self):
        """Start password change - SRS V.1.g."""
        if self._state != self.STATE_LOGGED_IN:
            return
        if self._access_level != 'MASTER':
            self.set_display_short_message1("Master only")
            return
        self._state = self.STATE_CHANGING_PW
        self._new_pw_buffer = ''
        self.set_display_short_message1("New password:")
        self.set_display_short_message2("")

    def _finish_pw_change(self):
        """Complete password change."""
        self._req('change_password', new_password=self._new_pw_buffer)
        self._new_pw_buffer = ''
        self._state = self.STATE_LOGGED_IN
        self.set_display_short_message1("Password changed")
        self.set_display_short_message2("")

    def _panic(self):
        """Panic button - SRS V.2.k."""
        self._req('panic')
        self.set_display_short_message1("PANIC!")
        self.set_display_short_message2("Calling service...")

    # Button implementations (required by abstract class)
    def button1(self):
        if self._state == self.STATE_OFF:
            self._turn_on()
        else:
            self._digit('1')

    def button2(self): self._digit('2')
    
    def button3(self):
        if self._state == self.STATE_LOGGED_IN:
            self._turn_off()
        else:
            self._digit('3')

    def button4(self): self._digit('4')
    def button5(self): self._digit('5')

    def button6(self):
        if self._state == self.STATE_LOGGED_IN:
            self._reset()
        else:
            self._digit('6')

    def button7(self):
        if self._state == self.STATE_LOGGED_IN:
            self._arm('AWAY')
        else:
            self._digit('7')

    def button8(self):
        if self._state == self.STATE_LOGGED_IN:
            self._disarm()  # HOME mode
        else:
            self._digit('8')

    def button9(self):
        if self._state == self.STATE_LOGGED_IN:
            self._start_pw_change()
        else:
            self._digit('9')

    def button0(self): self._digit('0')
    def button_star(self): self._panic()
    def button_sharp(self): self._panic()


def run_control_panel(system: 'System', master=None) -> SafeHomeControlPanel:
    """Factory function to create control panel."""
    return SafeHomeControlPanel(master, system)
