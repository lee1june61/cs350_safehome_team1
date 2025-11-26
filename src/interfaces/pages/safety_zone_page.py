"""SafetyZonePage - Safety zone management"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page
from ..components.floor_plan import FloorPlan


class SafetyZonePage(Page):
    """Safety zone management page"""
    
    def _build_ui(self) -> None:
        self._create_header("Safety Zones", back_page='security')
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Zone list
        left = ttk.LabelFrame(content, text="Zones", padding=10)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        list_frame = ttk.Frame(left)
        list_frame.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self._listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)
        self._listbox.bind('<<ListboxSelect>>', self._on_select)
        
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="Arm", command=self._arm_zone, width=10).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Disarm", command=self._disarm_zone, width=10).pack(side='left', padx=2)
        
        # Floor plan and actions
        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        plan_frame = ttk.LabelFrame(right, text="Floor Plan", padding=10)
        plan_frame.pack(fill='both', expand=True, pady=(0, 10))
        self._floor_plan = FloorPlan(plan_frame, 300, 200)
        self._floor_plan.create_canvas().pack()
        
        action_frame = ttk.LabelFrame(right, text="Zone Management", padding=10)
        action_frame.pack(fill='x')
        for text, cmd in [("Create", self._create), ("Update", self._update), ("Delete", self._delete)]:
            ttk.Button(action_frame, text=text, command=cmd, width=12).pack(side='left', padx=5)
        
        self._zones = []
    
    def _load_zones(self) -> None:
        self._listbox.delete(0, tk.END)
        response = self.send_to_system('get_safety_zones')
        if response.get('success'):
            self._zones = response.get('data', [])
            for zone in self._zones:
                status = "🟢" if zone.get('armed') else "⚪"
                self._listbox.insert(tk.END, f"{status} {zone['name']}")
    
    def _on_select(self, event) -> None:
        sel = self._listbox.curselection()
        if sel and self._zones:
            zone = self._zones[sel[0]]
            self._floor_plan.highlight_devices(zone.get('sensor_ids', []))
    
    def _arm_zone(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return self._show_message("Info", "Select a zone first", 'warning')
        zone = self._zones[sel[0]]
        response = self.send_to_system('arm_safety_zone', zone_id=zone['id'])
        if response.get('success'):
            self._show_message("Success", f"Zone '{zone['name']}' armed")
            self._load_zones()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def _disarm_zone(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return self._show_message("Info", "Select a zone first", 'warning')
        zone = self._zones[sel[0]]
        response = self.send_to_system('disarm_safety_zone', zone_id=zone['id'])
        if response.get('success'):
            self._show_message("Success", f"Zone '{zone['name']}' disarmed")
            self._load_zones()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def _create(self) -> None:
        from .dialogs.zone_dialog import ZoneDialog
        ZoneDialog(self._frame.winfo_toplevel(), self._web_interface, 'create').show()
        self._load_zones()
    
    def _update(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return self._show_message("Info", "Select a zone first", 'warning')
        from .dialogs.zone_dialog import ZoneDialog
        ZoneDialog(self._frame.winfo_toplevel(), self._web_interface, 
                  'update', self._zones[sel[0]]).show()
        self._load_zones()
    
    def _delete(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return self._show_message("Info", "Select a zone first", 'warning')
        zone = self._zones[sel[0]]
        if not self._ask_confirm("Delete", f"Delete zone '{zone['name']}'?"):
            return
        response = self.send_to_system('delete_safety_zone', zone_id=zone['id'])
        if response.get('success'):
            self._show_message("Success", "Zone deleted")
            self._load_zones()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        self._load_zones()
        response = self.send_to_system('get_sensors')
        if response.get('success'):
            self._floor_plan.load_devices_from_list(response.get('data', []))
