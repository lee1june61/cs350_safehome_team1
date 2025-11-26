"""
SafeHomeControlPanel - Physical control panel interface

SDS Design:
- Receives user input (4-digit PIN)
- Sends commands to System
- Displays system status
- Provides panic button functionality

IMPORTANT: ControlPanel does NOT directly access System's internal components.
All requests go through System.handle_request() and System routes internally.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any


class SafeHomeControlPanel(tk.Tk):
    """
    Physical Control Panel Interface.
    
    NOTE: This class ONLY communicates with System.
    It does NOT directly access LoginManager, Alarm, etc.
    """
    
    def __init__(self, system: 'System'):
        super().__init__()
        
        self._system = system
        self._logged_in = False
        
        self._setup_window()
        self._show_login()
    
    def _setup_window(self) -> None:
        self.title("SafeHome Control Panel")
        self.geometry("500x600")
        self.resizable(False, False)
    
    def _clear(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
    
    def _send(self, command: str, **kwargs) -> Dict[str, Any]:
        """Send command to System."""
        if not self._system:
            return {'success': False, 'message': 'System not connected'}
        return self._system.handle_request(source='control_panel', command=command, **kwargs)
    
    # ==================== LOGIN SCREEN ====================
    
    def _show_login(self) -> None:
        self._clear()
        
        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(frame, text="SafeHome", font=('Arial', 28, 'bold')).pack(pady=(0, 5))
        ttk.Label(frame, text="Control Panel", font=('Arial', 14)).pack(pady=(0, 30))
        
        login = ttk.LabelFrame(frame, text="Login", padding=25)
        login.pack()
        
        ttk.Label(login, text="Enter 4-digit PIN:", font=('Arial', 11)).pack(pady=(0, 10))
        
        self._pin = tk.StringVar()
        self._pin.trace_add('write', self._validate_pin)
        self._pin_entry = ttk.Entry(login, textvariable=self._pin, show='*', 
                                    font=('Arial', 18), width=10, justify='center')
        self._pin_entry.pack(pady=(0, 15))
        self._pin_entry.bind('<Return>', lambda e: self._login())
        self._pin_entry.focus_set()
        
        self._login_btn = ttk.Button(login, text="Login", command=self._login, width=15)
        self._login_btn.pack()
        
        self._status = ttk.Label(frame, text="", foreground='red')
        self._status.pack(pady=(15, 0))
        
        ttk.Label(frame, text="Default: 1234 (Master) / 5678 (Guest)",
                 font=('Arial', 9, 'italic'), foreground='gray').pack(pady=(10, 0))
    
    def _validate_pin(self, *args) -> None:
        val = ''.join(c for c in self._pin.get() if c.isdigit())[:4]
        if val != self._pin.get():
            self._pin.set(val)
    
    def _login(self) -> None:
        pin = self._pin.get()
        if len(pin) != 4:
            self._status.config(text="PIN must be 4 digits")
            return
        
        response = self._send('login_control_panel', password=pin)
        
        if response.get('success'):
            self._logged_in = True
            self._show_main()
        else:
            self._pin.set('')
            remaining = response.get('attempts_remaining', 0)
            if remaining == 0:
                self._status.config(text="System locked")
                self._pin_entry.config(state='disabled')
                self._login_btn.config(state='disabled')
                self.after(60000, self._unlock)
            else:
                self._status.config(text=f"Invalid. {remaining} attempts left")
    
    def _unlock(self) -> None:
        self._pin_entry.config(state='normal')
        self._login_btn.config(state='normal')
        self._status.config(text="Unlocked")
    
    # ==================== MAIN SCREEN ====================
    
    def _show_main(self) -> None:
        self._clear()
        
        header = ttk.Frame(self)
        header.pack(fill='x', padx=20, pady=20)
        ttk.Label(header, text="SafeHome", font=('Arial', 20, 'bold')).pack(side='left')
        
        self._led = tk.Canvas(header, width=25, height=25)
        self._led.pack(side='right')
        self._led_circle = self._led.create_oval(2, 2, 23, 23, fill='green')
        
        content = ttk.Frame(self)
        content.pack(fill='both', expand=True, padx=20)
        
        # Status
        left = ttk.LabelFrame(content, text="Status", padding=15)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(left, text="System:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self._armed = ttk.Label(left, text="DISARMED", foreground='green')
        self._armed.pack(anchor='w', pady=(0, 10))
        
        ttk.Label(left, text="Mode:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self._mode = ttk.Label(left, text="None")
        self._mode.pack(anchor='w', pady=(0, 10))
        
        ttk.Label(left, text="Alarm:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self._alarm = ttk.Label(left, text="Silent", foreground='green')
        self._alarm.pack(anchor='w', pady=(0, 10))
        
        ttk.Separator(left).pack(fill='x', pady=10)
        self._sensors = ttk.Label(left, text="Sensors: -")
        self._sensors.pack(anchor='w')
        
        # Controls
        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        sec = ttk.LabelFrame(right, text="Security", padding=10)
        sec.pack(fill='x', pady=(0, 10))
        
        self._arm_home = ttk.Button(sec, text="ARM STAY", 
                                    command=lambda: self._arm('HOME'), width=18)
        self._arm_home.pack(pady=3)
        self._arm_away = ttk.Button(sec, text="ARM AWAY", 
                                    command=lambda: self._arm('AWAY'), width=18)
        self._arm_away.pack(pady=3)
        self._disarm_btn = ttk.Button(sec, text="DISARM", 
                                      command=self._disarm, width=18, state='disabled')
        self._disarm_btn.pack(pady=3)
        
        ttk.Separator(sec).pack(fill='x', pady=10)
        ttk.Button(sec, text="🚨 PANIC", command=self._panic, width=18).pack(pady=3)
        
        sys = ttk.LabelFrame(right, text="System", padding=10)
        sys.pack(fill='x')
        
        ttk.Button(sys, text="Change Password", command=self._change_pw, width=18).pack(pady=3)
        ttk.Separator(sys).pack(fill='x', pady=10)
        ttk.Button(sys, text="Reset", command=self._reset, width=18).pack(pady=3)
        ttk.Button(sys, text="Turn Off", command=self._off, width=18).pack(pady=3)
        ttk.Separator(sys).pack(fill='x', pady=10)
        ttk.Button(sys, text="Logout", command=self._logout, width=18).pack(pady=3)
        
        self._update()
        self._schedule()
    
    def _arm(self, mode: str) -> None:
        response = self._send('arm_system', mode=mode)
        if response.get('success'):
            messagebox.showinfo("Success", f"Armed: {mode}")
        else:
            messagebox.showerror("Error", response.get('message', 'Failed'))
        self._update()
    
    def _disarm(self) -> None:
        response = self._send('disarm_system')
        if response.get('success'):
            messagebox.showinfo("Success", "Disarmed")
        else:
            messagebox.showerror("Error", response.get('message', 'Failed'))
        self._update()
    
    def _panic(self) -> None:
        if not messagebox.askyesno("Confirm", "Trigger panic and call monitoring?"):
            return
        response = self._send('panic')
        if response.get('success'):
            messagebox.showwarning("Alert", "Panic triggered!")
        self._update()
    
    def _change_pw(self) -> None:
        PasswordDialog(self, self._send).show()
    
    def _reset(self) -> None:
        if messagebox.askyesno("Confirm", "Reset the system?"):
            self._send('reset_system')
            self._update()
    
    def _off(self) -> None:
        if messagebox.askyesno("Confirm", "Turn off the system?"):
            self._send('turn_off')
            self.quit()
    
    def _logout(self) -> None:
        self._send('logout')
        self._logged_in = False
        self._show_login()
    
    def _update(self) -> None:
        response = self._send('get_status')
        if not response.get('success'):
            return
        
        data = response.get('data', {})
        armed = data.get('armed', False)
        mode = data.get('mode')
        alarm = data.get('alarm_active', False)
        
        if armed:
            self._armed.config(text="ARMED", foreground='red')
            self._arm_home.config(state='disabled')
            self._arm_away.config(state='disabled')
            self._disarm_btn.config(state='normal')
        else:
            self._armed.config(text="DISARMED", foreground='green')
            self._arm_home.config(state='normal')
            self._arm_away.config(state='normal')
            self._disarm_btn.config(state='disabled')
        
        self._mode.config(text=mode or 'None')
        
        if alarm:
            self._alarm.config(text="🔔 ACTIVE", foreground='red')
            self._led.itemconfig(self._led_circle, fill='red')
        else:
            self._alarm.config(text="Silent", foreground='green')
            self._led.itemconfig(self._led_circle, fill='yellow' if armed else 'green')
        
        self._sensors.config(
            text=f"Sensors: {data.get('active_sensors', 0)}/{data.get('sensor_count', 0)}")
    
    def _schedule(self) -> None:
        if self._logged_in:
            self._update()
            self.after(2000, self._schedule)


class PasswordDialog(tk.Toplevel):
    """Password change dialog"""
    
    def __init__(self, parent, send_func):
        super().__init__(parent)
        self._send = send_func
        
        self.title("Change Password")
        self.geometry("350x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Change Master Password", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 15))
        
        self._vars = [tk.StringVar() for _ in range(3)]
        for label, var in zip(["Current:", "New (4 digits):", "Confirm:"], self._vars):
            ttk.Label(frame, text=label).pack(anchor='w')
            ttk.Entry(frame, textvariable=var, show='*', width=25).pack(pady=(2, 8))
        
        btn = ttk.Frame(frame)
        btn.pack(pady=(5, 0))
        ttk.Button(btn, text="Change", command=self._change, width=10).pack(side='left', padx=5)
        ttk.Button(btn, text="Cancel", command=self.destroy, width=10).pack(side='left', padx=5)
    
    def _change(self) -> None:
        current, new, confirm = [v.get() for v in self._vars]
        
        if len(new) != 4 or not new.isdigit():
            messagebox.showerror("Error", "New password must be 4 digits", parent=self)
            return
        if new != confirm:
            messagebox.showerror("Error", "Passwords don't match", parent=self)
            return
        
        response = self._send('change_password', current_password=current, new_password=new)
        
        if response.get('success'):
            messagebox.showinfo("Success", "Password changed", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", response.get('message', 'Failed'), parent=self)
    
    def show(self):
        self.wait_window()


def run_control_panel(system: 'System') -> None:
    """Run the control panel application."""
    app = SafeHomeControlPanel(system)
    app.mainloop()
