"""ThumbnailViewPage - Thumbnail view of all cameras"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class ThumbnailViewPage(Page):
    """Thumbnail view page showing all cameras"""
    
    def _build_ui(self) -> None:
        header = self._create_header("All Cameras", back_page='surveillance')
        ttk.Button(header, text="Refresh", command=self._load, width=10).pack(side='right')
        
        ttk.Label(self._frame, text="Note: Password-protected cameras are not shown",
                 font=('Arial', 9, 'italic'), foreground='gray').pack(pady=(0, 10))
        
        # Scrollable thumbnail area
        canvas_frame = ttk.Frame(self._frame)
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        self._thumb_frame = ttk.Frame(canvas)
        self._thumb_frame.bind('<Configure>', 
                              lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self._thumb_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _load(self) -> None:
        for widget in self._thumb_frame.winfo_children():
            widget.destroy()
        
        response = self.send_to_system('get_cameras')
        if not response.get('success'):
            return
        
        cameras = [c for c in response.get('data', []) 
                  if c.get('enabled') and not c.get('has_password')]
        
        if not cameras:
            ttk.Label(self._thumb_frame, text="No cameras available", 
                     font=('Arial', 12)).pack(pady=50)
            return
        
        cols = 3
        for i, cam in enumerate(cameras):
            row, col = divmod(i, cols)
            
            frame = ttk.LabelFrame(self._thumb_frame, text=cam['name'], padding=5)
            frame.grid(row=row, column=col, padx=10, pady=10)
            
            canvas = tk.Canvas(frame, width=150, height=100, bg='#333')
            canvas.pack()
            canvas.create_text(75, 50, text=f"📷\n{cam.get('location', '')}", 
                             fill='white', font=('Arial', 9), justify='center')
            canvas.bind('<Button-1>', lambda e, c=cam: self._view(c))
            
            ttk.Label(frame, text="🟢 Enabled", font=('Arial', 8)).pack()
    
    def _view(self, camera: dict) -> None:
        self._web_interface.set_context('current_camera', camera)
        self.navigate_to('single_camera_view')
    
    def on_show(self) -> None:
        self._load()
