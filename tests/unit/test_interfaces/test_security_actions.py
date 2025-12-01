"""
Unit tests for SecurityActions handler.
"""

from src.interfaces.control_panel.handlers.security_actions import SecurityActions


class DummySystemCtrl:
    def __init__(self):
        self.arm_calls = []
        self.panic_called = False

    def arm(self, mode):
        self.arm_calls.append(mode)
        return self.next_response

    def panic(self):
        self.panic_called = True


class DummyPassword:
    def __init__(self, responses):
        self.responses = responses
        self.calls = 0

    def verify_master_code(self):
        resp = self.responses[self.calls]
        self.calls += 1
        return resp


class DummyDisplay:
    def __init__(self):
        self.panic_error_shown = False

    def show_panic_verify_error(self):
        self.panic_error_shown = True


class DummyPanel:
    STATE_LOGGED_IN = "LOGGED_IN"
    STATE_IDLE = "IDLE"

    def __init__(self):
        self._state = self.STATE_LOGGED_IN
        self._system_ctrl = DummySystemCtrl()
        self._system_ctrl.next_response = {"success": True}
        self._password = DummyPassword([])
        self._display = DummyDisplay()
        self.messages = ["", ""]
        self.led_updates = 0
        self.enter_panic_called = 0
        self.exit_panic_called = 0
        self.clear_requests = []
        self.panic_lock = None

    def set_display_short_message1(self, msg):
        self.messages[0] = msg

    def set_display_short_message2(self, msg):
        self.messages[1] = msg

    def _update_leds(self):
        self.led_updates += 1

    def enter_panic_verification(self):
        self.enter_panic_called += 1

    def exit_panic_verification(self):
        self.exit_panic_called += 1

    def send_request(self, action):
        self.clear_requests.append(action)

    def show_panic_lock(self, message, seconds):
        self.panic_lock = (message, seconds)


class TestSecurityActions:
    def test_arm_requires_logged_in(self):
        panel = DummyPanel()
        panel._state = panel.STATE_IDLE
        actions = SecurityActions(panel)

        actions.arm("AWAY")

        assert panel._system_ctrl.arm_calls == []

    def test_arm_success_and_failure(self):
        panel = DummyPanel()
        actions = SecurityActions(panel)

        actions.arm("AWAY")
        assert panel.messages[0] == "Armed: AWAY"
        assert panel.messages[1] == ""
        assert panel.led_updates == 1

        panel._system_ctrl.next_response = {"success": False, "message": "Doors open somewhere in house"}
        actions.arm("AWAY")
        assert panel.messages[0] == "Cannot arm"
        assert panel.messages[1] == "Doors open somewhere"

    def test_arm_home_messages(self):
        panel = DummyPanel()
        actions = SecurityActions(panel)

        actions.arm_home()
        assert panel.messages[0] == "HOME mode"
        assert panel.messages[1] == "Perimeter armed"

        panel._system_ctrl.next_response = {"success": False, "message": "Something wrong"}
        actions.arm_home()
        assert panel.messages[0] == "Cannot arm HOME"
        assert panel.messages[1] == "Something wrong"

    def test_panic_flow(self):
        panel = DummyPanel()
        actions = SecurityActions(panel)

        actions.panic()
        assert panel._system_ctrl.panic_called is True
        assert panel.enter_panic_called == 1

    def test_handle_panic_code_success(self):
        panel = DummyPanel()
        panel._password = DummyPassword([{"success": True}])
        actions = SecurityActions(panel)

        actions.handle_panic_code()

        assert panel.messages[0] == "Panic cleared"
        assert panel.clear_requests == ["clear_alarm"]
        assert panel.exit_panic_called == 1

    def test_handle_panic_code_locked(self):
        panel = DummyPanel()
        panel._password = DummyPassword(
            [{"success": False, "locked": True, "message": "Locked", "seconds_remaining": 30}]
        )
        actions = SecurityActions(panel)

        actions.handle_panic_code()

        assert panel.panic_lock == ("Locked", 30)

    def test_handle_panic_code_attempts_remaining(self):
        panel = DummyPanel()
        panel._password = DummyPassword(
            [
                {
                    "success": False,
                    "locked": False,
                    "attempts_remaining": 2,
                }
            ]
        )
        actions = SecurityActions(panel)

        actions.handle_panic_code()

        assert panel._display.panic_error_shown is True
        assert panel.messages[1] == "2 attempts left"


