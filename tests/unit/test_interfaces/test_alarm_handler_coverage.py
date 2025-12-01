from src.interfaces.control_panel.handlers.alarm_handler import AlarmHandler


class PanelStub:
    def __init__(self):
        self.is_off = False
        self.current_state = "IDLE"
        self.next_response = {"success": True, "data": {"alarm_active": False}}
        self.sent_requests = []
        self.after_calls = []
        self.cancelled_jobs = []
        self.msg1 = None
        self.msg2 = None
        self.armed_led_states = []
        self.not_ready_states = []
        self.restored_states = []

    def send_request(self, action):
        self.sent_requests.append(action)
        if callable(self.next_response):
            return self.next_response()
        return self.next_response

    def after(self, delay, callback):
        self.after_calls.append((delay, callback))
        return len(self.after_calls)

    def after_cancel(self, job_id):
        self.cancelled_jobs.append(job_id)

    def set_display_short_message1(self, msg):
        self.msg1 = msg

    def set_display_short_message2(self, msg):
        self.msg2 = msg

    def set_armed_led(self, state):
        self.armed_led_states.append(state)

    def set_display_not_ready(self, state):
        self.not_ready_states.append(state)

    def restore_state(self, state):
        self.restored_states.append(state)


def _make_handler(panel=None):
    panel = panel or PanelStub()
    handler = AlarmHandler(panel)
    return handler, panel


def test_start_polling_triggers_alarm_and_schedules_job():
    handler, panel = _make_handler()
    panel.next_response = {
        "success": True,
        "data": {
            "alarm_active": True,
            "sensor_id": "S-1",
            "zone_name": "Garage Entry",
            "alarm_type": "FIRE",
        },
    }

    handler.start_polling()

    assert handler.is_active is True
    assert panel.msg1 == "!ALARM! FIRE"
    assert panel.msg2 == "S-1 @ Garage Entry"[:20]
    assert panel.armed_led_states[-1] is True
    assert panel.not_ready_states[-1] is True
    assert len(panel.after_calls) == 1


def test_stop_polling_cancels_job_and_resets_state():
    handler, panel = _make_handler()
    handler._poll_job = panel.after(1000, handler._poll)  # simulate scheduled job
    handler._alarm_active = True

    handler.stop_polling()

    assert handler.is_active is False
    assert panel.cancelled_jobs == [1]
    assert handler._poll_job is None


def test_poll_noop_when_panel_off():
    handler, panel = _make_handler()
    panel.is_off = True

    handler._poll()

    assert panel.sent_requests == []
    assert panel.after_calls == []


def test_poll_clears_alarm_when_condition_resolves():
    handler, panel = _make_handler()
    handler._alarm_active = True
    handler._previous_state = "AWAY"
    panel.next_response = {"success": True, "data": {"alarm_active": False}}

    handler._poll()

    assert handler.is_active is False
    assert panel.not_ready_states[-1] is False
    assert panel.restored_states == ["AWAY"]
    assert len(panel.after_calls) == 1


def test_handle_event_triggers_and_then_clears():
    handler, panel = _make_handler()
    data = {
        "alarm_active": True,
        "sensor_id": "PIR-7",
        "zone_name": "Living Room Very Long Name",
    }

    handler.handle_event(data)
    assert handler.is_active is True
    assert panel.msg1 == "!ALARM! INTRUSION"
    assert panel.msg2 == "PIR-7 @ Living Room "  # truncated to 20 chars

    handler.handle_event({"alarm_active": False})
    assert handler.is_active is False
    assert panel.not_ready_states[-1] is False
    assert panel.restored_states[-1] == "IDLE"

