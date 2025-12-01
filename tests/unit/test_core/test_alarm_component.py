"""
Additional unit tests for the core Alarm component to raise branch coverage.
"""

from src.core.alarm import Alarm


class TestAlarmComponent:
    """Exercise the lightweight Alarm state machine."""

    def test_alarm_initial_state(self):
        alarm = Alarm()

        assert alarm.get_state() == "INACTIVE"
        assert alarm.get_trigger_reason() is None
        assert alarm.is_active() is False

    def test_trigger_sets_state_and_reason(self):
        alarm = Alarm()

        alarm.trigger("WINDOW_OPEN")

        assert alarm.get_state() == "TRIGGERED"
        assert alarm.get_trigger_reason() == "WINDOW_OPEN"
        assert alarm.is_active() is True

    def test_sound_acknowledge_and_reset_flow(self):
        alarm = Alarm()

        alarm.trigger("MOTION")
        alarm.sound()
        assert alarm.get_state() == "SOUNDING"
        assert alarm.is_active() is True

        alarm.acknowledge()
        assert alarm.get_state() == "ACKNOWLEDGED"
        assert alarm.is_active() is False

        alarm.reset()
        assert alarm.get_state() == "INACTIVE"
        assert alarm.get_trigger_reason() is None



