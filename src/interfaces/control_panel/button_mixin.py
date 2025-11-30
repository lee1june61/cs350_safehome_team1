"""Button handler mixin for control panel."""


class ButtonMixin:
    """Mixin providing button handling methods."""

    def _digit(self, d: str):
        if self._state == self.STATE_IDLE:
            self._password.add_digit(d, self._transitions.try_login)
        elif self._state == self.STATE_CHANGING_PW:
            self._password.add_new_digit(d, self._transitions.finish_pw_change)
        elif self._state == self.STATE_PANIC_VERIFY:
            if getattr(self, "_panic_locked", False):
                return
            self._password.add_digit(d, self._security.handle_panic_code)

    def button1(self):
        if self._state == self.STATE_OFF:
            self._transitions.turn_on()
        else:
            self._digit("1")

    def button2(self):
        self._digit("2")

    def button3(self):
        if self._state == self.STATE_LOGGED_IN:
            self._transitions.turn_off()
        else:
            self._digit("3")

    def button4(self):
        self._digit("4")

    def button5(self):
        self._digit("5")

    def button6(self):
        if self._state == self.STATE_LOGGED_IN:
            self._transitions.reset()
        else:
            self._digit("6")

    def button7(self):
        if self._state == self.STATE_LOGGED_IN:
            self._security.arm("AWAY")
        else:
            self._digit("7")

    def button8(self):
        if self._state == self.STATE_LOGGED_IN:
            self._security.arm_home()
        else:
            self._digit("8")

    def button9(self):
        if self._state == self.STATE_LOGGED_IN:
            self._transitions.start_pw_change()
        else:
            self._digit("9")

    def button0(self):
        self._digit("0")

    def button_star(self):
        self._security.panic()

    def button_sharp(self):
        self._security.panic()

