from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.interfaces.pages.safety_zone_page import zone_manager as zone_manager_module
from src.interfaces.pages.safety_zone_page.zone_manager import ZoneManager


class DummyListbox:
    def __init__(self):
        self._selection = ()
        self.cleared = None
        self.set_calls = []

    def curselection(self):
        return self._selection

    def selection_clear(self, start, end):
        self.cleared = (start, end)

    def selection_set(self, idx):
        self.set_calls.append(idx)
        self._selection = (idx,)

    def set_selection(self, idx=None):
        if idx is None:
            self._selection = ()
        else:
            self._selection = (idx,)


class DummyUpdater:
    def __init__(self, zone_list):
        self.zone_list = zone_list
        self.update_zone_list = MagicMock()
        self.display_selected_zone_info = MagicMock()
        self.clear_all_display = MagicMock()
        self.update_selection_info = MagicMock()


class PageStub:
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.calls = []

    def send_to_system(self, action):
        self.calls.append(action)
        response = self.responses.get(action, {"success": True, "data": []})
        return response() if callable(response) else response


@pytest.fixture
def manager_factory(monkeypatch):
    def _create(page=None):
        zone_list = DummyListbox()
        fake_updater = DummyUpdater(zone_list)
        fake_selection = SimpleNamespace(
            cancel_creation=MagicMock(),
            reset=MagicMock(),
            update_dialog=MagicMock(),
        )
        fake_action = SimpleNamespace(
            set_armed_state=MagicMock(),
            create_zone=MagicMock(),
            start_edit_sensors=MagicMock(),
            save_zone_sensors=MagicMock(),
            delete_zone=MagicMock(),
        )
        monkeypatch.setattr(
            zone_manager_module, "ZoneUIUpdater", lambda *args, **kwargs: fake_updater
        )
        monkeypatch.setattr(
            zone_manager_module,
            "ZoneSelectionSession",
            lambda *args, **kwargs: fake_selection,
        )
        monkeypatch.setattr(
            zone_manager_module, "ZoneActionHandler", lambda *args, **kwargs: fake_action
        )
        if page is None:
            page = PageStub()
        manager = ZoneManager(page, object(), zone_list, object(), object())
        context = SimpleNamespace(
            ui=fake_updater,
            selection=fake_selection,
            action=fake_action,
            zone_list=zone_list,
            page=page,
        )
        return manager, context

    return _create


@pytest.fixture(autouse=True)
def mock_showinfo(monkeypatch):
    showinfo = MagicMock()
    monkeypatch.setattr(zone_manager_module.messagebox, "showinfo", showinfo)
    return showinfo


def test_load_zones_success_updates_zone_list_and_cache(manager_factory):
    responses = {
        "get_sensors": {"success": True, "data": [{"id": "S1", "armed": True}]},
        "get_safety_zones": {"success": True, "data": [{"id": 5, "name": "Front"}]},
    }
    manager, ctx = manager_factory(page=PageStub(responses))

    manager.load_zones()

    assert manager.zones == responses["get_safety_zones"]["data"]
    assert manager._sensor_cache == responses["get_sensors"]["data"]
    ctx.ui.update_zone_list.assert_called_once_with(
        responses["get_safety_zones"]["data"]
    )
    assert ctx.page.calls == ["get_sensors", "get_safety_zones"]


def test_load_zones_failure_clears_data(manager_factory):
    responses = {
        "get_sensors": {"success": False},
        "get_safety_zones": {"success": False},
    }
    manager, ctx = manager_factory(page=PageStub(responses))

    manager.load_zones()

    assert manager.zones == []
    assert manager._sensor_cache == []
    ctx.ui.update_zone_list.assert_called_once_with([])


def test_get_selected_zone_returns_match(manager_factory):
    manager, ctx = manager_factory()
    manager.zones = [{"id": 1}, {"id": 2}]
    ctx.zone_list.set_selection(1)

    assert manager.get_selected_zone() == {"id": 2}


