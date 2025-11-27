"""SafetyZonePage - Safety zone management with floorplan (SRS GUI)"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..components.page import Page


ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')


class SafetyZonePage(Page):
    """Safety Zone page - SRS Section II 'Security Function - Safety zone'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Safety Zone", back_page='security')
        
        # Main content
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Left: Floor plan
        left_frame = ttk.LabelFrame(content, text="Floor Plan", padding=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10), pady=5)
        
        self._canvas = tk.Canvas(left_frame, bg='white', width=400, height=350)
        self._canvas.pack(expand=True, fill='both')
        self._load_floorplan()
        
        # Right: Zone list and controls
        right_frame = ttk.Frame(content)
        right_frame.grid(row=0, column=1, sticky='nsew', pady=5)
        
        # Zone list
        list_frame = ttk.LabelFrame(right_frame, text="Safety Zones", padding=10)
        list_frame.pack(fill='both', expand=True)
        
        self._zone_list = tk.Listbox(list_frame, height=10, font=('Arial', 11))
        self._zone_list.pack(fill='both', expand=True, pady=(0, 10))
        self._zone_list.bind('<<ListboxSelect>>', self._on_zone_select)
        
        # Zone status
        self._zone_status = ttk.Label(list_frame, text="Select a zone", font=('Arial', 10))
        self._zone_status.pack(pady=5)
        
        # Control buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=10)
        
        self._btn_arm = ttk.Button(btn_frame, text="Arm Zone", command=self._arm_zone, width=15)
        self._btn_arm.pack(side='left', padx=5)
        
        self._btn_disarm = ttk.Button(btn_frame, text="Disarm Zone", command=self._disarm_zone, width=15)
        self._btn_disarm.pack(side='left', padx=5)
        
        # Zone management buttons
        mgmt_frame = ttk.LabelFrame(right_frame, text="Zone Management", padding=10)
        mgmt_frame.pack(fill='x', pady=10)
        
        ttk.Button(mgmt_frame, text="Create Zone", command=self._create_zone, width=15).pack(pady=3)
        ttk.Button(mgmt_frame, text="Update Zone", command=self._update_zone, width=15).pack(pady=3)
        ttk.Button(mgmt_frame, text="Delete Zone", command=self._delete_zone, width=15).pack(pady=3)
    
    def _load_floorplan(self) -> None:
        """Load floorplan.png from assets"""
        try:
            path = os.path.join(ASSETS_DIR, 'floorplan.png')
            img = Image.open(path)
            img = img.resize((400, 350), Image.LANCZOS)
            self._floorplan_img = ImageTk.PhotoImage(img)
            self._canvas.create_image(0, 0, anchor='nw', image=self._floorplan_img)
        except Exception as e:
            # Draw placeholder if image not found
            self._canvas.create_rectangle(10, 10, 390, 340, outline='gray')
            self._canvas.create_text(200, 175, text="Floor Plan\n(floorplan.png)", 
                                    font=('Arial', 14), fill='gray')
    
    def _load_zones(self) -> None:
        """Load safety zones from system"""
        self._zone_list.delete(0, tk.END)
        response = self.send_to_system('get_safety_zones')
        
        if response.get('success'):
            zones = response.get('data', [])
            for zone in zones:
                status = "🔴" if zone.get('armed') else "⚪"
                self._zone_list.insert(tk.END, f"{status} {zone['name']}")
            self._zones = zones
        else:
            self._zones = []
    
    def _on_zone_select(self, event) -> None:
        selection = self._zone_list.curselection()
        if selection and hasattr(self, '_zones') and selection[0] < len(self._zones):
            zone = self._zones[selection[0]]
            status = "Armed" if zone.get('armed') else "Disarmed"
            self._zone_status.config(text=f"Zone: {zone['name']} - {status}")
    
    def _get_selected_zone(self):
        selection = self._zone_list.curselection()
        if selection and hasattr(self, '_zones') and selection[0] < len(self._zones):
            return self._zones[selection[0]]
        return None
    
    def _arm_zone(self) -> None:
        zone = self._get_selected_zone()
        if zone:
            response = self.send_to_system('arm_zone', zone_id=zone['id'])
            if response.get('success'):
                messagebox.showinfo("Success", f"Zone '{zone['name']}' armed")
                self._load_zones()
        else:
            messagebox.showwarning("Warning", "Please select a zone")
    
    def _disarm_zone(self) -> None:
        zone = self._get_selected_zone()
        if zone:
            response = self.send_to_system('disarm_zone', zone_id=zone['id'])
            if response.get('success'):
                messagebox.showinfo("Success", f"Zone '{zone['name']}' disarmed")
                self._load_zones()
        else:
            messagebox.showwarning("Warning", "Please select a zone")
    
    def _create_zone(self) -> None:
        # Simple dialog for zone creation
        name = tk.simpledialog.askstring("Create Zone", "Enter zone name:")
        if name:
            response = self.send_to_system('create_safety_zone', name=name, sensor_ids=[])
            if response.get('success'):
                messagebox.showinfo("Success", f"Zone '{name}' created")
                self._load_zones()
    
    def _update_zone(self) -> None:
        zone = self._get_selected_zone()
        if zone:
            name = tk.simpledialog.askstring("Update Zone", "Enter new name:", 
                                            initialvalue=zone['name'])
            if name:
                response = self.send_to_system('update_safety_zone', 
                                              zone_id=zone['id'], name=name, sensor_ids=[])
                if response.get('success'):
                    messagebox.showinfo("Success", "Zone updated")
                    self._load_zones()
        else:
            messagebox.showwarning("Warning", "Please select a zone")
    
    def _delete_zone(self) -> None:
        zone = self._get_selected_zone()
        if zone:
            if messagebox.askyesno("Confirm", f"Delete zone '{zone['name']}'?"):
                response = self.send_to_system('delete_safety_zone', zone_id=zone['id'])
                if response.get('success'):
                    messagebox.showinfo("Success", "Zone deleted")
                    self._load_zones()
        else:
            messagebox.showwarning("Warning", "Please select a zone")
    
    def on_show(self) -> None:
        self._load_zones()


# Import simpledialog
import tkinter.simpledialog
