"""ZoneDialog - Safety zone create/update dialog"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from .base_dialog import BaseDialog


class ZoneDialog(BaseDialog):
    """Dialog for creating or updating safety zones"""
    
    def __init__(self, parent: tk.Widget, web_interface, mode: str = 'create', 
                 zone_data: Optional[Dict] = None):
        title = 'Create Zone' if mode == 'create' else 'Update Zone'
        super().__init__(parent, title, 500, 450)
        
        self._web_interface = web_interface
        self._mode = mode
        self._zone_data = zone_data
        self._sensors = []
        
        self._build_ui()
        self._load_sensors()
        if zone_data:
            self._load_zone()
    
    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Zone Name:").pack(anchor='w')
        self._name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self._name_var, width=40).pack(pady=(5, 15))
        
        ttk.Label(frame, text="Select Sensors:").pack(anchor='w')
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill='both', expand=True, pady=(5, 15))
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self._listbox = tk.Listbox(list_frame, selectmode='multiple', 
                                   yscrollcommand=scrollbar.set, height=10)
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text='Create' if self._mode == 'create' else 'Update', 
                  command=self._save, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self._on_cancel, width=12).pack(side='left', padx=5)
    
    def _load_sensors(self) -> None:
        response = self._web_interface.send_message('get_sensors')
        if response.get('success'):
            self._sensors = response.get('data', [])
            for sensor in self._sensors:
                self._listbox.insert(tk.END, f"{sensor['name']} ({sensor['type']})")
    
    def _load_zone(self) -> None:
        self._name_var.set(self._zone_data.get('name', ''))
        zone_sensor_ids = self._zone_data.get('sensor_ids', [])
        for i, sensor in enumerate(self._sensors):
            if sensor['id'] in zone_sensor_ids:
                self._listbox.selection_set(i)
    
    def _save(self) -> None:
        name = self._name_var.get().strip()
        if not name:
            return self._show_error("Zone name required")
        
        selected = self._listbox.curselection()
        if not selected:
            return self._show_error("Select at least one sensor")
        
        sensor_ids = [self._sensors[i]['id'] for i in selected]
        
        if self._mode == 'create':
            response = self._web_interface.send_message('create_safety_zone', 
                                                        zone_name=name, sensor_ids=sensor_ids)
        else:
            response = self._web_interface.send_message('update_safety_zone',
                                                        zone_id=self._zone_data['id'],
                                                        zone_name=name, sensor_ids=sensor_ids)
        
        if response.get('success'):
            self._show_info(response.get('message', 'Success'))
            self._on_ok()
        else:
            self._show_error(response.get('message', 'Failed'))
