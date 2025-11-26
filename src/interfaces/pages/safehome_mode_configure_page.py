"""SafeHomeModeConfigurePage - Configure sensors for each mode"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SafeHomeModeConfigurePage(Page):
    """Page for configuring SafeHome mode sensor assignments"""
    
    MODES = ['HOME', 'AWAY', 'NIGHT', 'EXTENDED', 'GUEST']
    
    def _build_ui(self) -> None:
        self._create_header("Configure Modes", back_page='security')
        
        mode_frame = ttk.Frame(self._frame)
        mode_frame.pack(fill='x', padx=20, pady=(0, 10))
        ttk.Label(mode_frame, text="Mode:").pack(side='left')
        self._mode_var = tk.StringVar(value='HOME')
        combo = ttk.Combobox(mode_frame, textvariable=self._mode_var,
                            values=self.MODES, state='readonly', width=15)
        combo.pack(side='left', padx=(10, 0))
        combo.bind('<<ComboboxSelected>>', lambda e: self._load_mode())
        
        sensor_frame = ttk.LabelFrame(self._frame, text="Sensors in this Mode", padding=10)
        sensor_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        list_frame = ttk.Frame(sensor_frame)
        list_frame.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self._listbox = tk.Listbox(list_frame, selectmode='multiple', 
                                   yscrollcommand=scrollbar.set, height=12)
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)
        
        ttk.Button(self._frame, text="Save Configuration", 
                  command=self._save, width=20).pack(pady=(0, 20))
        
        self._sensors = []
    
    def _load_sensors(self) -> None:
        response = self.send_to_system('get_sensors')
        if response.get('success'):
            self._sensors = response.get('data', [])
            self._listbox.delete(0, tk.END)
            for sensor in self._sensors:
                self._listbox.insert(tk.END, f"{sensor['name']} ({sensor['type']})")
    
    def _load_mode(self) -> None:
        response = self.send_to_system('get_mode_info', mode_name=self._mode_var.get())
        if response.get('success'):
            sensor_ids = response.get('data', {}).get('sensor_ids', [])
            self._listbox.selection_clear(0, tk.END)
            for i, sensor in enumerate(self._sensors):
                if sensor['id'] in sensor_ids:
                    self._listbox.selection_set(i)
    
    def _save(self) -> None:
        selected = self._listbox.curselection()
        sensor_ids = [self._sensors[i]['id'] for i in selected]
        response = self.send_to_system('configure_safehome_mode', 
                                       mode_name=self._mode_var.get(), sensor_ids=sensor_ids)
        if response.get('success'):
            self._show_message("Success", f"Mode '{self._mode_var.get()}' configured")
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        self._load_sensors()
        self._load_mode()
