"""SafeHomeModeConfigurePage - Redefine security modes (SRS GUI)"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..components.page import Page


ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')


class SafeHomeModeConfigurePage(Page):
    """Redefine security modes - SRS 'Configure SafeHome modes'"""
    
    MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST']
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Redefine Security Modes", back_page='security')
        
        # Main content
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Left: Floor plan with sensors
        left_frame = ttk.LabelFrame(content, text="Floor Plan - Sensors", padding=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._canvas = tk.Canvas(left_frame, bg='white', width=400, height=350)
        self._canvas.pack(expand=True, fill='both')
        self._canvas.bind('<Button-1>', self._on_sensor_click)
        self._load_floorplan()
        
        # Right: Mode selection and sensor list
        right_frame = ttk.Frame(content)
        right_frame.grid(row=0, column=1, sticky='nsew')
        
        # Mode selection
        mode_frame = ttk.LabelFrame(right_frame, text="Select Mode to Configure", padding=10)
        mode_frame.pack(fill='x')
        
        self._mode_var = tk.StringVar(value='HOME')
        for mode in self.MODES:
            ttk.Radiobutton(mode_frame, text=mode, variable=self._mode_var,
                           value=mode, command=self._on_mode_change).pack(anchor='w')
        
        # Sensor list for selected mode
        sensor_frame = ttk.LabelFrame(right_frame, text="Sensors in Mode", padding=10)
        sensor_frame.pack(fill='both', expand=True, pady=10)
        
        self._sensor_list = tk.Listbox(sensor_frame, selectmode='multiple', height=8)
        self._sensor_list.pack(fill='both', expand=True)
        
        # Instructions
        ttk.Label(right_frame, text="Click sensors on floor plan\nor select from list",
                 foreground='gray').pack(pady=5)
        
        # Save button
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self._save, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self._cancel, width=12).pack(side='left', padx=5)
        
        # Sensor positions
        self._sensor_positions = {}
        self._selected_sensors = set()
    
    def _load_floorplan(self) -> None:
        try:
            path = os.path.join(ASSETS_DIR, 'floorplan.png')
            img = Image.open(path)
            img = img.resize((400, 350), Image.LANCZOS)
            self._floorplan_img = ImageTk.PhotoImage(img)
            self._canvas.create_image(0, 0, anchor='nw', image=self._floorplan_img)
        except Exception:
            self._canvas.create_rectangle(10, 10, 390, 340, outline='gray')
            self._canvas.create_text(200, 175, text="Floor Plan", fill='gray')
    
    def _load_sensors(self) -> None:
        """Load sensors from system"""
        self._sensor_list.delete(0, tk.END)
        
        response = self.send_to_system('get_sensors')
        if response.get('success'):
            sensors = response.get('data', [])
            self._sensors = sensors
            
            # Draw sensors on floor plan
            self._draw_sensors(sensors)
            
            # Populate list
            for sensor in sensors:
                self._sensor_list.insert(tk.END, 
                    f"{sensor['type']} - {sensor['location']}")
        else:
            self._sensors = []
    
    def _draw_sensors(self, sensors) -> None:
        """Draw sensor icons on floor plan"""
        self._canvas.delete('sensor')
        self._sensor_positions = {}
        
        # Predefined positions
        positions = {
            1: (80, 60), 2: (200, 100), 3: (320, 150),
            4: (100, 250), 5: (250, 280)
        }
        
        for sensor in sensors:
            sid = sensor['id']
            x, y = positions.get(sid, (50 + sid * 60, 200))
            
            # Color based on selection
            color = 'green' if sid in self._selected_sensors else 'gray'
            
            # Icon based on type
            icon = '🚪' if sensor['type'] == 'DOOR' else ('🪟' if sensor['type'] == 'WINDOW' else '👁')
            
            self._canvas.create_oval(x-12, y-12, x+12, y+12, fill=color, tags='sensor')
            self._canvas.create_text(x, y, text=icon, font=('Arial', 10), tags='sensor')
            
            self._sensor_positions[sid] = (x, y, sensor)
    
    def _on_sensor_click(self, event) -> None:
        """Toggle sensor selection on click"""
        for sid, (x, y, sensor) in self._sensor_positions.items():
            if abs(event.x - x) < 15 and abs(event.y - y) < 15:
                if sid in self._selected_sensors:
                    self._selected_sensors.remove(sid)
                else:
                    self._selected_sensors.add(sid)
                
                # Redraw and update list selection
                self._draw_sensors(self._sensors)
                self._update_list_selection()
                break
    
    def _update_list_selection(self) -> None:
        """Update listbox selection to match canvas selection"""
        self._sensor_list.selection_clear(0, tk.END)
        for i, sensor in enumerate(self._sensors):
            if sensor['id'] in self._selected_sensors:
                self._sensor_list.selection_set(i)
    
    def _on_mode_change(self) -> None:
        """Load sensors for selected mode"""
        mode = self._mode_var.get()
        
        response = self.send_to_system('get_mode_configuration', mode=mode)
        if response.get('success'):
            sensor_ids = response.get('data', [])
            self._selected_sensors = set(sensor_ids)
            self._draw_sensors(self._sensors)
            self._update_list_selection()
    
    def _save(self) -> None:
        mode = self._mode_var.get()
        sensor_ids = list(self._selected_sensors)
        
        response = self.send_to_system('configure_safehome_mode', 
                                       mode=mode, sensor_ids=sensor_ids)
        if response.get('success'):
            messagebox.showinfo("Success", f"Mode '{mode}' configuration saved")
        else:
            messagebox.showerror("Error", "Failed to save configuration")
    
    def _cancel(self) -> None:
        self.navigate_to('security')
    
    def on_show(self) -> None:
        self._load_sensors()
        self._on_mode_change()  # Load initial mode config
