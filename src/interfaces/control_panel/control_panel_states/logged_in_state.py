from .__init__ import ControlPanelState
from .off_state import OffState # Assuming OffState will be in its own file
from .changing_password_state import ChangingPasswordState # Assuming ChangingPasswordState will be in its own file


class LoggedInState(ControlPanelState):
    def enter(self) -> None:
        self._panel.set_display_short_message1(f"Welcome ({self._panel._access_level})")
        self._panel.set_display_short_message2("7=Away 8=Home")
        self._update_leds()

    def exit(self) -> None:
        pass

    def _update_leds(self) -> None:
        res = self._req('get_status')
        if res.get('success'):
            d = res.get('data', {})
            armed = d.get('armed', False)
            mode = d.get('mode', 'DISARMED')
            self._panel.set_armed_led(armed)
            self._panel.set_display_away(mode == 'AWAY')
            self._panel.set_display_stay(mode == 'HOME')

    def handle_button3(self) -> None: # Turn off
        self._panel.set_display_short_message1("Stopping...")
        self._panel.set_display_short_message2("Please wait")
        self._panel.after(500, self._complete_off)

    def _complete_off(self) -> None:
        self._req('turn_off')
        self._panel._access_level = None
        self._panel.transition_to(OffState(self._panel))

    def handle_button6(self) -> None: # Reset
        self._panel.set_display_short_message1("Resetting...")
        self._panel.set_display_short_message2("Please wait")
        self._panel.after(500, self._complete_reset)

    def _complete_reset(self) -> None:
        self._req('reset_system')
        self._panel.transition_to(OffState(self._panel))
        self._panel.after(300, lambda: self._panel.transition_to(BootingState(self._panel))) # Re-boot

    def handle_button7(self) -> None: # Arm AWAY
        res = self._req('arm_system', mode='AWAY')
        if res.get('success'):
            self._panel.set_display_short_message1("Armed: AWAY")
            self._panel.set_display_short_message2("")
        else:
            self._panel.set_display_short_message1("Cannot arm")
            msg = res.get('message', '')[:20]
            self._panel.set_display_short_message2(msg)
        self._update_leds()

    def handle_button8(self) -> None: # Arm HOME (disarm if currently armed)
        res = self._req('disarm_system') # Disarm system, sets to HOME mode
        self._panel.set_display_short_message1("HOME mode")
        self._panel.set_display_short_message2("Disarmed")
        self._update_leds()

    def handle_button9(self) -> None: # Change master password
        if self._panel._access_level != 'MASTER':
            self._panel.set_display_short_message1("Master only")
            return
        self._panel.transition_to(ChangingPasswordState(self._panel))

    def handle_button_star(self) -> None:
        self._req('panic')
        self._panel.set_display_short_message1("PANIC!")
        self._panel.set_display_short_message2("Calling service...")
    
    def handle_button_sharp(self) -> None:
        self.handle_button_star() # Same as star
