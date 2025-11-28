"""
FloorPlanController - Manages the state and interaction logic for the FloorPlan component.
"""
from typing import Dict, Optional, Callable, Set, List, Any

# This will eventually hold references to the actual UI elements if needed,
# but primarily manages the data state and delegates UI updates.
class FloorPlanController:
    def __init__(self,
                 on_click: Optional[Callable[[str, str], None]] = None,
                 on_sensor_click: Optional[Callable[[str, str, bool], None]] = None):
        
        self._on_click = on_click
        self._on_sensor_click = on_sensor_click
        
        self._states: Dict[str, bool] = {}  # armed state
        self._selected: Set[str] = set()    # selected sensors for zone editing
        
        self._select_mode = False
        
        # Reference to the FloorPlan component for refreshing its UI
        self._floor_plan_refresh_callback: Optional[Callable[[], None]] = None

    def set_refresh_callback(self, callback: Callable[[], None]):
        self._floor_plan_refresh_callback = callback

    def _refresh_floor_plan(self):
        if self._floor_plan_refresh_callback:
            self._floor_plan_refresh_callback()

    def handle_device_click(self, dev_id: str, dtype: str):
        """Handle device click, delegating to appropriate callbacks and updating state."""
        if self._select_mode and dtype in ('sensor', 'motion'):
            if dev_id in self._selected:
                self._selected.discard(dev_id)
            else:
                self._selected.add(dev_id)
            self._refresh_floor_plan() # Request UI refresh
            if self._on_sensor_click:
                self._on_sensor_click(dev_id, dtype, dev_id in self._selected)
        elif self._on_click:
            self._on_click(dev_id, dtype)

    # Configuration and State Management
    def set_on_click_handler(self, handler: Callable[[str, str], None]):
        self._on_click = handler

    def set_on_sensor_click_handler(self, handler: Callable[[str, str, bool], None]):
        self._on_sensor_click = handler

    def set_select_mode(self, enabled: bool):
        self._select_mode = enabled
        if not enabled:
            self._selected.clear()
        self._refresh_floor_plan() # Request UI refresh

    def set_armed_state(self, device_id: str, armed: bool):
        self._states[device_id] = armed
        self._refresh_floor_plan() # Request UI refresh

    def get_armed_states(self) -> Dict[str, bool]:
        return self._states

    def set_selected_devices(self, device_ids: List[str]):
        self._selected = set(device_ids)
        self._refresh_floor_plan() # Request UI refresh

    def get_selected_devices(self) -> List[str]:
        return list(self._selected)

    def clear_selection(self):
        self._selected.clear()
        self._refresh_floor_plan() # Request UI refresh

    def get_is_select_mode(self) -> bool:
        return self._select_mode

