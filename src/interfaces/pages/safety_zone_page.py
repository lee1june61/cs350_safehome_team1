"""SafetyZonePage - Safety zone management with floor plan interaction (SRS V.2.c-h)

Features:
- View safety zones on floor plan
- Create/Update/Delete zones
- Select sensors on floor plan to add to zones
- Arm/Disarm individual zones selectively
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ..components.page import Page
from ..components.floor_plan import FloorPlan


class SafetyZonePage(Page):
    """Safety Zone management with floorplan display and sensor selection."""
    
    def _build_ui(self):
        self._create_header("Safety Zone Management", back_page='security')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=15, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        
        # Left: Floor plan with sensors
        left = ttk.LabelFrame(content, text="Floor Plan - Click sensors to select", padding=5)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._floorplan = FloorPlan(left, 420, 280, show_cameras=False, show_sensors=True)
        self._floorplan.create().pack(fill='both', expand=True)
        self._floorplan.set_on_sensor_click(self._on_sensor_selected)
        self._floorplan.set_on_click(self._on_device_click)
        
        # Selection info
        self._sel_info = ttk.Label(left, text="Selected sensors: None", font=('Arial', 9))
        self._sel_info.pack(pady=(5, 0))
        
        # Right: Zone list and controls
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky='nsew')
        
        # Zone list
        zone_frame = ttk.LabelFrame(right, text="Safety Zones", padding=5)
        zone_frame.pack(fill='both', expand=True)
        
        self._zone_list = tk.Listbox(zone_frame, height=8, font=('Arial', 10), selectmode='single')
        self._zone_list.pack(fill='both', expand=True)
        self._zone_list.bind('<<ListboxSelect>>', self._on_zone_select)
        
        self._status_label = ttk.Label(zone_frame, text="", font=('Arial', 9))
        self._status_label.pack(pady=3)
        
        # Arm/Disarm buttons
        arm_frame = ttk.Frame(right)
        arm_frame.pack(fill='x', pady=5)
        ttk.Button(arm_frame, text="🔴 Arm Zone", command=self._arm_zone, width=12).pack(side='left', padx=2)
        ttk.Button(arm_frame, text="⚪ Disarm Zone", command=self._disarm_zone, width=12).pack(side='left', padx=2)
        
        # Zone management buttons
        manage_frame = ttk.LabelFrame(right, text="Manage Zones", padding=5)
        manage_frame.pack(fill='x', pady=5)
        
        btn_row1 = ttk.Frame(manage_frame)
        btn_row1.pack(fill='x', pady=2)
        ttk.Button(btn_row1, text="Create Zone", command=self._create_zone, width=12).pack(side='left', padx=2)
        ttk.Button(btn_row1, text="Delete Zone", command=self._delete_zone, width=12).pack(side='left', padx=2)
        
        btn_row2 = ttk.Frame(manage_frame)
        btn_row2.pack(fill='x', pady=2)
        ttk.Button(btn_row2, text="Edit Sensors", command=self._start_edit_sensors, width=12).pack(side='left', padx=2)
        ttk.Button(btn_row2, text="Save Changes", command=self._save_zone_sensors, width=12).pack(side='left', padx=2)
        
        # Help text
        help_text = "• Select a zone, then click sensors on floor plan to add/remove\n• Green = Armed, Orange = Selected"
        ttk.Label(right, text=help_text, font=('Arial', 8), foreground='#666').pack(pady=5)
        
        # State
        self._zones = []
        self._editing_zone = None

    def _load_zones(self):
        """Load zones from system and update display."""
        self._zone_list.delete(0, tk.END)
        res = self.send_to_system('get_safety_zones')
        self._zones = res.get('data', []) if res.get('success') else []
        
        for z in self._zones:
            status = '🔴' if z.get('armed') else '⚪'
            self._zone_list.insert(tk.END, f"{status} {z['name']} ({len(z.get('sensors', []))} sensors)")
        
        self._update_floorplan_states()

    def _update_floorplan_states(self):
        """Update floor plan to show armed sensors."""
        # Get all armed sensors
        armed_sensors = set()
        for z in self._zones:
            if z.get('armed'):
                armed_sensors.update(z.get('sensors', []))
        
        # Update floor plan
        for sensor_id in self._floorplan.get_sensors():
            self._floorplan.set_armed(sensor_id, sensor_id in armed_sensors)
        self._floorplan.refresh()

    def _get_selected_zone(self):
        """Get currently selected zone."""
        sel = self._zone_list.curselection()
        if sel and sel[0] < len(self._zones):
            return self._zones[sel[0]]
        return None

    def _on_zone_select(self, event):
        """Handle zone selection in list."""
        zone = self._get_selected_zone()
        if zone:
            sensors = zone.get('sensors', [])
            armed = 'Armed' if zone.get('armed') else 'Disarmed'
            self._status_label.config(text=f"{zone['name']}: {armed}")
            # Highlight zone's sensors on floor plan
            self._floorplan.set_selected(sensors)
            self._update_selection_info()
        else:
            self._floorplan.clear_selection()
            self._update_selection_info()

    def _on_sensor_selected(self, sensor_id: str, dtype: str, is_selected: bool):
        """Handle sensor click in select mode."""
        self._update_selection_info()

    def _on_device_click(self, dev_id: str, dtype: str):
        """Handle device click (non-select mode)."""
        if dtype in ('sensor', 'motion'):
            # Show sensor info
            res = self.send_to_system('get_sensors')
            if res.get('success'):
                for s in res.get('data', []):
                    if s['id'] == dev_id:
                        armed = 'Armed' if s.get('armed') else 'Disarmed'
                        messagebox.showinfo("Sensor Info", 
                            f"ID: {dev_id}\nType: {s.get('type', 'Unknown')}\n"
                            f"Location: {s.get('location', 'Unknown')}\nStatus: {armed}")
                        return

    def _update_selection_info(self):
        """Update selection info label."""
        selected = self._floorplan.get_selected()
        if selected:
            self._sel_info.config(text=f"Selected sensors: {', '.join(sorted(selected))}")
        else:
            self._sel_info.config(text="Selected sensors: None")

    def _arm_zone(self):
        """Arm selected zone."""
        zone = self._get_selected_zone()
        if not zone:
            messagebox.showwarning("Warning", "Please select a zone first")
            return
        
        res = self.send_to_system('arm_zone', zone_id=zone['id'])
        if res.get('success'):
            self._load_zones()
            messagebox.showinfo("Success", f"Zone '{zone['name']}' armed")
        else:
            messagebox.showerror("Error", res.get('message', 'Failed to arm zone'))

    def _disarm_zone(self):
        """Disarm selected zone."""
        zone = self._get_selected_zone()
        if not zone:
            messagebox.showwarning("Warning", "Please select a zone first")
            return
        
        res = self.send_to_system('disarm_zone', zone_id=zone['id'])
        if res.get('success'):
            self._load_zones()
            messagebox.showinfo("Success", f"Zone '{zone['name']}' disarmed")
        else:
            messagebox.showerror("Error", res.get('message', 'Failed to disarm zone'))

    def _create_zone(self):
        """Create new safety zone - SRS V.2.f."""
        name = simpledialog.askstring("Create Zone", "Enter zone name:")
        if not name or not name.strip():
            return
        
        # Enable sensor selection mode
        self._floorplan.set_select_mode(True)
        self._floorplan.clear_selection()
        
        messagebox.showinfo("Create Zone", 
            "Click sensors on the floor plan to add them to this zone.\n"
            "Click 'Save Changes' when done.")
        
        # Create zone with no sensors initially
        res = self.send_to_system('create_safety_zone', name=name.strip(), sensors=[])
        if res.get('success'):
            self._load_zones()
            # Select the new zone
            self._zone_list.selection_set(len(self._zones) - 1)
            self._editing_zone = res.get('zone_id')
            self._on_zone_select(None)

    def _start_edit_sensors(self):
        """Start editing sensors for selected zone."""
        zone = self._get_selected_zone()
        if not zone:
            messagebox.showwarning("Warning", "Please select a zone first")
            return
        
        # Enable selection mode and show current sensors
        self._floorplan.set_select_mode(True)
        self._floorplan.set_selected(zone.get('sensors', []))
        self._editing_zone = zone['id']
        self._update_selection_info()
        
        messagebox.showinfo("Edit Zone", 
            f"Editing zone '{zone['name']}'.\n"
            "Click sensors to add/remove them.\n"
            "Click 'Save Changes' when done.")

    def _save_zone_sensors(self):
        """Save sensor changes to zone."""
        if not self._editing_zone:
            messagebox.showwarning("Warning", "No zone being edited")
            return
        
        selected = self._floorplan.get_selected()
        if not selected:
            if not messagebox.askyesno("Confirm", "No sensors selected. Save empty zone?"):
                return
        
        res = self.send_to_system('update_safety_zone', 
                                   zone_id=self._editing_zone, 
                                   sensors=selected)
        if res.get('success'):
            messagebox.showinfo("Success", "Zone sensors updated")
            self._editing_zone = None
            self._floorplan.set_select_mode(False)
            self._load_zones()
        else:
            messagebox.showerror("Error", res.get('message', 'Failed to update zone'))

    def _delete_zone(self):
        """Delete selected zone - SRS V.2.g."""
        zone = self._get_selected_zone()
        if not zone:
            messagebox.showwarning("Warning", "Please select a zone first")
            return
        
        if not messagebox.askyesno("Confirm Delete", f"Delete zone '{zone['name']}'?"):
            return
        
        res = self.send_to_system('delete_safety_zone', zone_id=zone['id'])
        if res.get('success'):
            self._editing_zone = None
            self._floorplan.clear_selection()
            self._load_zones()
        else:
            messagebox.showerror("Error", res.get('message', 'Failed to delete zone'))

    def on_show(self):
        """Called when page is shown."""
        self._editing_zone = None
        self._floorplan.set_select_mode(False)
        self._load_zones()
