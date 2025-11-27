"""ThumbnailViewPage - View all cameras as thumbnails (SRS GUI)"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ..components.page import Page


class ThumbnailViewPage(Page):
    """Thumbnail view - SRS 'View thumbnail Shots'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("All Cameras", back_page='surveillance')
        
        # Main content - grid of thumbnails
        self._content = ttk.Frame(self._frame)
        self._content.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Will hold camera frames
        self._camera_frames = []
        self._cameras = []
        self._photos = []
        self._update_timer = None
    
    def _create_thumbnails(self) -> None:
        """Create thumbnail grid"""
        # Clear existing
        for frame in self._camera_frames:
            frame.destroy()
        self._camera_frames = []
        self._cameras = []
        self._photos = []
        
        # Get camera list
        response = self.send_to_system('get_cameras')
        if not response.get('success'):
            return
        
        camera_data = response.get('data', [])
        
        # Create DeviceCamera for each
        from src.devices import DeviceCamera
        
        cols = 3  # 3 columns
        for i, cam_data in enumerate(camera_data):
            row, col = i // cols, i % cols
            
            frame = ttk.LabelFrame(self._content, text=f"Camera {cam_data['id']}: {cam_data['location']}")
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Configure grid weights
            self._content.columnconfigure(col, weight=1)
            self._content.rowconfigure(row, weight=1)
            
            # Create label for video
            label = ttk.Label(frame, text="Loading...")
            label.pack(expand=True, fill='both', padx=5, pady=5)
            
            # Click to view full
            label.bind('<Button-1>', lambda e, cid=cam_data['id']: self._view_camera(cid))
            
            self._camera_frames.append(frame)
            
            # Create camera device (if not password protected)
            if not cam_data.get('has_password'):
                camera = DeviceCamera()
                camera.set_id(cam_data['id'])
                self._cameras.append((camera, label, cam_data))
            else:
                label.config(text="🔒 Password Protected")
                self._cameras.append((None, label, cam_data))
    
    def _update_thumbnails(self) -> None:
        """Update all thumbnail views"""
        if not self._is_visible:
            return
        
        for camera, label, cam_data in self._cameras:
            if camera and cam_data.get('enabled', True):
                try:
                    img = camera.get_view()
                    if img:
                        img = img.resize((200, 150))
                        photo = ImageTk.PhotoImage(img)
                        label.config(image=photo, text='')
                        # Keep reference
                        label._photo = photo
                except Exception:
                    label.config(text="Error")
        
        # Schedule next update (1 FPS)
        self._update_timer = self._frame.after(1000, self._update_thumbnails)
    
    def _view_camera(self, camera_id: int) -> None:
        """Navigate to single camera view"""
        self._web_interface.set_context('camera_id', camera_id)
        self.navigate_to('single_camera_view')
    
    def _stop_cameras(self) -> None:
        """Stop all camera threads"""
        if self._update_timer:
            self._frame.after_cancel(self._update_timer)
            self._update_timer = None
        
        for camera, label, cam_data in self._cameras:
            if camera:
                camera.stop()
    
    def on_show(self) -> None:
        self._create_thumbnails()
        self._update_thumbnails()
    
    def on_hide(self) -> None:
        self._stop_cameras()
        self._cameras = []
