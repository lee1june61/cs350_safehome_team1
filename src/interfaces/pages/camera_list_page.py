"""CameraListPage - Pick camera from list/floorplan (SRS V.3.a)"""
import tkinter as tk
from tkinter import ttk, simpledialog
from ..components.page import Page
from ..components.floor_plan import FloorPlan


class CameraListPage(Page):
    """Pick a camera - list + floorplan view."""
    
    def _build_ui(self):
        self._create_header("Pick a Camera", back_page='surveillance')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        
        left = ttk.LabelFrame(content, text="Click camera on map", padding=5)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        self._floorplan = FloorPlan(left, 380, 300)
        self._floorplan.set_on_click(self._on_map_click)
        self._floorplan.create().pack()
        
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky='nsew')
        
        lf = ttk.LabelFrame(right, text="Cameras", padding=5)
        lf.pack(fill='both', expand=True)
        self._list = tk.Listbox(lf, font=('Arial', 10), height=10)
        self._list.pack(fill='both', expand=True)
        self._list.bind('<<ListboxSelect>>', self._on_select)
        
        info = ttk.LabelFrame(right, text="Info", padding=5)
        info.pack(fill='x', pady=5)
        self._info = ttk.Label(info, text="Select a camera")
        self._info.pack()
        
        self._btn = ttk.Button(right, text="View Camera", command=self._view, state='disabled')
        self._btn.pack(pady=10)
        
        self._cams, self._selected = [], None
    
    def _on_map_click(self, dev_id, dev_type):
        if dev_type == 'camera':
            for c in self._cams:
                if c['id'] == dev_id: self._select(c); break
    
    def _on_select(self, e):
        sel = self._list.curselection()
        if sel and sel[0] < len(self._cams): self._select(self._cams[sel[0]])
    
    def _select(self, cam):
        self._selected = cam
        self._btn.config(state='normal')
        en, pw = "On" if cam.get('enabled') else "Off", "Yes" if cam.get('password') else "No"
        self._info.config(text=f"{cam['id']} @ {cam['location']}\nStatus: {en}, Password: {pw}")
    
    def _view(self):
        if not self._selected: return
        c = self._selected
        if c.get('password'):
            pw = simpledialog.askstring("Password", f"Password for {c['id']}:", show='*')
            if not pw: return
            res = self.send_to_system('verify_camera_password', camera_id=c['id'], password=pw)
            if not res.get('success'): return
        self._web_interface.set_context('camera_id', c['id'])
        self.navigate_to('single_camera_view')
    
    def _load(self):
        self._list.delete(0, tk.END)
        res = self.send_to_system('get_cameras')
        self._cams = res.get('data', []) if res.get('success') else []
        for c in self._cams:
            self._list.insert(tk.END, f"{'✓' if c.get('enabled') else '✗'} {c['id']}: {c['location']} {'🔒' if c.get('password') else ''}")
    
    def on_show(self):
        self._load()
        self._selected = None
        self._btn.config(state='disabled')
