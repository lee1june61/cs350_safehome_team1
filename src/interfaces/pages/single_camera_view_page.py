"""SingleCameraViewPage - Camera view with pan/zoom (SRS V.3.a,b)"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import ImageTk
from ..components.page import Page


class SingleCameraViewPage(Page):
    """Single camera view with pan/zoom controls and live feed."""
    
    def __init__(self, parent, web_interface):
        super().__init__(parent, web_interface)
        self._cam_id = None
        self._is_visible = False
        self._video_job = None

    def _build_ui(self):
        self._create_header("Camera View", back_page='camera_list')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=20, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=1)
        
        left = ttk.LabelFrame(content, text="Live View", padding=5)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        # Label to display the video feed
        self._video = ttk.Label(left, anchor='center')
        self._video.pack(expand=True, fill='both')
        
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky='nsew')
        
        info = ttk.LabelFrame(right, text="Camera Info", padding=8)
        info.pack(fill='x', pady=5)
        self._info = ttk.Label(info, text="")
        self._info.pack(anchor='w')
        
        ptz = ttk.LabelFrame(right, text="Pan/Zoom", padding=8)
        ptz.pack(fill='x', pady=5)
        pf = ttk.Frame(ptz)
        pf.pack()
        ttk.Button(pf, text="◄ L", command=lambda: self._pan('L'), width=6).pack(side='left', padx=2)
        ttk.Button(pf, text="R ►", command=lambda: self._pan('R'), width=6).pack(side='left', padx=2)
        zf = ttk.Frame(ptz)
        zf.pack(pady=5)
        ttk.Button(zf, text="+ In", command=lambda: self._zoom('in'), width=6).pack(side='left', padx=2)
        ttk.Button(zf, text="- Out", command=lambda: self._zoom('out'), width=6).pack(side='left', padx=2)
        
        act = ttk.LabelFrame(right, text="Actions", padding=8)
        act.pack(fill='x', pady=5)
        self._btn_en = ttk.Button(act, text="Enable", command=self._enable, width=12)
        self._btn_en.pack(pady=2)
        self._btn_dis = ttk.Button(act, text="Disable", command=self._disable, width=12)
        self._btn_dis.pack(pady=2)
        
        pw = ttk.LabelFrame(right, text="Password", padding=8)
        pw.pack(fill='x', pady=5)
        ttk.Button(pw, text="Set Password", command=self._set_pw, width=12).pack(pady=2)
        ttk.Button(pw, text="Delete Password", command=self._del_pw, width=12).pack(pady=2)
    
    def _pan(self, d): self.send_to_system('camera_pan', camera_id=self._cam_id, direction=d); self._update_info()
    def _zoom(self, d): self.send_to_system('camera_zoom', camera_id=self._cam_id, direction=d); self._update_info()
    def _enable(self): self.send_to_system('enable_camera', camera_id=self._cam_id); self._update_info()
    def _disable(self): self.send_to_system('disable_camera', camera_id=self._cam_id); self._update_info()
    
    def _set_pw(self):
        pw = simpledialog.askstring("Set Password", "Enter new password:", show='*')
        if pw:
            old_pw = simpledialog.askstring("Verify", "Enter current password (if any):", show='*')
            res = self.send_to_system('set_camera_password', camera_id=self._cam_id, old_password=old_pw, password=pw)
            if res.get('success'):
                messagebox.showinfo("Success", "Password set")
                self._update_info()
            else:
                messagebox.showerror("Error", res.get('message', "Failed to set password"))

    def _del_pw(self):
        old = simpledialog.askstring("Verify", "Enter current password:", show='*')
        if old is not None:
            res = self.send_to_system('delete_camera_password', camera_id=self._cam_id, old_password=old)
            if res.get('success'):
                messagebox.showinfo("Success", "Password deleted")
                self._update_info()
            else:
                messagebox.showerror("Error", res.get('message', "Wrong password"))
    
    def _update_info(self):
        """Update the camera info text display."""
        res = self.send_to_system('get_camera', camera_id=self._cam_id)
        if res.get('success'):
            c = res.get('data', {})
            en = c.get('enabled', False)
            pw_status = "Yes" if c.get('password') else "No"
            self._info.config(text=f"ID: {c.get('id')}\nLoc: {c.get('location')}\nPan: {c.get('pan', 0)} Zoom: {c.get('zoom', 1)}x\nStatus: {'On' if en else 'Off'}\nPassword: {pw_status}")
            self._btn_en.config(state='disabled' if en else 'normal')
            self._btn_dis.config(state='normal' if en else 'disabled')

    def _update_video_feed(self):
        """Fetch and display the latest camera view."""
        if not self._is_visible:
            return  # Stop the loop if the page is hidden

        res = self.send_to_system('get_camera_view', camera_id=self._cam_id)
        if res.get('success'):
            view = res.get('view')
            if view:
                # Convert PIL Image to PhotoImage
                photo_img = ImageTk.PhotoImage(view)
                
                # Update the label with the new image
                self._video.config(image=photo_img)
                # IMPORTANT: Keep a reference to the image to prevent garbage collection
                self._video.image = photo_img
        
        # Schedule the next update
        self._video_job = self._frame.after(1000, self._update_video_feed)

    def on_show(self):
        """Called when page is displayed."""
        self._is_visible = True
        self._cam_id = self._web_interface.get_context('camera_id', 'C1')
        self._update_info()
        self._update_video_feed() # Start the video feed loop

    def on_hide(self):
        """Called when page is hidden."""
        self._is_visible = False
        if self._video_job:
            self._frame.after_cancel(self._video_job)
            self._video_job = None