def test_get_selected_zone_handles_invalid_selection(manager_factory):
    manager, ctx = manager_factory()
    manager.zones = [{"id": 1}]
    ctx.zone_list.set_selection(5)

    assert manager.get_selected_zone() is None


def test_on_zone_select_displays_info(manager_factory):
    manager, ctx = manager_factory()
    manager.zones = [{"id": 1, "name": "Hall"}]
    ctx.zone_list.set_selection(0)

    manager.on_zone_select(None)

    ctx.selection.cancel_creation.assert_called_once()
    ctx.ui.display_selected_zone_info.assert_called_once_with({"id": 1, "name": "Hall"})


def test_on_zone_select_clears_display_when_no_zone(manager_factory):
    manager, ctx = manager_factory()
    ctx.zone_list.set_selection(None)

    manager.on_zone_select(None)

    ctx.ui.clear_all_display.assert_called_once()


def test_select_zone_updates_list_and_triggers_callback(manager_factory):
    manager, ctx = manager_factory()
    manager.zones = [{"id": 55}, {"id": 77}]
    manager.on_zone_select = MagicMock()

    manager.select_zone(77)

    assert ctx.zone_list.cleared == (0, zone_manager_module.tk.END)
    assert ctx.zone_list.set_calls[-1] == 1
    manager.on_zone_select.assert_called_once_with(None)


def test_select_zone_ignores_missing_ids(manager_factory):
    manager, ctx = manager_factory()
    manager.zones = [{"id": 55}]

    manager.select_zone(999)
    assert ctx.zone_list.cleared is None

    manager.select_zone(None)
    assert ctx.zone_list.cleared is None


def test_handle_device_click_info_filters_non_sensors(manager_factory, mock_showinfo):
    manager, _ = manager_factory()

    manager.handle_device_click_info("CAM1", "camera")

    mock_showinfo.assert_not_called()


def test_handle_device_click_info_refreshes_cache(manager_factory):
    manager, _ = manager_factory()
    manager._sensor_cache = []
    manager._refresh_sensor_cache = MagicMock()

    manager.handle_device_click_info("S1", "sensor")

    manager._refresh_sensor_cache.assert_called_once()


def test_handle_device_click_info_shows_message_for_known_sensor(
    manager_factory, mock_showinfo
):
    manager, _ = manager_factory()
    manager._sensor_cache = [
        {
            "id": "S1",
            "type": "door",
            "location": "Back",
            "armed": False,
        }
    ]

    manager.handle_device_click_info("S1", "sensor")

    mock_showinfo.assert_called_once()
    _, body = mock_showinfo.call_args[0]
    assert "ID: S1" in body
    assert "Location: Back" in body
    assert "Status: Disarmed" in body


def test_on_sensor_selected_updates_ui_and_dialog(manager_factory):
    manager, ctx = manager_factory()

    manager.on_sensor_selected("S1", "sensor", True)

    ctx.ui.update_selection_info.assert_called_once()
    ctx.selection.update_dialog.assert_called_once()


def test_on_show_resets_selection_and_clears_ui(manager_factory):
    manager, ctx = manager_factory()
    manager.load_zones = MagicMock()

    manager.on_show()

    ctx.selection.reset.assert_called_once()
    manager.load_zones.assert_called_once()
    ctx.ui.clear_all_display.assert_called_once()


def test_action_shortcuts_delegate_to_handler(manager_factory):
    manager, ctx = manager_factory()

    manager.arm_zone()
    manager.disarm_zone()
    manager.create_zone()
    manager.start_edit_sensors()
    manager.save_zone_sensors()
    manager.delete_zone()

    ctx.action.set_armed_state.assert_any_call(True)
    ctx.action.set_armed_state.assert_any_call(False)
    ctx.action.create_zone.assert_called_once()
    ctx.action.start_edit_sensors.assert_called_once()
    ctx.action.save_zone_sensors.assert_called_once()
    ctx.action.delete_zone.assert_called_once()


