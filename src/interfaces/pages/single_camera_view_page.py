"""SingleCameraViewPage - Single camera view with controls (SRS GUI)"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import ImageTk
from ..components.page import Page


class SingleCameraViewPage(Page):
    """Single camera view - SRS 'Display Specific camera view'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Camera View", back_page='surveillance')
        
        # Main content
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Left: Video display
        left_frame = ttk.LabelFrame(content, text="Live View", padding=5)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self._video_label = ttk.Label(left_frame, text="Loading...", anchor='center')
        self._video_label.pack(expand=True, fill='both')
        
        # Right: Controls
        right_frame = ttk.Frame(content)
        right_frame.grid(row=0, column=1, sticky='nsew')
        
        # Camera info
        info_frame = ttk.LabelFrame(right_frame, text="Camera Info", padding=10)
        info_frame.pack(fill='x', pady=5)
        
        self._info_label = ttk.Label(info_frame, text="Camera: -")
        self._info_label.pack(anchor='w')
        
        self._location_label = ttk.Label(info_frame, text="Location: -")
        self._location_label.pack(anchor='w')
        
        self._status_label = ttk.Label(info_frame, text="Status: -")
        self._status_label.pack(anchor='w')
        
        # Pan/Zoom controls
        ptz_frame = ttk.LabelFrame(right_frame, text="Pan/Zoom Control", padding=10)
        ptz_frame.pack(fill='x', pady=10)
        
        # Pan buttons
        pan_frame = ttk.Frame(ptz_frame)
        pan_frame.pack(pady=5)
        
        ttk.Button(pan_frame, text="◄ Left", command=self._pan_left, width=10).pack(side='left', padx=5)
        ttk.Button(pan_frame, text="Right ►", command=self._pan_right, width=10).pack(side='left', padx=5)
        
        # Zoom buttons
        zoom_frame = ttk.Frame(ptz_frame)
        zoom_frame.pack(pady=5)
        
        ttk.Button(zoom_frame, text="+ Zoom In", command=self._zoom_in, width=10).pack(side='left', padx=5)
        ttk.Button(zoom_frame, text="- Zoom Out", command=self._zoom_out, width=10).pack(side='left', padx=5)
        
        # Camera actions
        action_frame = ttk.LabelFrame(right_frame, text="Camera Actions", padding=10)
        action_frame.pack(fill='x', pady=10)
        
        self._btn_enable = ttk.Button(action_frame, text="Enable", command=self._enable, width=15)
        self._btn_enable.pack(pady=3)
        
        self._btn_disable = ttk.Button(action_frame, text="Disable", command=self._disable, width=15)
        self._btn_disable.pack(pady=3)
        
        ttk.Separator(action_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(action_frame, text="Set Password", command=self._set_password, width=15).pack(pady=3)
        ttk.Button(action_frame, text="Delete Password", command=self._delete_password, width=15).pack(pady=3)
        
        # Timer for video update
        self._update_timer = None
        self._camera = None
        self._photo = None
    
    def _get_camera_id(self) -> int:
        return self._web_interface.get_context('camera_id', 1)
    
    def _start_video(self) -> None:
        """Start video update loop"""
        self._update_video()
    
    def _update_video(self) -> None:
        """Update video frame"""
        if not self._is_visible:
            return
        
        if self._camera:
            try:
                img = self._camera.get_view()
                if img:
                    # Resize for display
                    img = img.resize((400, 400))
                    self._photo = ImageTk.PhotoImage(img)
                    self._video_label.config(image=self._photo, text='')
            except Exception as e:
                self._video_label.config(text=f"Error: {e}")
        
        # Schedule next update (1 FPS as per SRS)
        self._update_timer = self._frame.after(1000, self._update_video)
    
    def _stop_video(self) -> None:
        """Stop video update loop"""
        if self._update_timer:
            self._frame.after_cancel(self._update_timer)
            self._update_timer = None
    
    def _pan_left(self) -> None:
        if self._camera:
            self._camera.pan_left()
    
    def _pan_right(self) -> None:
        if self._camera:
            self._camera.pan_right()
    
    def _zoom_in(self) -> None:
        if self._camera:
            self._camera.zoom_in()
    
    def _zoom_out(self) -> None:
        if self._camera:
            self._camera.zoom_out()
    
    def _enable(self) -> None:
        if self._camera:
            self._camera.enable()
            self._update_status()
    
    def _disable(self) -> None:
        if self._camera:
            self._camera.disable()
            self._update_status()
    
    def _set_password(self) -> None:
        password = simpledialog.askstring("Set Password", "Enter new password:", show='*')
        if password:
            if self._camera:
                self._camera.set_password(password)
                messagebox.showinfo("Success", "Password set")
    
    def _delete_password(self) -> None:
        if self._camera and self._camera.has_password():
            current = simpledialog.askstring("Verify", "Enter current password:", show='*')
            if current and self._camera.verify_password(current):
                self._camera.clear_password()
                messagebox.showinfo("Success", "Password deleted")
            else:
                messagebox.showerror("Error", "Wrong password")
        else:
            messagebox.showinfo("Info", "No password set")
    
    def _update_status(self) -> None:
        if self._camera:
            enabled = self._camera.is_enabled()
            self._status_label.config(text=f"Status: {'Enabled' if enabled else 'Disabled'}")
            self._btn_enable.config(state='disabled' if enabled else 'normal')
            self._btn_disable.config(state='normal' if enabled else 'disabled')
    
    def on_show(self) -> None:
        camera_id = self._get_camera_id()
        
        # Create camera device
        from src.devices import DeviceCamera
        self._camera = DeviceCamera()
        self._camera.set_id(camera_id)
        self._camera.set_location(f"Camera {camera_id}")
        
        # Update info
        self._info_label.config(text=f"Camera: {camera_id}")
        self._location_label.config(text=f"Location: Camera {camera_id}")
        self._update_status()
        
        # Start video
        self._start_video()
    
    def on_hide(self) -> None:
        self._stop_video()
        if self._camera:
            self._camera.stop()
            self._camera = None
