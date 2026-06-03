# ==============================================================================
# 📄 PROJECT: NetSpeed Monitor Pro & SpeedTester
# 👤 AUTHOR: Eng Ahmed Abdelaziz
# 📅 YEAR: 2026
# 📜 LICENSE: MIT License
# 🛠️ LANGUAGE: Python (Tkinter, Psutil, Speedtest-cli)
# ==============================================================================
# COPYRIGHT NOTICE:
# Copyright (c) 2026 Eng Ahmed Abdelaziz. All rights reserved.
# This code is open-source under the MIT License terms. You are free to use, 
# modify, and distribute, provided that the original author credit is maintained.
# ==============================================================================

import tkinter as tk
from tkinter import messagebox
import psutil
import os
import sys
import winreg
import threading
import math

# توجيه أوامر الطباعة الخلفية لمنع الانهيار في ملفات .pyw
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

try:
    import speedtest
except ImportError:
    speedtest = None

APPDATA_DIR = os.getenv('APPDATA')
POS_FILE = os.path.join(APPDATA_DIR, "netspeed_pos.txt")
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "NetSpeedMonitor"

def format_speed(bytes_per_sec):
    for unit in ['B/s ', 'KB/s', 'MB/s', 'GB/s']:
        if bytes_per_sec < 1024.0:
            return f"{bytes_per_sec:5.1f} {unit}"
        bytes_per_sec /= 1024.0
    return "  0.0 B/s "

class SpeedTestWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Speed Test Pro")
        self.top.geometry("350x450")
        self.top.configure(bg="#1E1E1E")
        self.top.attributes('-topmost', True)
        
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()
        self.top.geometry(f"+{int(sw/2 - 175)}+{int(sh/2 - 225)}")

        self.canvas = tk.Canvas(self.top, width=300, height=180, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.cx, self.cy, self.r = 150, 160, 130 
        
        for i in range(45):
            start_angle = 180 - (i * 4)
            extent_angle = -4.5 
            w = 3 + (i / 44.0) * 13
            
            if i < 15:
                col = "#2ECC71" 
            elif i < 30:
                col = "#F1C40F" 
            else:
                col = "#E74C3C" 
                
            self.canvas.create_arc(self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r,
                                   start=start_angle, extent=extent_angle, style=tk.ARC, outline=col, width=w)
        
        for speed in range(0, 101, 5):
            angle = 180 - (speed * 1.8)
            rad = math.radians(angle)
            is_major = (speed % 20 == 0)
            
            r_outer = self.r - 18
            r_inner = self.r - 28 if not is_major else self.r - 33
            
            x1 = self.cx + r_inner * math.cos(rad)
            y1 = self.cy - r_inner * math.sin(rad)
            x2 = self.cx + r_outer * math.cos(rad)
            y2 = self.cy - r_outer * math.sin(rad)
            
            self.canvas.create_line(x1, y1, x2, y2, fill="#777777" if not is_major else "#DDDDDD", width=2 if is_major else 1)
            
            if is_major:
                r_text = self.r - 48
                tx = self.cx + r_text * math.cos(rad)
                ty = self.cy - r_text * math.sin(rad)
                self.canvas.create_text(tx, ty, text=str(speed), fill="#AAAAAA", font=("Arial", 8, "bold"))
        
        self.center_text = self.canvas.create_text(self.cx, self.cy - 60, text="0.0", font=("Consolas", 32, "bold"), fill="#FFFFFF")
        self.unit_text = self.canvas.create_text(self.cx, self.cy - 25, text="Mbps", font=("Arial", 10, "bold"), fill="#888888")
        
        self.needle_color = "#FFFFFF"
        self.needle = self.canvas.create_line(self.cx, self.cy, self.cx-self.r, self.cy, width=4, fill=self.needle_color, arrow=tk.LAST)
        
        self.canvas.create_oval(self.cx - 8, self.cy - 8, self.cx + 8, self.cy + 8, fill="#2C3E50", outline="#7F8C8D", width=2)

        self.current_angle = 180.0
        self.target_angle = 180.0
        
        self.anim_state = "up" 
        self.current_phase = "init"
        self.last_bytes_recv = 0
        self.last_bytes_sent = 0
        
        self.status_lbl = tk.Label(self.top, text="Initializing...", font=("Arial", 12, "bold"), fg="white", bg="#1E1E1E")
        self.status_lbl.pack()
        
        self.ping_lbl = tk.Label(self.top, text="Ping: -- ms", font=("Consolas", 13), fg="#A9A9A9", bg="#1E1E1E")
        self.ping_lbl.pack(pady=8)
        self.dl_lbl = tk.Label(self.top, text="Download: -- Mbps", font=("Consolas", 14, "bold"), fg="#00BFFF", bg="#1E1E1E")
        self.dl_lbl.pack(pady=8)
        self.ul_lbl = tk.Label(self.top, text="Upload: -- Mbps", font=("Consolas", 14, "bold"), fg="#FFA500", bg="#1E1E1E")
        self.ul_lbl.pack(pady=8)
        
        self.target_angle = 0.0 
        self.animate_needle()

    def set_speed(self, speed):
        visual_speed = min(speed, 100.0) 
        self.target_angle = 180.0 - (visual_speed * 1.8)

    def animate_needle(self):
        if not self.top.winfo_exists():
            return
            
        if abs(self.current_angle - self.target_angle) > 0.5:
            self.current_angle += (self.target_angle - self.current_angle) * 0.15
            
        rad = math.radians(self.current_angle)
        x = self.cx + (self.r - 28) * math.cos(rad)
        y = self.cy - (self.r - 28) * math.sin(rad)
        
        self.canvas.coords(self.needle, self.cx, self.cy, x, y)
        self.canvas.itemconfig(self.needle, fill=self.needle_color)
        
        if self.anim_state == "up" and self.current_angle <= 5.0:
            self.target_angle = 180.0
            self.anim_state = "down"
        elif self.anim_state == "down" and self.current_angle >= 175.0:
            self.anim_state = "ready"
            threading.Thread(target=self.run_test, daemon=True).start()
            self.last_bytes_recv = psutil.net_io_counters().bytes_recv
            self.last_bytes_sent = psutil.net_io_counters().bytes_sent
            self.track_live_traffic()
            
        self.top.after(20, self.animate_needle)

    def track_live_traffic(self):
        if not self.top.winfo_exists() or self.current_phase == "done":
            return
            
        now_io = psutil.net_io_counters()
        
        if self.current_phase == "download":
            diff = now_io.bytes_recv - self.last_bytes_recv
            live_mbps = (diff * 40) / 1000000.0
            self.set_speed(live_mbps)
            self.canvas.itemconfig(self.center_text, text=f"{live_mbps:.1f}", fill="#00BFFF")
            self.needle_color = "#00BFFF"
            
        elif self.current_phase == "upload":
            diff = now_io.bytes_sent - self.last_bytes_sent
            live_mbps = (diff * 40) / 1000000.0
            self.set_speed(live_mbps)
            self.canvas.itemconfig(self.center_text, text=f"{live_mbps:.1f}", fill="#FFA500")
            self.needle_color = "#FFA500"

        self.last_bytes_recv = now_io.bytes_recv
        self.last_bytes_sent = now_io.bytes_sent
        
        self.top.after(200, self.track_live_traffic)

    def run_test(self):
        try:
            st = speedtest.Speedtest()
            
            self.current_phase = "ping"
            self.top.after(0, lambda: self.status_lbl.config(text="Finding Best Server..."))
            st.get_best_server()
            ping = st.results.ping
            self.top.after(0, lambda: self.ping_lbl.config(text=f"Ping: {ping:.1f} ms", fg="#00FF00"))
            
            self.current_phase = "download"
            self.top.after(0, lambda: self.status_lbl.config(text="Testing Download Speed..."))
            dl_speed_bits = st.download() 
            dl_speed_mbps = dl_speed_bits / 1000000.0
            
            self.top.after(0, lambda: self.set_speed(dl_speed_mbps))
            self.top.after(0, lambda: self.canvas.itemconfig(self.center_text, text=f"{dl_speed_mbps:.1f}"))
            self.top.after(0, lambda: self.dl_lbl.config(text=f"Download: {dl_speed_mbps:.2f} Mbps"))
            
            self.current_phase = "upload"
            self.top.after(0, lambda: self.status_lbl.config(text="Testing Upload Speed..."))
            self.top.after(0, lambda: self.set_speed(0)) 
            ul_speed_bits = st.upload()
            ul_speed_mbps = ul_speed_bits / 1000000.0
            
            self.top.after(0, lambda: self.set_speed(ul_speed_mbps))
            self.top.after(0, lambda: self.canvas.itemconfig(self.center_text, text=f"{ul_speed_mbps:.1f}"))
            self.top.after(0, lambda: self.ul_lbl.config(text=f"Upload: {ul_speed_mbps:.2f} Mbps"))
            
            self.current_phase = "done"
            self.top.after(0, lambda: self.status_lbl.config(text="Test Completed!", fg="#00FF00"))
            self.top.after(2000, lambda: self.set_speed(0)) 
            self.top.after(0, lambda: self.canvas.itemconfig(self.center_text, text="Done", fill="#00FF00"))
            self.top.after(0, lambda: self.canvas.itemconfig(self.unit_text, text=""))
            self.top.after(0, lambda: self.canvas.itemconfig(self.needle, fill="#00FF00"))
            self.needle_color = "#00FF00"
            
        except Exception as e:
            self.top.after(0, lambda: self.status_lbl.config(text=f"Error: Check Internet Connection", fg="red"))


class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        bg_color = 'black'
        self.root.configure(bg=bg_color)
        self.root.attributes('-transparentcolor', bg_color)

        x, y = self.load_position()
        self.root.geometry(f"110x35+{x}+{y}")

        self.net_io = psutil.net_io_counters()
        self.old_recv = self.net_io.bytes_recv
        self.old_sent = self.net_io.bytes_sent

        font_style = ("Consolas", 10, "bold")

        self.lbl_dl = tk.Label(root, text="D: 0.0 B/s", font=font_style, fg="#00FF00", bg=bg_color)
        self.lbl_dl.pack(anchor="w", padx=5)

        self.lbl_ul = tk.Label(root, text="U: 0.0 B/s", font=font_style, fg="#FFA500", bg=bg_color)
        self.lbl_ul.pack(anchor="w", padx=5)

        self.auto_run_var = tk.BooleanVar(value=self.check_autorun())
        self.menu = tk.Menu(self.root, tearoff=0)
        
        self.menu.add_command(label="Speed Test", command=self.open_speedtest_window)
        self.menu.add_separator()
        self.menu.add_checkbutton(label="Auto-Run", variable=self.auto_run_var, command=self.toggle_autorun)
        self.menu.add_separator()
        self.menu.add_command(label="About", command=self.show_about)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.exit_app)

        for lbl in (self.lbl_dl, self.lbl_ul):
            lbl.bind('<Button-1>', self.start_move)
            lbl.bind('<B1-Motion>', self.do_move)
            lbl.bind('<ButtonRelease-1>', self.save_position)
            lbl.bind('<Button-3>', self.show_menu)

        self.update_speed()

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("About")
        about_win.geometry("350x260")
        about_win.configure(bg="#1E1E1E")
        about_win.attributes('-topmost', True)
        
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        about_win.geometry(f"+{int(sw/2 - 175)}+{int(sh/2 - 130)}")

        tk.Label(about_win, text="NetSpeed Monitor Pro", font=("Arial", 16, "bold"), fg="#00BFFF", bg="#1E1E1E").pack(pady=(20, 2))
        tk.Label(about_win, text="Version 1.0.0", font=("Consolas", 10), fg="#7F8C8D", bg="#1E1E1E").pack(pady=(0, 15))
        
        tk.Label(about_win, text="Developer: Eng Ahmed Abdelaziz", font=("Arial", 11, "bold"), fg="white", bg="#1E1E1E").pack(pady=2)

        def create_selectable_text(parent, text_content, font_style, text_color):
            entry = tk.Entry(parent, font=font_style, fg=text_color, bg="#1E1E1E", 
                             readonlybackground="#1E1E1E", relief="flat", justify="center")
            entry.insert(0, text_content)
            entry.configure(state="readonly") 
            entry.pack(pady=2, fill="x", padx=10)
            return entry

        create_selectable_text(about_win, "Email: eng.ahmed.abdelaziz.2022@gmail.com", ("Consolas", 10), "#A9A9A9")
        create_selectable_text(about_win, "Phone: 01024735044", ("Consolas", 10), "#A9A9A9")
        
        tk.Label(about_win, text="© 2026 All Rights Reserved", font=("Arial", 8), fg="#555555", bg="#1E1E1E").pack(pady=(15, 5))

        tk.Button(about_win, text="Close", command=about_win.destroy, bg="#333333", fg="white", 
                  width=15, relief="flat", font=("Arial", 9, "bold")).pack(pady=5)

    def open_speedtest_window(self):
        if speedtest is None:
            tk.messagebox.showerror("Missing Library", "Please install speedtest library using:\npip install speedtest-cli")
            return
        SpeedTestWindow(self.root)

    def get_app_path(self):
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            return os.path.abspath(sys.argv[0])

    def check_autorun(self):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(registry_key, APP_NAME)
            winreg.CloseKey(registry_key)
            return value == self.get_app_path()
        except WindowsError:
            return False

    def toggle_autorun(self):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
            if self.auto_run_var.get():
                winreg.SetValueEx(registry_key, APP_NAME, 0, winreg.REG_SZ, self.get_app_path())
            else:
                winreg.DeleteValue(registry_key, APP_NAME)
            winreg.CloseKey(registry_key)
        except WindowsError:
            pass

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def load_position(self):
        try:
            if os.path.exists(POS_FILE):
                with open(POS_FILE, "r") as f:
                    coords = f.read().split(',')
                    if len(coords) == 2:
                        return int(coords[0]), int(coords[1])
        except Exception:
            pass
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        return screen_width - 250, screen_height - 50

    def save_position(self, event):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        try:
            with open(POS_FILE, "w") as f:
                f.write(f"{x},{y}")
        except Exception:
            pass

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def exit_app(self):
        self.root.destroy()

    def update_speed(self):
        self.root.attributes('-topmost', True)

        net_io = psutil.net_io_counters()
        new_recv = net_io.bytes_recv
        new_sent = net_io.bytes_sent

        dl_speed = new_recv - self.old_recv
        ul_speed = new_sent - self.old_sent

        self.lbl_dl.config(text=f"D: {format_speed(dl_speed)}")
        self.lbl_ul.config(text=f"U: {format_speed(ul_speed)}")

        self.old_recv = new_recv
        self.old_sent = new_sent

        self.root.after(1000, self.update_speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()