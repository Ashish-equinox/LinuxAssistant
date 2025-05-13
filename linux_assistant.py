# Statix code
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
import psutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import calendar
import datetime
from pathlib import Path

# Set up or locate the log file in the current working directory

def get_log_file():
    path = Path.cwd() / 'log.txt'
    path.touch(exist_ok=True)
    return path
LOG_FILE = get_log_file()

# Define themes with color schemes

themes = {
    "Dark":   {"bg":"#1e1e2e","panel":"#2e2e3e","fg":"#d8dee9","colors":["#88c0d0","#81a1c1","#bf616a"]},
    "Light":  {"bg":"#f0f0f0","panel":"#ffffff","fg":"#2e3440","colors":["#5e81ac","#a3be8c","#b48ead"]},
    "Hacker": {"bg":"#000000","panel":"#101010","fg":"#00ff00","colors":["#00ff00","#00cc00","#009900"]},
    "Glass":  {"bg":"#e0f7fa","panel":"#ffffff","fg":"#37474f","colors":["#00838f","#4db6ac","#006064"]},
}

class LinuxAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configure main window
        self.title("Linux Assistant")
        self.geometry("1100x800")
        self.minsize(900,700)
        self.current_theme = "Dark"

        # Buffers for historical CPU/RAM usage
        self.cpu_history = deque([0]*60, maxlen=60)
        self.ram_history = deque([0]*60, maxlen=60)

        # Build and apply UI
        self._setup_styles()
        self._build_ui()
        self._apply_theme(self.current_theme)
        self.after(500, self._update_chart)

    def _log(self, message):
        """Append a timestamped message to the log file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} - {message}\n")

    def _setup_styles(self):
        # Define custom ttk styles
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Bold.TButton', font=("Segoe UI", 11, "bold"))

    def _build_ui(self):
        # Create split panes for navigation and display
        paned = ttk.PanedWindow(self, orient='horizontal')
        paned.pack(fill='both', expand=True)

        # Left pane: theme selector and operation buttons
        left = ttk.Frame(paned, width=220)
        left.pack_propagate(False)
        paned.add(left, weight=0)

        theme_combo = ttk.Combobox(
            left, values=list(themes.keys()), state='readonly',
            font=("Segoe UI",11,"bold")
        )
        theme_combo.set(self.current_theme)
        theme_combo.pack(fill='x', padx=10, pady=10)
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_theme(theme_combo.get()))

        # Map button labels to their handlers
        ops = [
            ("CPU Usage", self.op_cpu_usage),
            ("Memory Usage", self.op_memory_usage),
            ("Disk Usage", self.op_disk_usage),
            ("Network Info", self.op_network_info),
            ("Create File", self.op_create_file),
            ("Create Dir", self.op_create_dir),
            ("Delete File", self.op_delete_file),
            ("Delete Dir", self.op_delete_dir),
            ("Reboot", self.op_reboot),
            ("Calendar", self.op_calendar),
            ("Exit", self.op_exit),
        ]
        for txt, cmd in ops:
            btn = ttk.Button(left, text=txt, command=cmd, style='Bold.TButton')
            btn.pack(fill='x', padx=10, pady=6)

        # Right pane: charts, legend, and terminal
        right = ttk.Frame(paned)
        paned.add(right, weight=1)

        header = ttk.Label(right, text="Resource Usage", font=("Segoe UI",16,"bold"))
        header.pack(anchor='w', padx=20, pady=(20,10))

        # Frame for donut and line charts
        charts_frame = ttk.Frame(right)
        charts_frame.pack(fill='x', padx=20)

        # Multi-ring donut chart setup
        self.fig, self.ax = plt.subplots(figsize=(5,5), dpi=100)
        self.ax.axis('equal')
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(side='left', fill='both', expand=True)

        # Line chart for historical data
        self.line_fig, self.line_ax = plt.subplots(figsize=(6,5), dpi=100)
        self.line_ax.set_ylim(0,100)
        self.line_ax.set_xlabel("Samples", fontweight='bold')
        self.line_ax.set_ylabel("% Usage", fontweight='bold')
        self.line_ax.tick_params(labelsize=8)
        self.line_ax.grid(True, linestyle='--', alpha=0.5)
        self.line_canvas = FigureCanvasTkAgg(self.line_fig, master=charts_frame)
        self.line_canvas.get_tk_widget().pack(side='left', fill='both', expand=True, padx=(20,0))

        # Legend labels for current values
        legend = ttk.Frame(right)
        legend.pack(pady=(15,10))
        self.legend_labels = {}
        for label in ['CPU','RAM','Disk']:
            lbl = ttk.Label(legend, text=f"{label}: 0.0%", font=("Segoe UI",11,"bold"))
            lbl.pack(side='left', padx=25)
            self.legend_labels[label] = lbl

        # Terminal output area
        term_label = ttk.Label(right, text="Terminal", font=("Segoe UI",14,"bold"))
        term_label.pack(anchor='w', padx=20, pady=(10,5))
        self.term = scrolledtext.ScrolledText(right, height=14, state='disabled', font=("Consolas",11,"bold"))
        self.term.pack(fill='both', expand=True, padx=20, pady=(0,15))

    def _apply_theme(self, theme_name):
        # Apply the selected theme to all UI elements and charts
        self.current_theme = theme_name
        th = themes[theme_name]
        self.configure(bg=th['bg'])
        style = ttk.Style(self)
        style.configure('TFrame', background=th['panel'])
        style.configure('TLabel', background=th['panel'], foreground=th['fg'], font=("Segoe UI",11,"bold"))
        style.configure('Bold.TButton', background=th['colors'][0], foreground=th['bg'], font=("Segoe UI",11,"bold"))
        style.map('Bold.TButton', background=[('active', th['colors'][1])])

        # Update chart backgrounds
        self.fig.patch.set_facecolor(th['panel'])
        self.ax.set_facecolor(th['panel'])
        self.line_fig.patch.set_facecolor(th['panel'])
        self.line_ax.set_facecolor(th['panel'])
        for txt in (self.line_ax.get_xticklabels() + self.line_ax.get_yticklabels()):
            txt.set_color(th['fg'])
            txt.set_fontweight('bold')
        self.line_ax.xaxis.label.set_color(th['fg'])
        self.line_ax.yaxis.label.set_color(th['fg'])

        # Style terminal
        self.term.configure(bg=th['panel'], fg=th['fg'], insertbackground=th['fg'])
        self.canvas.draw_idle()
        self.line_canvas.draw_idle()

    # ==== Operation methods (button callbacks) ====

    def op_cpu_usage(self):
        # Display CPU usage via shell command
        self._run_cmd("top -bn1 | grep 'Cpu(s)'")

    def op_memory_usage(self):
        # Display memory usage
        self._run_cmd("free -m")

    def op_disk_usage(self):
        # Display disk usage
        self._run_cmd("df -h")

    def op_network_info(self):
        # Display network interfaces summary
        self._run_cmd("ip -brief addr")

    def op_create_file(self):
        # Prompt and create a new empty file
        p = simpledialog.askstring('Create File','Enter File name:')
        if p:
            open(p,'a').close()
            self._log(f"File created: {p}")
            messagebox.showinfo('Created', p)

    def op_create_dir(self):
        # Prompt and create a new directory
        p = simpledialog.askstring('Create Dir','Enter Directory name:')
        if p:
            os.makedirs(p, exist_ok=True)
            self._log(f"Directory created: {p}")
            messagebox.showinfo('Created', p)

    def op_delete_file(self):
        # Prompt and delete an existing file
        p = simpledialog.askstring('Delete File','Enter File name:')
        if p and os.path.isfile(p):
            os.remove(p)
            self._log(f"File deleted: {p}")
            messagebox.showinfo('Deleted', p)

    def op_delete_dir(self):
        # Prompt and delete an existing directory
        p = simpledialog.askstring('Delete Dir','Enter Directory name:')
        if p and os.path.isdir(p):
            os.rmdir(p)
            self._log(f"Directory deleted: {p}")
            messagebox.showinfo('Deleted', p)

    def op_reboot(self):
        # Confirm and reboot the system
        if messagebox.askyesno('Confirm','Reboot now?'):
            self._run_cmd("reboot")

    def op_calendar(self):
        # Show a popup calendar for the current month
        now = datetime.datetime.now()
        cal_str = calendar.month(now.year, now.month)
        win = tk.Toplevel(self)
        win.title('Calendar')
        txt = scrolledtext.ScrolledText(win, width=20, height=8, font=("Consolas",12))
        txt.pack(padx=10, pady=10)
        txt.insert('end', cal_str)
        txt.configure(state='disabled')

    def op_exit(self):
        # Exit the application cleanly
        self.destroy()

    def _run_cmd(self, cmd):
        # Run a shell command in a background thread and show output
        def worker():
            self.term.configure(state='normal')
            self.term.delete('1.0','end')
            self.term.insert('end', f"$ {cmd}\n")
            try:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                out = res.stdout or res.stderr or ""
                self.term.insert('end', out + "\n")
            except Exception as e:
                self.term.insert('end', f"Error: {e}\n")
            self.term.configure(state='disabled')
            self.term.see('end')
        threading.Thread(target=worker, daemon=True).start()

    def _update_chart(self):
        # Refresh charts with latest CPU, RAM, and Disk metrics
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        self.ax.clear()
        th = themes[self.current_theme]
        size = 0.3
        for i,(val,col,key) in enumerate([(cpu, th['colors'][0], 'CPU'),(ram, th['colors'][1], 'RAM'),(disk, th['colors'][2], 'Disk')]):
            wedges,_ = self.ax.pie([val, 100-val], radius=1-i*size, colors=[col, th['panel']], wedgeprops=dict(width=size, edgecolor=th['bg'], linewidth=4), startangle=90)
            ang = (wedges[0].theta2 + wedges[0].theta1) / 2
            x = 0.6*(1-i*size) * np.cos(np.deg2rad(ang))
            y = 0.6*(1-i*size) * np.sin(np.deg2rad(ang))
            self.ax.text(x, y, f"{val:.1f}%", ha='center', va='center', color=th['fg'], fontweight='bold')
            self.legend_labels[key].config(text=f"{key}: {val:.1f}%")
        self.canvas.draw_idle()
        self.cpu_history.append(cpu)
        self.ram_history.append(ram)
        self.line_ax.clear()
        self.line_ax.plot(self.cpu_history, label='CPU', linewidth=2)
        self.line_ax.plot(self.ram_history, label='RAM', linewidth=2)
        self.line_ax.set_ylim(0,100)
        self.line_ax.legend(loc='upper right', fontsize=9, facecolor=th['panel'], labelcolor=th['fg'])
        self.line_ax.tick_params(colors=th['fg'])
        self.line_canvas.draw_idle()
        self.after(1000, self._update_chart)

if __name__ == '__main__':
    LinuxAssistant().mainloop()
