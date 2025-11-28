"""ThumbnailViewPage - All cameras thumbnails (SRS V.3.e)"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from ..components.page import Page


class ThumbnailViewPage(Page):
    """View all cameras as thumbnails. Shows all enabled cameras with lock indicators."""
    
    def _build_ui(self):
        self._create_header("All Cameras", back_page='surveillance')
        self._content = ttk.Frame(self._frame)
        self._content.pack(expand=True, fill='both', padx=20, pady=10)
        self._frames = []
        self._images = []  # Keep references to images
    
    def _create_grid(self):
        for f in self._frames: f.destroy()
        self._frames = []
        self._images = []
        
        res = self.send_to_system('get_thumbnails')
        cams = res.get('data', {}) if res.get('success') else {}
        
        cols = 3
        for i, (cam_id, cam) in enumerate(cams.items()):
            r, c = i // cols, i % cols
            is_locked = cam.get('locked', False)
            
            f = ttk.LabelFrame(self._content, text=f"{cam_id}: {cam.get('location', '')}")
            f.grid(row=r, column=c, padx=8, pady=8, sticky='nsew')
            self._content.columnconfigure(c, weight=1)
            self._content.rowconfigure(r, weight=1)
            
            # Get thumbnail image
            if is_locked:
                # Show locked indicator
                locked_label = ttk.Label(
                    f, 
                    text="🔒 LOCKED\n\nPassword Required",
                    font=('Arial', 14, 'bold'),
                    foreground='red',
                    anchor='center'
                )
                locked_label.pack(expand=True, fill='both', padx=5, pady=5)
                locked_label.bind('<Button-1>', lambda e, cid=cam_id: self._view(cid))
            else:
                # Get actual thumbnail
                view_res = self.send_to_system('get_camera_view', camera_id=cam_id)
                if view_res.get('success') and view_res.get('view'):
                    view_img = view_res.get('view')
                    # Resize to thumbnail size
                    try:
                        from PIL import Image
                        thumbnail = view_img.resize((200, 150), Image.Resampling.LANCZOS)
                    except (AttributeError, ImportError):
                        # Fallback for older PIL versions
                        thumbnail = view_img.resize((200, 150))
                    photo = ImageTk.PhotoImage(thumbnail)
                    self._images.append(photo)  # Keep reference
                    
                    img_label = ttk.Label(f, image=photo, anchor='center')
                    img_label.pack(expand=True, fill='both', padx=5, pady=5)
                    img_label.bind('<Button-1>', lambda e, cid=cam_id: self._view(cid))
                else:
                    # Fallback if image not available
                    lbl = ttk.Label(f, text=f"📷\n{cam_id}", font=('Arial', 16), anchor='center')
                    lbl.pack(expand=True, fill='both', padx=5, pady=5)
                    lbl.bind('<Button-1>', lambda e, cid=cam_id: self._view(cid))
            
            self._frames.append(f)
        
        if not cams:
            ttk.Label(self._content, text="No cameras available", font=('Arial', 14)).pack(pady=50)
    
    def _view(self, cam_id):
        self._web_interface.set_context('camera_id', cam_id)
        self.navigate_to('single_camera_view')
    
    def on_show(self): 
        self._create_grid()
