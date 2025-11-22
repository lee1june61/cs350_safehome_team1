"""
SafeHome Control Panel Implementation.
Physical control panel interface for the SafeHome system.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
from datetime import datetime

from src.devices import DeviceControlPanelAbstract


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """
    Physical control panel implementation using Tkinter.
    Provides local interface for homeowner to interact with SafeHome system.
    """
    
    def __init__(self, system):
        """
        Initialize control panel.
        
        Args:
            system: Reference to main System instance
        """
        self.system = system
        self._window: Optional[tk.Tk] = None
        self._current_user: Optional[str] = None
        self._status_label: Optional[tk.Label] = None
        self._message_text: Optional[tk.Text] = None
        
        # UI state
        self._is_running = False
        
    def start(self):
        """Start the control panel GUI."""
        if self._is_running:
            return
        
        self._is_running = True
        self._setup_ui()
        self._window.mainloop()
    
    def stop(self):
        """Stop the control panel GUI."""
        if self._window:
            self._window.quit()
            self._is_running = False
    
    def _setup_ui(self):
        """Setup the main UI window."""
        self._window = tk.Tk()
        self._window.title("SafeHome Control Panel")
        self._window.geometry("800x600")
        self._window.protocol("WM_DELETE_WINDOW", self.stop)
        
        # Main container
        main_frame = ttk.Frame(self._window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame, 
            text="SafeHome Security System", 
            font=("Arial", 24, "bold")
        )
        title_label.pack()
        
        self._status_label = ttk.Label(
            header_frame,
            text="Status: Not Logged In",
            font=("Arial", 12)
        )
        self._status_label.pack(pady=5)
        
        # Login section
        self._create_login_section(main_frame)
        
        # System controls section
        self._create_system_controls(main_frame)
        
        # Security controls section
        self._create_security_controls(main_frame)
        
        # Message display area
        self._create_message_display(main_frame)
        
        # Configure grid weights
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def _create_login_section(self, parent):
        """Create login UI section."""
        login_frame = ttk.LabelFrame(parent, text="Login", padding="10")
        login_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Password entry
        ttk.Label(login_frame, text="Password (4 digits):").grid(row=0, column=0, sticky=tk.W)
        self._password_entry = ttk.Entry(login_frame, show="*", width=20)
        self._password_entry.grid(row=0, column=1, padx=5)
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", command=self._handle_login)
        login_btn.grid(row=0, column=2, padx=5)
        
        # Logout button
        logout_btn = ttk.Button(login_frame, text="Logout", command=self._handle_logout)
        logout_btn.grid(row=0, column=3, padx=5)
        
        # Bind Enter key
        self._password_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _create_system_controls(self, parent):
        """Create system control buttons."""
        system_frame = ttk.LabelFrame(parent, text="System Controls", padding="10")
        system_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(
            system_frame, 
            text="Turn System On", 
            command=self._handle_system_on
        ).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            system_frame, 
            text="Turn System Off", 
            command=self._handle_system_off
        ).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            system_frame, 
            text="Reset System", 
            command=self._handle_system_reset
        ).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            system_frame, 
            text="Change Password", 
            command=self._handle_change_password
        ).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
    
    def _create_security_controls(self, parent):
        """Create security control buttons."""
        security_frame = ttk.LabelFrame(parent, text="Security Controls", padding="10")
        security_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Mode buttons
        ttk.Button(
            security_frame, 
            text="🏠 Home Mode", 
            command=lambda: self._handle_set_mode("ARMED_HOME")
        ).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            security_frame, 
            text="🚗 Away Mode", 
            command=lambda: self._handle_set_mode("ARMED_AWAY")
        ).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            security_frame, 
            text="🌙 Night Mode", 
            command=lambda: self._handle_set_mode("ARMED_NIGHT")
        ).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            security_frame, 
            text="✈️ Vacation Mode", 
            command=lambda: self._handle_set_mode("ARMED_VACATION")
        ).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(
            security_frame, 
            text="⛔ Disarm", 
            command=lambda: self._handle_set_mode("DISARMED")
        ).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Emergency button
        panic_btn = ttk.Button(
            security_frame, 
            text="🚨 PANIC / Emergency", 
            command=self._handle_panic
        )
        panic_btn.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
    
    def _create_message_display(self, parent):
        """Create message display area."""
        message_frame = ttk.LabelFrame(parent, text="System Messages", padding="10")
        message_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Scrollable text widget
        self._message_text = tk.Text(message_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self._message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(message_frame, command=self._message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._message_text['yscrollcommand'] = scrollbar.set
        
        # Configure text tags for different message types
        self._message_text.tag_config('info', foreground='blue')
        self._message_text.tag_config('warning', foreground='orange')
        self._message_text.tag_config('error', foreground='red')
        self._message_text.tag_config('alarm', foreground='red', font=('Arial', 10, 'bold'))
    
    # ============================================================
    # Event Handlers
    # ============================================================
    
    def _handle_login(self):
        """Handle login button click."""
        password = self._password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        try:
            # Attempt login through system
            success = self.system.login_control_panel(password)
            
            if success:
                self._current_user = "User"
                self._status_label.config(text=f"Status: Logged in as {self._current_user}")
                self.display_message("Login successful", "info")
                self._password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Login Failed", "Invalid password")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {e}")
    
    def _handle_logout(self):
        """Handle logout button click."""
        if self._current_user:
            self.system.logout()
            self._current_user = None
            self._status_label.config(text="Status: Not Logged In")
            self.display_message("Logged out successfully", "info")
        else:
            messagebox.showinfo("Info", "Not currently logged in")
    
    def _handle_system_on(self):
        """Handle system on button."""
        if not self._check_logged_in():
            return
        
        try:
            self.system.turn_on()
            self.display_message("System turned ON", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to turn on system: {e}")
    
    def _handle_system_off(self):
        """Handle system off button."""
        if not self._check_logged_in():
            return
        
        confirm = messagebox.askyesno(
            "Confirm", 
            "Are you sure you want to turn off the system?"
        )
        if confirm:
            try:
                self.system.turn_off()
                self.display_message("System turned OFF", "warning")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to turn off system: {e}")
    
    def _handle_system_reset(self):
        """Handle system reset button."""
        if not self._check_logged_in():
            return
        
        confirm = messagebox.askyesno(
            "Confirm Reset", 
            "Are you sure you want to reset the system?"
        )
        if confirm:
            try:
                self.system.reset()
                self.display_message("System RESET", "warning")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset system: {e}")
    
    def _handle_set_mode(self, mode: str):
        """Handle security mode change."""
        if not self._check_logged_in():
            return
        
        try:
            self.system.set_security_mode(mode)
            self.display_message(f"Security mode set to: {mode}", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set mode: {e}")
    
    def _handle_panic(self):
        """Handle panic/emergency button."""
        confirm = messagebox.askyesno(
            "EMERGENCY", 
            "Call monitoring service immediately?",
            icon='warning'
        )
        if confirm:
            try:
                self.system.call_monitoring_service("PANIC")
                self.display_message("🚨 EMERGENCY: Monitoring service called", "alarm")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to call monitoring service: {e}")
    
    def _handle_change_password(self):
        """Handle change password."""
        if not self._check_logged_in():
            return
        
        # Create password change dialog
        dialog = tk.Toplevel(self._window)
        dialog.title("Change Password")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Current Password:").pack(pady=5)
        current_pw = ttk.Entry(dialog, show="*")
        current_pw.pack()
        
        ttk.Label(dialog, text="New Password:").pack(pady=5)
        new_pw = ttk.Entry(dialog, show="*")
        new_pw.pack()
        
        ttk.Label(dialog, text="Confirm Password:").pack(pady=5)
        confirm_pw = ttk.Entry(dialog, show="*")
        confirm_pw.pack()
        
        def do_change():
            if new_pw.get() != confirm_pw.get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            try:
                success = self.system.change_password(current_pw.get(), new_pw.get())
                if success:
                    messagebox.showinfo("Success", "Password changed successfully")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Current password incorrect")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {e}")
        
        ttk.Button(dialog, text="Change", command=do_change).pack(pady=10)
    
    def _check_logged_in(self) -> bool:
        """Check if user is logged in."""
        if not self._current_user:
            messagebox.showerror("Error", "Please login first")
            return False
        return True
    
    # ============================================================
    # DeviceControlPanelAbstract Implementation
    # ============================================================
    
    def display_message(self, message: str, message_type: str = "info"):
        """Display message in the message area."""
        if not self._message_text:
            return
        
        self._message_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self._message_text.insert(tk.END, f"[{timestamp}] ", 'info')
        self._message_text.insert(tk.END, f"{message}\n", message_type)
        
        # Auto-scroll to bottom
        self._message_text.see(tk.END)
        
        self._message_text.config(state=tk.DISABLED)
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> Optional[str]:
        """Get user input via dialog."""
        if input_type == "password":
            from tkinter import simpledialog
            return simpledialog.askstring("Input", prompt, show='*')
        else:
            from tkinter import simpledialog
            return simpledialog.askstring("Input", prompt)
    
    def show_system_status(self, status: dict):
        """Display system status."""
        status_text = f"Mode: {status.get('mode', 'Unknown')}"
        if status.get('alarms'):
            status_text += " | ⚠️ ALARMS ACTIVE"
        
        self._status_label.config(text=f"Status: {status_text}")
        
        # Display details in message area
        details = [
            f"Security Mode: {status.get('mode', 'Unknown')}",
            f"Cameras: {status.get('camera_count', 0)}",
            f"Sensors: {status.get('sensor_count', 0)}",
            f"Active Alarms: {len(status.get('alarms', []))}"
        ]
        self.display_message(" | ".join(details), "info")
    
    def play_alarm_sound(self, duration: float = 5.0):
        """Play alarm sound."""
        self.display_message("🔊 ALARM SOUNDING!", "alarm")
        self._window.bell()  # System beep
    
    def update_zone_display(self, zone_id: int, zone_name: str, is_armed: bool):
        """Update zone display."""
        status = "ARMED ✓" if is_armed else "DISARMED"
        self.display_message(f"Zone '{zone_name}' (ID: {zone_id}): {status}", "info")