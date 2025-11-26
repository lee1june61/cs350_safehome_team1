"""SingleCameraViewPage - Single camera view with controls"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SingleCameraViewPage(Page):
    """Single camera view page with pan/zoom controls"""
    
    def _build_ui(self) -> None:
        header = self._create_header("Camera View", back_page='camera_list')
        self._title = header.winfo_children()[-1]  # Get title label
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Video display
        video_frame = ttk.LabelFrame(content, text="Video Feed (1 FPS)", padding=10)
        video_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self._video = tk.Canvas(video_frame, width=400, height=300, bg='black')
        self._video.pack()
        self._video.create_text(200, 150, text="Camera Feed", fill='white', font=('Arial', 14))
        
        # Controls
        ctrl_frame = ttk.Frame(content)
        ctrl_frame.pack(fill='x')
        
        # Pan/Zoom
        pz = ttk.LabelFrame(ctrl_frame, text="Pan/Zoom", padding=10)
        pz.pack(side='left', padx=(0, 10))
        
        pan_frame = ttk.Frame(pz)
        pan_frame.pack(side='left', padx=(0, 20))
        ttk.Label(pan_frame, text="Pan:").pack()
        btn_row = ttk.Frame(pan_frame)
        btn_row.pack()
        ttk.Button(btn_row, text="◀", command=lambda: self._pan('LEFT'), width=3).pack(side='left')
        ttk.Button(btn_row, text="▶", command=lambda: self._pan('RIGHT'), width=3).pack(side='left')
        
        zoom_frame = ttk.Frame(pz)
        zoom_frame.pack(side='left')
        ttk.Label(zoom_frame, text="Zoom:").pack()
        btn_row2 = ttk.Frame(zoom_frame)
        btn_row2.pack()
        ttk.Button(btn_row2, text="+", command=lambda: self._zoom('IN'), width=3).pack(side='left')
        ttk.Button(btn_row2, text="-", command=lambda: self._zoom('OUT'), width=3).pack(side='left')
        
        # Camera controls
        cam = ttk.LabelFrame(ctrl_frame, text="Camera", padding=10)
        cam.pack(side='left', padx=(0, 10))
        self._enable_btn = ttk.Button(cam, text="Enable", command=self._enable, width=10)
        self._enable_btn.pack(side='left', padx=2)
        self._disable_btn = ttk.Button(cam, text="Disable", command=self._disable, width=10)
        self._disable_btn.pack(side='left', padx=2)
        
        # Password controls
        pw = ttk.LabelFrame(ctrl_frame, text="Password", padding=10)
        pw.pack(side='left')
        ttk.Button(pw, text="Set", command=self._set_password, width=8).pack(side='left', padx=2)
        ttk.Button(pw, text="Delete", command=self._delete_password, width=8).pack(side='left', padx=2)
    
    def _get_camera(self):
        return self._web_interface.get_context('current_camera')
    
    def _pan(self, direction: str) -> None:
        cam = self._get_camera()
        if cam:
            self.send_to_system('pan_camera', camera_id=cam['id'], direction=direction)
    
    def _zoom(self, direction: str) -> None:
        cam = self._get_camera()
        if cam:
            self.send_to_system('zoom_camera', camera_id=cam['id'], direction=direction)
    
    def _enable(self) -> None:
        cam = self._get_camera()
        if cam:
            response = self.send_to_system('enable_camera', camera_id=cam['id'])
            if response.get('success'):
                self._show_message("Success", "Camera enabled")
                self._update_buttons(True)
    
    def _disable(self) -> None:
        cam = self._get_camera()
        if cam:
            response = self.send_to_system('disable_camera', camera_id=cam['id'])
            if response.get('success'):
                self._show_message("Success", "Camera disabled")
                self._update_buttons(False)
    
    def _set_password(self) -> None:
        from .dialogs.camera_password_dialog import CameraPasswordDialog
        cam = self._get_camera()
        if cam:
            CameraPasswordDialog(self._frame.winfo_toplevel(), self._web_interface, cam, 'set').show()
    
    def _delete_password(self) -> None:
        from .dialogs.camera_password_dialog import CameraPasswordDialog
        cam = self._get_camera()
        if cam:
            CameraPasswordDialog(self._frame.winfo_toplevel(), self._web_interface, cam, 'delete').show()
    
    def _update_buttons(self, enabled: bool) -> None:
        self._enable_btn.config(state='disabled' if enabled else 'normal')
        self._disable_btn.config(state='normal' if enabled else 'disabled')
    
    def on_show(self) -> None:
        cam = self._get_camera()
        if cam:
            self._title.config(text=f"Camera: {cam['name']}")
            self._update_buttons(cam.get('enabled', False))
            self._video.delete('all')
            text = f"Video: {cam['name']}\n(1 FPS)" if cam.get('enabled') else "Camera Disabled"
            color = 'white' if cam.get('enabled') else 'gray'
            self._video.create_text(200, 150, text=text, fill=color, font=('Arial', 14))
