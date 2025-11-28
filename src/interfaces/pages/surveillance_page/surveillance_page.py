"""SurveillancePage - Camera surveillance (SRS V.3)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page
from ...components.floor_plan import FloorPlan


class SurveillancePage(Page):
    """Surveillance main page - pick camera or view all."""
    
    def _build_ui(self):
        self._create_header("Surveillance Function", back_page='major_function')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        
        left = ttk.LabelFrame(content, text="Floor Plan - Click camera", padding=5)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        self._floorplan = FloorPlan(left, 400, 320)
        self._floorplan.set_on_click(self._on_device_click)
        self._floorplan.create().pack()
        
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky='nsew')
        
        tk.Button(right, text="Pick a Camera", font=('Arial', 12), bg='#2196F3', fg='white',
                 height=2, command=lambda: self.navigate_to('camera_list')).pack(fill='x', pady=5)
        tk.Button(right, text="All Cameras", font=('Arial', 12), bg='#4CAF50', fg='white',
                 height=2, command=lambda: self.navigate_to('thumbnail_view')).pack(fill='x', pady=5)
        
        lf = ttk.LabelFrame(right, text="Cameras", padding=5)
        lf.pack(fill='both', expand=True, pady=10)
        self._list = tk.Listbox(lf, font=('Arial', 10))
        self._list.pack(fill='both', expand=True)
        self._list.bind('<Double-Button-1>', self._on_dblclick)
        
        ttk.Label(right, text="Double-click to view", foreground='gray').pack()
        self._cams = []
    
    def _on_device_click(self, dev_id: str, dev_type: str):
        if dev_type == 'camera':
            self._web_interface.set_context('camera_id', dev_id)
            self.navigate_to('single_camera_view')
    
    def _on_dblclick(self, e):
        sel = self._list.curselection()
        if sel and sel[0] < len(self._cams):
            self._web_interface.set_context('camera_id', self._cams[sel[0]]['id'])
            self.navigate_to('single_camera_view')
    
    def _load(self):
        self._list.delete(0, tk.END)
        res = self.send_to_system('get_cameras')
        self._cams = res.get('data', []) if res.get('success') else []
        for c in self._cams:
            st = "✓" if c.get('enabled') else "✗"
            lock = "🔒" if c.get('password') else ""
            self._list.insert(tk.END, f"{st} {c['id']}: {c['location']} {lock}")
    
    def on_show(self): self._load()


