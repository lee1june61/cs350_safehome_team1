"""
Unit tests for the web login page LoginManager.
"""

from src.interfaces.pages.login_page.login_manager import LoginManager


class VarStub:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class WidgetStub:
    def __init__(self):
        self.props = {}

    def config(self, **kwargs):
        self.props.update(kwargs)


class FrameStub:
    def __init__(self):
        self.scheduled = []
        self.canceled = []

    def after(self, delay, callback):
        self.scheduled.append((delay, callback))
        return f"job-{len(self.scheduled)}"

    def after_cancel(self, job_id):
        self.canceled.append(job_id)


class PageStub:
    def __init__(self):
        self.sent = []
        self.context = {}
        self.navigated = None
        self._frame = FrameStub()
        self._web_interface = self

    def send_to_system(self, action, **payload):
        self.sent.append((action, payload))
        return self.next_response

    def set_context(self, key, value):
        self.context[key] = value

    def navigate_to(self, target):
        self.navigated = target


class GuardStub:
    def __init__(self):
        self.locked = False
        self.failure_returns = []
        self.reset_calls = 0
        self.start_args = None
        self.remaining = 2

    def is_locked(self):
        return self.locked

    def record_failure(self):
        if self.failure_returns:
            return self.failure_returns.pop(0)
        return False

    def remaining_attempts(self):
        return self.remaining

    def reset_attempts(self):
        self.reset_calls += 1

    def start_countdown(self, scheduler, tick_fn, unlock_fn):
        self.start_args = (scheduler, tick_fn, unlock_fn)


class TestLoginPageLoginManager:
    def _manager(self):
        page = PageStub()
        manager = LoginManager(
            page,
            VarStub("user"),
            VarStub("pw1"),
            VarStub("pw2"),
            WidgetStub(),
            WidgetStub(),
        )
        manager._guard = GuardStub()
        return manager, page

    def test_login_exits_when_locked(self):
        manager, page = self._manager()
        manager._guard.locked = True

        manager.login()

        assert page.sent == []

    def test_login_validates_fields(self):
        manager, page = self._manager()
        manager._user_var.set("")

        manager.login()

        assert page.sent == []
        assert manager._status_msg.props["text"] == "Fill all fields"

    def test_login_success_flow(self):
        manager, page = self._manager()
        page.next_response = {"success": True}

        manager.login()

        assert manager._user_var.get() == ""
        assert page.context["user_id"] == "user"
        assert page.navigated == "major_function"
        assert manager._guard.reset_calls == 1

    def test_login_failure_paths(self):
        manager, page = self._manager()
        page.next_response = {"success": False}
        manager._guard.failure_returns = [False]

        manager.login()

        assert "Failed." in manager._status_msg.props["text"]

        manager._guard.failure_returns = [True]
        manager.login()

        assert manager._login_btn.props["state"] == "disabled"
        assert manager._guard.start_args is not None

    def test_unlock_and_schedule(self):
        manager, page = self._manager()
        manager._login_btn.config(state="disabled")

        manager._unlock()

        assert manager._login_btn.props["state"] == "normal"
        assert manager._status_msg.props["text"] == "Unlocked"

        job_id = manager._schedule(100, lambda: None)
        assert job_id is not None
        manager._schedule("cancel", job_id)
        assert page._frame.canceled == [job_id]

    def test_on_show_resets_state(self):
        manager, page = self._manager()
        manager._login_btn.config(state="disabled")
        manager._status_msg.config(text="Locked")

        manager.on_show()

        assert manager._login_btn.props["state"] == "normal"
        assert manager._status_msg.props["text"] == ""
        assert manager._guard.reset_calls == 1

