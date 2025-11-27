"""CameraListPage - Pick a camera from list (SRS GUI)"""
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
from ..components.page import Page


ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')


class CameraListPage(Page):
    """Camera list page - SRS 'Pick a Camera'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Pick a Camera", back_page='surveillance')
        
        # Main content
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Left: Floor plan
        left_frame = ttk.LabelFrame(content, text="Floor Plan", padding=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._canvas = tk.Canvas(left_frame, bg='white', width=400, height=400)
        self._canvas.pack(expand=True, fill='both')
        self._canvas.bind('<Button-1>', self._on_canvas_click)
        self._load_floorplan()
        
        # Right: Camera details
        right_frame = ttk.Frame(content)
        right_frame.grid(row=0, column=1, sticky='nsew')
        
        # Camera list
        list_frame = ttk.LabelFrame(right_frame, text="Select Camera", padding=10)
        list_frame.pack(fill='both', expand=True)
        
        self._camera_list = tk.Listbox(list_frame, font=('Arial', 11), height=12)
        self._camera_list.pack(fill='both', expand=True, pady=(0, 10))
        self._camera_list.bind('<<ListboxSelect>>', self._on_select)
        
        # Selected camera info
        info_frame = ttk.LabelFrame(right_frame, text="Camera Info", padding=10)
        info_frame.pack(fill='x', pady=10)
        
        self._info_text = tk.Text(info_frame, height=5, width=30, state='disabled')
        self._info_text.pack(fill='x')
        
        # View button
        self._btn_view = ttk.Button(right_frame, text="View Camera", 
                                   command=self._view_selected, width=20, state='disabled')
        self._btn_view.pack(pady=10)
        
        # Camera positions for click detection
        self._camera_positions = {}
    
    def _load_floorplan(self) -> None:
        try:
            path = os.path.join(ASSETS_DIR, 'floorplan.png')
            img = Image.open(path)
            img = img.resize((400, 400), Image.LANCZOS)
            self._floorplan_img = ImageTk.PhotoImage(img)
            self._canvas.create_image(0, 0, anchor='nw', image=self._floorplan_img)
        except Exception:
            self._canvas.create_rectangle(10, 10, 390, 390, outline='gray')
            self._canvas.create_text(200, 200, text="Floor Plan", fill='gray')
    
    def _draw_camera_icons(self, cameras) -> None:
        """Draw camera icons on floor plan"""
        self._canvas.delete('camera')
        self._camera_positions = {}
        
        # Predefined positions (in real app, would come from config)
        positions = {1: (100, 80), 2: (300, 150), 3: (200, 300)}
        
        for cam in cameras:
            cam_id = cam['id']
            x, y = positions.get(cam_id, (50 + cam_id * 100, 200))
            
            color = 'green' if cam.get('enabled') else 'gray'
            if cam.get('has_password'):
                color = 'orange'
            
            self._canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags='camera')
            self._canvas.create_text(x, y, text=str(cam_id), fill='white', 
                                    font=('Arial', 10, 'bold'), tags='camera')
            self._canvas.create_text(x, y+25, text=cam['location'], 
                                    font=('Arial', 8), tags='camera')
            
            self._camera_positions[cam_id] = (x, y, cam)
    
    def _on_canvas_click(self, event) -> None:
        for cam_id, (x, y, cam) in self._camera_positions.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                self._select_camera(cam)
                break
    
    def _on_select(self, event) -> None:
        selection = self._camera_list.curselection()
        if selection and hasattr(self, '_cameras'):
            cam = self._cameras[selection[0]]
            self._select_camera(cam)
    
    def _select_camera(self, cam) -> None:
        self._selected_camera = cam
        self._btn_view.config(state='normal')
        
        # Update info
        self._info_text.config(state='normal')
        self._info_text.delete('1.0', tk.END)
        self._info_text.insert('1.0', 
            f"Camera ID: {cam['id']}\n"
            f"Location: {cam['location']}\n"
            f"Status: {'Enabled' if cam.get('enabled') else 'Disabled'}\n"
            f"Password: {'Yes' if cam.get('has_password') else 'No'}"
        )
        self._info_text.config(state='disabled')
    
    def _view_selected(self) -> None:
        if hasattr(self, '_selected_camera'):
            cam = self._selected_camera
            
            # Check password
            if cam.get('has_password'):
                password = simpledialog.askstring("Password", 
                    f"Enter password for Camera {cam['id']}:", show='*')
                if not password:
                    return
                # In real app, would verify password
            
            self._web_interface.set_context('camera_id', cam['id'])
            self.navigate_to('single_camera_view')
    
    def _load_cameras(self) -> None:
        self._camera_list.delete(0, tk.END)
        
        response = self.send_to_system('get_cameras')
        if response.get('success'):
            cameras = response.get('data', [])
            for cam in cameras:
                status = "✓" if cam.get('enabled') else "✗"
                lock = "🔒" if cam.get('has_password') else ""
                self._camera_list.insert(tk.END, 
                    f"{status} Camera {cam['id']}: {cam['location']} {lock}")
            self._cameras = cameras
            self._draw_camera_icons(cameras)
        else:
            self._cameras = []
    
    def on_show(self) -> None:
        self._load_cameras()
        self._btn_view.config(state='disabled')
