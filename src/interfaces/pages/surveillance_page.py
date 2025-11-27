"""SurveillancePage - Camera surveillance menu (SRS GUI)"""
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ..components.page import Page


ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')


class SurveillancePage(Page):
    """Surveillance page - SRS Section II 'Surveillance Function'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Surveillance Function", back_page='major_function')
        
        # Main content
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Left: Floor plan with camera icons
        left_frame = ttk.LabelFrame(content, text="Floor Plan", padding=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._canvas = tk.Canvas(left_frame, bg='white', width=400, height=400)
        self._canvas.pack(expand=True, fill='both')
        self._canvas.bind('<Button-1>', self._on_canvas_click)
        self._load_floorplan()
        
        # Right: Buttons and camera list
        right_frame = ttk.Frame(content)
        right_frame.grid(row=0, column=1, sticky='nsew')
        
        # Main buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=20)
        
        tk.Button(btn_frame, text="Pick a Camera", font=('Arial', 14),
                 bg='#2196F3', fg='white', height=2,
                 command=lambda: self.navigate_to('camera_list')).pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="All Cameras", font=('Arial', 14),
                 bg='#4CAF50', fg='white', height=2,
                 command=lambda: self.navigate_to('thumbnail_view')).pack(fill='x', pady=5)
        
        # Camera list
        list_frame = ttk.LabelFrame(right_frame, text="Cameras", padding=10)
        list_frame.pack(fill='both', expand=True, pady=10)
        
        self._camera_list = tk.Listbox(list_frame, font=('Arial', 11))
        self._camera_list.pack(fill='both', expand=True)
        self._camera_list.bind('<Double-Button-1>', self._on_camera_double_click)
        
        # Instructions
        ttk.Label(right_frame, text="Double-click camera to view", 
                 foreground='gray').pack(pady=5)
    
    def _load_floorplan(self) -> None:
        """Load floorplan and draw camera icons"""
        try:
            path = os.path.join(ASSETS_DIR, 'floorplan.png')
            img = Image.open(path)
            img = img.resize((400, 400), Image.LANCZOS)
            self._floorplan_img = ImageTk.PhotoImage(img)
            self._canvas.create_image(0, 0, anchor='nw', image=self._floorplan_img)
        except Exception:
            self._canvas.create_rectangle(10, 10, 390, 390, outline='gray')
            self._canvas.create_text(200, 200, text="Floor Plan", fill='gray')
        
        # Draw camera icons
        self._draw_camera_icons()
    
    def _draw_camera_icons(self) -> None:
        """Draw camera icons on floor plan"""
        # Camera positions (mock data - should come from system)
        positions = [
            (100, 80, 1, "Front Door"),
            (300, 150, 2, "Back Yard"),
            (200, 300, 3, "Garage"),
        ]
        
        self._camera_positions = {}
        for x, y, cam_id, name in positions:
            # Draw camera icon (small circle)
            self._canvas.create_oval(x-15, y-15, x+15, y+15, fill='blue', tags=f'cam_{cam_id}')
            self._canvas.create_text(x, y, text='📷', font=('Arial', 12), tags=f'cam_{cam_id}')
            self._canvas.create_text(x, y+25, text=name, font=('Arial', 8), tags=f'cam_{cam_id}')
            self._camera_positions[cam_id] = (x, y, name)
    
    def _on_canvas_click(self, event) -> None:
        """Handle click on floor plan"""
        for cam_id, (x, y, name) in self._camera_positions.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                self._view_camera(cam_id)
                break
    
    def _on_camera_double_click(self, event) -> None:
        """Handle double-click on camera list"""
        selection = self._camera_list.curselection()
        if selection and hasattr(self, '_cameras'):
            camera = self._cameras[selection[0]]
            self._view_camera(camera['id'])
    
    def _view_camera(self, camera_id: int) -> None:
        """Navigate to camera view"""
        self._web_interface.set_context('camera_id', camera_id)
        self.navigate_to('single_camera_view')
    
    def _load_cameras(self) -> None:
        """Load camera list from system"""
        self._camera_list.delete(0, tk.END)
        response = self.send_to_system('get_cameras')
        
        if response.get('success'):
            cameras = response.get('data', [])
            for cam in cameras:
                status = "✓" if cam.get('enabled') else "✗"
                lock = "🔒" if cam.get('has_password') else ""
                self._camera_list.insert(tk.END, f"{status} Camera {cam['id']}: {cam['location']} {lock}")
            self._cameras = cameras
        else:
            self._cameras = []
    
    def on_show(self) -> None:
        self._load_cameras()
