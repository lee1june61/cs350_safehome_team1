import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .camera_list_page import CameraListPage
    from ..components.floor_plan import FloorPlan


class CameraSelectionManager:
    """
    Manages the logic for camera selection, viewing, and data loading on the CameraListPage.
    """
    def __init__(self, page_instance: 'CameraListPage', floorplan: 'FloorPlan', listbox: tk.Listbox, info_label: ttk.Label, view_button: ttk.Button):
        self._page = page_instance
        self._web_interface = page_instance._web_interface
        self._floorplan = floorplan
        self._list = listbox
        self._info = info_label
        self._btn = view_button
        
        self._cams: List[Dict] = []
        self._selected: Optional[Dict] = None

    def on_map_click(self, dev_id: str, dev_type: str):
        if dev_type == 'camera':
            for c in self._cams:
                if c['id'] == dev_id:
                    self._select(c)
                    # Also select in listbox if present
                    for i, item_c in enumerate(self._cams):
                        if item_c['id'] == dev_id:
                            self._list.selection_clear(0, tk.END)
                            self._list.selection_set(i)
                            self._list.activate(i)
                            break
                    break

    def on_select(self, event: Any):
        sel = self._list.curselection()
        if sel and sel[0] < len(self._cams):
            self._select(self._cams[sel[0]])
    
    def _select(self, cam: Dict):
        self._selected = cam
        self._btn.config(state='normal')
        en, pw = "On" if cam.get('enabled') else "Off", "Yes" if cam.get('password') else "No"
        self._info.config(text=f"{cam['id']} @ {cam['location']}\nStatus: {en}, Password: {pw}")
    
    def view_camera(self):
        if not self._selected: return
        c = self._selected
        if c.get('password'):
            pw = simpledialog.askstring("Password", f"Password for {c['id']}:
", show='*')
            if not pw: return
            res = self._web_interface.send_message('verify_camera_password', camera_id=c['id'], password=pw)
            if not res.get('success'):
                messagebox.showerror("Verification Failed", res.get('message', "Incorrect password or camera not found."))
                return
        self._web_interface.set_context('camera_id', c['id'])
        self._page.navigate_to('single_camera_view')
    
    def load_cameras(self):
        self._list.delete(0, tk.END)
        res = self._web_interface.send_message('get_cameras')
        self._cams = res.get('data', []) if res.get('success') else []
        for c in self._cams:
            self._list.insert(tk.END, f"{ '✓' if c.get('enabled') else '✗'} {c['id']}: {c['location']} {'🔒' if c.get('password') else ''}")
        
        # Update floorplan camera states
        all_devices_status = self._web_interface.send_message('get_all_devices_status')
        if all_devices_status.get('success'):
            for dev_id, dev_info in all_devices_status['data'].items():
                if dev_info['type'] == 'camera':
                    self._floorplan.set_armed(dev_id, dev_info['armed'])
            self._floorplan.refresh()

    def on_show(self):
        self.load_cameras()
        self._selected = None
        self._btn.config(state='disabled')
        self._floorplan.refresh() # Ensure floorplan is refreshed
