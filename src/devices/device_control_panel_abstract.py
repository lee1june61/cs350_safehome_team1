"""
DeviceControlPanelAbstract - Control Panel GUI from TA (virtual_device_v4)

This is the abstract base class that defines the control panel UI.
Subclasses must implement button callback methods.
"""
import tkinter as tk
from tkinter import Label, Button, Text
from abc import ABC, abstractmethod


class DeviceControlPanelAbstract(tk.Toplevel, ABC):
    """
    Abstract Control Panel GUI.
    
    Requires a tk.Tk() root to exist before creating.
    Subclasses must implement all button methods.
    """
    
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)
        self.title("Control Panel")
        self.geometry("505x300")
        self.resizable(False, False)
        
        # Message variables
        self.short_message1 = ""
        self.short_message2 = ""
        
        x_start, y_start = 15, 15
        x_w1, x_w2, x_w3 = 100, 40, 80
        y_h1, y_h2 = 90, 70
        
        # Security Zone panel
        zone_frame = tk.Frame(self, bd=0, relief='flat', bg='white')
        zone_frame.place(x=x_start, y=y_start, width=(x_w1 + x_w2), height=y_h1)
        
        tk.Label(zone_frame, text="Security Zone", justify='center',
                bg='white', fg='black', font=('Arial', 10, 'bold')).place(
                x=0, y=0, width=x_w1, height=y_h1)
        
        self.display_number = tk.Label(zone_frame, text="1", justify='center',
                                       bg='white', fg='black', font=('Arial', 24, 'bold'))
        self.display_number.place(x=x_w1, y=0, width=x_w2, height=y_h1)
        
        # Status displays
        status_frame = tk.Frame(self, bg='white')
        status_frame.place(x=x_start + x_w1 + x_w2, y=y_start, width=x_w3, height=y_h1)
        
        self.display_away = tk.Label(status_frame, text="away", bg='white', fg='light gray')
        self.display_away.pack(fill='both', expand=True)
        
        self.display_stay = tk.Label(status_frame, text="stay", bg='white', fg='light gray')
        self.display_stay.pack(fill='both', expand=True)
        
        self.display_not_ready = tk.Label(status_frame, text="not ready", bg='white', fg='light gray')
        self.display_not_ready.pack(fill='both', expand=True)
        
        # Text display area
        self.display_text = Text(self, height=3, width=27, bg='white', fg='black',
                                font=('Courier', 10), state='disabled', wrap='word',
                                bd=0, relief='flat', highlightthickness=0)
        text_width = x_w1 + x_w2 + x_w3
        text_height = max(40, y_h2 - 10)
        self.display_text.place(x=x_start, y=y_start + y_h1, width=text_width, height=text_height)
        self.display_text.lower()
        self._update_display_text()
        
        # Button panel
        button_frame = tk.Frame(self)
        button_frame.place(x=300, y=6, width=240, height=300)
        
        # Row 0: Labels
        tk.Label(button_frame, text="     on").grid(row=0, column=0)
        tk.Label(button_frame, text="").grid(row=0, column=1)
        tk.Label(button_frame, text="    off").grid(row=0, column=2)
        tk.Label(button_frame, text="").grid(row=0, column=3)
        tk.Label(button_frame, text="  reset").grid(row=0, column=4)
        
        # Row 1: 1, 2, 3
        Button(button_frame, text="1", bg='white', command=self.button1, width=3).grid(row=1, column=0)
        tk.Label(button_frame, text="").grid(row=1, column=1)
        Button(button_frame, text="2", bg='white', command=self.button2, width=3).grid(row=1, column=2)
        tk.Label(button_frame, text="").grid(row=1, column=3)
        Button(button_frame, text="3", bg='white', command=self.button3, width=3).grid(row=1, column=4)
        
        # Row 2: Empty
        for i in range(5):
            tk.Label(button_frame, text="").grid(row=2, column=i)
        
        # Row 3: 4, 5, 6
        Button(button_frame, text="4", bg='white', command=self.button4, width=3).grid(row=3, column=0)
        tk.Label(button_frame, text="").grid(row=3, column=1)
        Button(button_frame, text="5", bg='white', command=self.button5, width=3).grid(row=3, column=2)
        tk.Label(button_frame, text="").grid(row=3, column=3)
        Button(button_frame, text="6", bg='white', command=self.button6, width=3).grid(row=3, column=4)
        
        # Row 4: Labels
        tk.Label(button_frame, text="  away").grid(row=4, column=0)
        tk.Label(button_frame, text="").grid(row=4, column=1)
        tk.Label(button_frame, text="   stay").grid(row=4, column=2)
        tk.Label(button_frame, text="").grid(row=4, column=3)
        tk.Label(button_frame, text="  code").grid(row=4, column=4)
        
        # Row 5: 7, 8, 9
        Button(button_frame, text="7", bg='white', command=self.button7, width=3).grid(row=5, column=0)
        tk.Label(button_frame, text="").grid(row=5, column=1)
        Button(button_frame, text="8", bg='white', command=self.button8, width=3).grid(row=5, column=2)
        tk.Label(button_frame, text="").grid(row=5, column=3)
        Button(button_frame, text="9", bg='white', command=self.button9, width=3).grid(row=5, column=4)
        
        # Row 6: Empty
        for i in range(5):
            tk.Label(button_frame, text="").grid(row=6, column=i)
        
        # Row 7: *, 0, #
        Button(button_frame, text="*", bg='white', command=self.button_star, width=3).grid(row=7, column=0)
        tk.Label(button_frame, text="").grid(row=7, column=1)
        Button(button_frame, text="0", bg='white', command=self.button0, width=3).grid(row=7, column=2)
        tk.Label(button_frame, text="").grid(row=7, column=3)
        Button(button_frame, text="#", bg='white', command=self.button_sharp, width=3).grid(row=7, column=4)
        
        # Row 8: Panic labels
        tk.Label(button_frame, text="(panic)").grid(row=8, column=0)
        tk.Label(button_frame, text="").grid(row=8, column=1)
        tk.Label(button_frame, text="").grid(row=8, column=2)
        tk.Label(button_frame, text="").grid(row=8, column=3)
        tk.Label(button_frame, text="(panic)").grid(row=8, column=4)
        
        # LED panel
        led_frame = tk.Frame(self)
        led_frame.place(x=30, y=y_start + y_h1 + y_h2, width=230, height=70)
        
        tk.Label(led_frame, text="armed").grid(row=0, column=0)
        tk.Label(led_frame, text="").grid(row=0, column=1)
        tk.Label(led_frame, text="power").grid(row=0, column=2)
        
        self.led_armed = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
        self.led_armed.grid(row=1, column=0)
        tk.Label(led_frame, text="").grid(row=1, column=1)
        self.led_power = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
        self.led_power.grid(row=1, column=2)
    
    def _update_display_text(self):
        self.display_text.config(state='normal')
        self.display_text.delete('1.0', tk.END)
        self.display_text.insert('1.0', f"\n{self.short_message1}\n{self.short_message2}")
        self.display_text.config(state='disabled')
    
    def set_security_zone_number(self, num: int):
        self.display_number.config(text=str(num))
    
    def set_display_away(self, on: bool):
        self.display_away.config(fg='black' if on else 'light gray')
    
    def set_display_stay(self, on: bool):
        self.display_stay.config(fg='black' if on else 'light gray')
    
    def set_display_not_ready(self, on: bool):
        self.display_not_ready.config(fg='black' if on else 'light gray')
    
    def set_display_short_message1(self, message: str):
        self.short_message1 = message
        self._update_display_text()
    
    def set_display_short_message2(self, message: str):
        self.short_message2 = message
        self._update_display_text()
    
    def set_armed_led(self, on: bool):
        self.led_armed.config(bg='red' if on else 'light gray')
    
    def set_powered_led(self, on: bool):
        self.led_power.config(bg='green' if on else 'light gray')
    
    # Abstract button methods
    @abstractmethod
    def button1(self): pass
    @abstractmethod
    def button2(self): pass
    @abstractmethod
    def button3(self): pass
    @abstractmethod
    def button4(self): pass
    @abstractmethod
    def button5(self): pass
    @abstractmethod
    def button6(self): pass
    @abstractmethod
    def button7(self): pass
    @abstractmethod
    def button8(self): pass
    @abstractmethod
    def button9(self): pass
    @abstractmethod
    def button_star(self): pass
    @abstractmethod
    def button0(self): pass
    @abstractmethod
    def button_sharp(self): pass
