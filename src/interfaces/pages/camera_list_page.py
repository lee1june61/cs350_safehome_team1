"""CameraListPage - Camera list with floor plan"""
import tkinter as tk
from tkinter import ttk, simpledialog
from ..components.page import Page
from ..components.floor_plan import FloorPlan


class CameraListPage(Page):
    """Camera selection page with floor plan"""
    
    def _build_ui(self) -> None:
        self._create_header("Pick a Camera", back_page='surveillance')
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Floor plan
        left = ttk.LabelFrame(content, text="Floor Plan", padding=10)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self._floor_plan = FloorPlan(left, 300, 250)
        self._floor_plan.create_canvas().pack()
        self._floor_plan.set_device_click_handler(self._on_camera_click)
        
        # Camera list
        right = ttk.LabelFrame(content, text="Cameras", padding=10)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        list_frame = ttk.Frame(right)
        list_frame.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self._listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)
        self._listbox.bind('<Double-Button-1>', lambda e: self._view_selected())
        
        ttk.Button(right, text="View Camera", command=self._view_selected, 
                  width=15).pack(pady=(10, 0))
        
        self._cameras = []
    
    def _load_cameras(self) -> None:
        response = self.send_to_system('get_cameras')
        if response.get('success'):
            self._cameras = response.get('data', [])
            self._listbox.delete(0, tk.END)
            for cam in self._cameras:
                status = "🟢" if cam.get('enabled') else "⚪"
                lock = "🔒" if cam.get('has_password') else ""
                self._listbox.insert(tk.END, f"{status} {cam['name']} {lock}")
            
            camera_devices = [{'id': c['id'], 'type': 'CAMERA', 'name': c['name']} 
                             for c in self._cameras]
            self._floor_plan.load_devices_from_list(camera_devices)
    
    def _on_camera_click(self, device) -> None:
        for i, cam in enumerate(self._cameras):
            if cam['id'] == device.device_id:
                self._listbox.selection_clear(0, tk.END)
                self._listbox.selection_set(i)
                self._listbox.see(i)
                break
    
    def _view_selected(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return self._show_message("Info", "Select a camera first", 'warning')
        
        camera = self._cameras[sel[0]]
        
        if camera.get('has_password'):
            password = simpledialog.askstring("Password Required", "Enter camera password:",
                                             show='*', parent=self._frame.winfo_toplevel())
            if password is None:
                return
            response = self.send_to_system('verify_camera_password', 
                                          camera_id=camera['id'], password=password)
            if not response.get('success'):
                return self._show_message("Error", "Invalid password", 'error')
        
        self._web_interface.set_context('current_camera', camera)
        self.navigate_to('single_camera_view')
    
    def on_show(self) -> None:
        self._load_cameras()
