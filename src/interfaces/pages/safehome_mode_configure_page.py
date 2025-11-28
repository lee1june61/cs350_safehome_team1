"""SafeHomeModeConfigurePage - Redefine security modes (SRS V.2.i)

Allows homeowner to configure which sensors are active in each mode:
- HOME: Perimeter sensors only
- AWAY: All sensors
- OVERNIGHT: All except motion sensors
- EXTENDED: All sensors
- GUEST: Same as HOME
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page
from ..components.floor_plan import FloorPlan


class SafeHomeModeConfigurePage(Page):
    """Configure which sensors are active in each SafeHome mode."""
    
    MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST']
    MODE_DESCRIPTIONS = {
        'HOME': 'At home - perimeter sensors only',
        'AWAY': 'Away from home - all sensors active',
        'OVERNIGHT': 'Overnight travel - all except motion',
        'EXTENDED': 'Extended travel - all sensors active',
        'GUEST': 'Guest at home - same as HOME'
    }
    
    def _build_ui(self):
        self._create_header("Configure Security Modes", back_page='security')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=15, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        
        # Left: Floor plan with selectable sensors
        left = ttk.LabelFrame(content, text="Floor Plan - Click sensors to toggle", padding=5)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._floorplan = FloorPlan(left, 400, 280, show_cameras=False, show_sensors=True)
        self._floorplan.create().pack(fill='both', expand=True)
        self._floorplan.set_on_click(self._on_sensor_click)
        
        # Selection info
        self._sel_info = ttk.Label(left, text="Active sensors: None", font=('Arial', 9))
        self._sel_info.pack(pady=(5, 0))
        
        # Right: Mode selection and sensor list
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky='nsew')
        
        # Mode selection
        mode_frame = ttk.LabelFrame(right, text="Select Mode to Configure", padding=5)
        mode_frame.pack(fill='x')
        
        self._mode_var = tk.StringVar(value='HOME')
        for mode in self.MODES:
            rb = ttk.Radiobutton(mode_frame, text=mode, variable=self._mode_var, 
                                  value=mode, command=self._load_mode)
            rb.pack(anchor='w', pady=1)
        
        # Mode description
        self._mode_desc = ttk.Label(mode_frame, text="", font=('Arial', 8), foreground='#666')
        self._mode_desc.pack(anchor='w', pady=(5, 0))
        
        # Sensor list for current mode
        sensor_frame = ttk.LabelFrame(right, text="Sensors in Mode", padding=5)
        sensor_frame.pack(fill='both', expand=True, pady=5)
        
        self._sensor_list = tk.Listbox(sensor_frame, height=6, font=('Arial', 9))
        self._sensor_list.pack(fill='both', expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(right)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Save Mode", command=self._save_mode, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Reset Mode", command=self._reset_mode, width=12).pack(side='left', padx=2)
        
        # Quick actions
        quick_frame = ttk.LabelFrame(right, text="Quick Actions", padding=5)
        quick_frame.pack(fill='x', pady=5)
        
        ttk.Button(quick_frame, text="Select All", command=self._select_all, width=12).pack(side='left', padx=2)
        ttk.Button(quick_frame, text="Clear All", command=self._clear_all, width=12).pack(side='left', padx=2)
        
        # State
        self._sensors = []
        self._selected_sensors = set()
        self._original_configs = {}

    def _on_sensor_click(self, dev_id: str, dev_type: str):
        """Handle sensor click to toggle selection."""
        if dev_type not in ('sensor', 'motion'):
            return
        
        if dev_id in self._selected_sensors:
            self._selected_sensors.discard(dev_id)
        else:
            self._selected_sensors.add(dev_id)
        
        self._update_display()

    def _load_sensors(self):
        """Load all sensors from system."""
        res = self.send_to_system('get_sensors')
        self._sensors = res.get('data', []) if res.get('success') else []

    def _load_mode(self):
        """Load sensor configuration for selected mode."""
        mode = self._mode_var.get()
        
        # Update description
        self._mode_desc.config(text=self.MODE_DESCRIPTIONS.get(mode, ''))
        
        # Get mode configuration from system
        res = self.send_to_system('get_mode_configuration', mode=mode)
        if res.get('success'):
            self._selected_sensors = set(res.get('data', []))
        else:
            self._selected_sensors = set()
        
        self._update_display()

    def _update_display(self):
        """Update floor plan and sensor list display."""
        # Update floor plan
        for s in self._sensors:
            self._floorplan.set_armed(s['id'], s['id'] in self._selected_sensors)
        self._floorplan.refresh()
        
        # Update sensor list
        self._sensor_list.delete(0, tk.END)
        for s in self._sensors:
            status = "✓" if s['id'] in self._selected_sensors else "○"
            self._sensor_list.insert(tk.END, f"{status} {s['id']}: {s['type']} @ {s['location']}")
        
        # Update selection info
        if self._selected_sensors:
            self._sel_info.config(text=f"Active sensors: {', '.join(sorted(self._selected_sensors))}")
        else:
            self._sel_info.config(text="Active sensors: None")

    def _select_all(self):
        """Select all sensors."""
        self._selected_sensors = {s['id'] for s in self._sensors}
        self._update_display()

    def _clear_all(self):
        """Clear all selections."""
        self._selected_sensors = set()
        self._update_display()

    def _save_mode(self):
        """Save current mode configuration."""
        mode = self._mode_var.get()
        sensors = list(self._selected_sensors)
        
        res = self.send_to_system('configure_safehome_mode', mode=mode, sensors=sensors)
        if res.get('success'):
            messagebox.showinfo("Success", f"Mode '{mode}' configuration saved\n"
                                           f"Active sensors: {len(sensors)}")
        else:
            messagebox.showerror("Error", res.get('message', 'Failed to save'))

    def _reset_mode(self):
        """Reset to original configuration."""
        if messagebox.askyesno("Confirm", "Reset to original configuration?"):
            self._load_mode()

    def on_show(self):
        """Called when page is shown."""
        self._load_sensors()
        self._load_mode()
