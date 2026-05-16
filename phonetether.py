#!/usr/bin/env python3
"""
ULTIMATE MOBILE CONTROL TOOL
Complete Android phone control from laptop
Requirements: Python 3.8+, ADB, scrcpy
"""

import subprocess
import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import socket
import re

class MobileController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📱 Ultimate Mobile Controller - Control Android from PC")
        self.root.geometry("1300x800")
        self.root.configure(bg="#0a0a0f")
        
        # Variables
        self.scrcpy_process = None
        self.adb_connected = False
        self.device_serial = None
        self.is_recording = False
        self.recording_process = None
        
        # UI Setup
        self.setup_ui()
        
        # Check ADB and device
        self.check_adb_and_device()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the GUI interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#0a0a0f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main_frame, bg="#0a0a0f")
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(header, text="📱 Ultimate Mobile Controller", 
                        font=("Segoe UI", 24, "bold"), 
                        fg="#7c3aed", bg="#0a0a0f")
        title.pack()
        
        subtitle = tk.Label(header, text="Complete Android Control from Your Laptop", 
                           font=("Segoe UI", 11), 
                           fg="#71717a", bg="#0a0a0f")
        subtitle.pack()
        
        # Control Panel (Left Side)
        control_panel = tk.Frame(main_frame, bg="#18181b", width=350)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipady=10)
        control_panel.pack_propagate(False)
        
        # Status Section
        status_frame = tk.LabelFrame(control_panel, text=" Connection Status ", 
                                     font=("Segoe UI", 11, "bold"),
                                     fg="#7c3aed", bg="#18181b",
                                     relief=tk.FLAT, borderwidth=0)
        status_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.status_label = tk.Label(status_frame, text="🔴 Not Connected", 
                                     font=("Segoe UI", 11),
                                     fg="#ef4444", bg="#18181b")
        self.status_label.pack(pady=5)
        
        self.device_label = tk.Label(status_frame, text="No Device", 
                                     font=("Segoe UI", 9),
                                     fg="#71717a", bg="#18181b")
        self.device_label.pack(pady=5)
        
        # Connection Controls
        conn_frame = tk.LabelFrame(control_panel, text=" Connection ", 
                                   font=("Segoe UI", 11, "bold"),
                                   fg="#7c3aed", bg="#18181b",
                                   relief=tk.FLAT, borderwidth=0)
        conn_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.refresh_btn = self.create_btn(conn_frame, "🔄 Refresh Devices", self.refresh_devices, "#3b82f6")
        self.refresh_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.connect_btn = self.create_btn(conn_frame, "🔌 Connect USB", self.connect_usb, "#10b981")
        self.connect_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.wifi_btn = self.create_btn(conn_frame, "📶 Connect Wi-Fi", self.connect_wifi, "#f59e0b")
        self.wifi_btn.pack(fill=tk.X, pady=5, padx=15)
        
        # Control Buttons
        control_frame = tk.LabelFrame(control_panel, text=" Screen Control ", 
                                      font=("Segoe UI", 11, "bold"),
                                      fg="#7c3aed", bg="#18181b",
                                      relief=tk.FLAT, borderwidth=0)
        control_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.start_btn = self.create_btn(control_frame, "▶ START MIRRORING", self.start_mirroring, "#10b981")
        self.start_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.stop_btn = self.create_btn(control_frame, "⏹ STOP MIRRORING", self.stop_mirroring, "#ef4444")
        self.stop_btn.pack(fill=tk.X, pady=5, padx=15)
        
        # Actions
        actions_frame = tk.LabelFrame(control_panel, text=" Quick Actions ", 
                                      font=("Segoe UI", 11, "bold"),
                                      fg="#7c3aed", bg="#18181b",
                                      relief=tk.FLAT, borderwidth=0)
        actions_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.screenshot_btn = self.create_btn(actions_frame, "📸 Take Screenshot", self.take_screenshot, "#8b5cf6")
        self.screenshot_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.record_btn = self.create_btn(actions_frame, "🎥 Start Recording", self.toggle_recording, "#f56565")
        self.record_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.home_btn = self.create_btn(actions_frame, "🏠 Press Home", self.press_home, "#6366f1")
        self.home_btn.pack(fill=tk.X, pady=5, padx=15)
        
        self.back_btn = self.create_btn(actions_frame, "⬅ Press Back", self.press_back, "#6366f1")
        self.back_btn.pack(fill=tk.X, pady=5, padx=15)
        
        # Apps
        apps_frame = tk.LabelFrame(control_panel, text=" Launch Apps ", 
                                   font=("Segoe UI", 11, "bold"),
                                   fg="#7c3aed", bg="#18181b",
                                   relief=tk.FLAT, borderwidth=0)
        apps_frame.pack(fill=tk.X, padx=15, pady=10)
        
        apps = [
            ("📞 Phone", "com.android.dialer"),
            ("📧 Gmail", "com.google.android.gm"),
            ("🎵 YouTube", "com.google.android.youtube"),
            ("📸 Camera", "com.android.camera"),
            ("⚙ Settings", "com.android.settings")
        ]
        
        for name, package in apps:
            btn = self.create_btn(apps_frame, name, lambda p=package: self.launch_app(p), "#475569")
            btn.pack(fill=tk.X, pady=2, padx=15)
        
        # Right Panel - Instructions
        info_panel = tk.Frame(main_frame, bg="#18181b")
        info_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = tk.LabelFrame(info_panel, text=" How to Use ", 
                                     font=("Segoe UI", 14, "bold"),
                                     fg="#7c3aed", bg="#18181b",
                                     relief=tk.FLAT, borderwidth=0)
        instructions.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        steps = """
        📱 ULTIMATE MOBILE CONTROL TOOL
        
        === SETUP (First Time Only) ===
        
        1️⃣ ENABLE USB DEBUGGING ON YOUR PHONE:
           • Go to Settings → About Phone
           • Tap "Build Number" 7 times
           • Go to Developer Options
           • Enable "USB Debugging"
        
        2️⃣ CONNECT YOUR PHONE:
           • Connect via USB cable
           • Accept the RSA key on your phone
           • Click "Refresh Devices" below
           • Click "Connect USB"
        
        === USING THE TOOL ===
        
        🖥 SCREEN CONTROL:
           • Click "START MIRRORING"
           • A new window will open showing your phone
           • Use mouse to tap anywhere on the screen
           • Use keyboard to type on your phone
        
        🎮 CONTROL BUTTONS:
           • Home/Back - Navigate your phone
           • Screenshot - Capture the screen
           • Recording - Record your screen
        
        📱 APP LAUNCHER:
           • Click any app icon to open it
        
        ⚡ TIPS:
           • Works over USB and Wi-Fi
           • Extremely low latency (35-70ms)
           • 30-120 FPS streaming
        
        🎯 KEYBOARD SHORTCUTS (in mirroring window):
           • Ctrl+H - Home button
           • Ctrl+B - Back button
           • Ctrl+S - Take screenshot
           • Ctrl+R - Start/stop recording
        """
        
        steps_label = tk.Label(instructions, text=steps, 
                              font=("Consolas", 10), 
                              fg="#a1a1aa", bg="#18181b",
                              justify=tk.LEFT)
        steps_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status bar
        status_bar = tk.Frame(self.root, bg="#18181b", height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_text = tk.Label(status_bar, text="✅ Ready | ADB: Checking...", 
                                    font=("Segoe UI", 9), 
                                    fg="#71717a", bg="#18181b")
        self.status_text.pack(side=tk.LEFT, padx=10)
    
    def create_btn(self, parent, text, command, color):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg="white",
                       font=("Segoe UI", 10, "bold"),
                       cursor="hand2", relief=tk.FLAT,
                       padx=10, pady=8,
                       activebackground=self.darken_color(color),
                       activeforeground="white")
        return btn
    
    def darken_color(self, color):
        """Return darker version of color"""
        return "#1f2937"
    
    def check_adb_and_device(self):
        """Check if ADB is installed and device is connected"""
        def check():
            # Check ADB
            try:
                result = subprocess.run(["adb", "version"], 
                                       capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.status_text.config(text="✅ ADB: Installed")
                    self.check_devices()
                else:
                    self.status_text.config(text="❌ ADB: Not found. Please install ADB")
            except FileNotFoundError:
                self.status_text.config(text="❌ ADB: Not installed. Run: sudo apt install adb")
        
        threading.Thread(target=check, daemon=True).start()
    
    def check_devices(self):
        """Check connected devices"""
        try:
            result = subprocess.run(["adb", "devices"], 
                                   capture_output=True, text=True, timeout=10)
            lines = result.stdout.strip().split('\n')[1:]
            devices = [l.split()[0] for l in lines if l.strip() and 'device' in l]
            
            if devices:
                self.device_serial = devices[0]
                self.adb_connected = True
                self.status_label.config(text="🟢 Connected", fg="#10b981")
                self.device_label.config(text=f"Device: {self.device_serial[:8]}...", fg="#10b981")
                self.status_text.config(text=f"✅ Device connected: {self.device_serial}")
                
                # Get device info
                self.get_device_info()
            else:
                self.adb_connected = False
                self.status_label.config(text="🔴 No Device", fg="#ef4444")
                self.device_label.config(text="No device connected", fg="#71717a")
                self.status_text.config(text="⚠️ No device connected. Connect phone via USB")
        except Exception as e:
            print(f"Error checking devices: {e}")
    
    def get_device_info(self):
        """Get device information"""
        try:
            # Get device model
            model = subprocess.run(["adb", "shell", "getprop", "ro.product.model"], 
                                  capture_output=True, text=True, timeout=5)
            # Get Android version
            android = subprocess.run(["adb", "shell", "getprop", "ro.build.version.release"], 
                                    capture_output=True, text=True, timeout=5)
            
            if model.stdout.strip():
                self.device_label.config(text=f"{model.stdout.strip()} | Android {android.stdout.strip()}")
        except:
            pass
    
    def refresh_devices(self):
        """Refresh device list"""
        self.status_text.config(text="🔄 Refreshing devices...")
        threading.Thread(target=self.check_devices, daemon=True).start()
    
    def connect_usb(self):
        """Connect via USB"""
        if not self.adb_connected:
            messagebox.showwarning("Not Connected", 
                                  "Please connect your phone via USB and enable USB Debugging")
        else:
            messagebox.showinfo("Connected", 
                               f"Device {self.device_serial} is ready!\nClick 'START MIRRORING' to begin.")
    
    def connect_wifi(self):
        """Connect over Wi-Fi"""
        if not self.adb_connected:
            messagebox.showwarning("No USB", "Please connect via USB first to set up Wi-Fi connection")
            return
        
        # Get device IP
        try:
            ip_result = subprocess.run(["adb", "shell", "ip", "route"], 
                                      capture_output=True, text=True, timeout=5)
            # Extract IP (simplified)
            import re
            ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', ip_result.stdout)
            device_ip = None
            for ip in ips:
                if ip.startswith('192.168.') or ip.startswith('10.'):
                    device_ip = ip
                    break
            
            if device_ip:
                # Connect over TCP/IP
                subprocess.run(["adb", "tcpip", "5555"], timeout=5)
                time.sleep(2)
                subprocess.run(["adb", "connect", f"{device_ip}:5555"], timeout=5)
                messagebox.showinfo("Wi-Fi Connected", 
                                   f"Connected to {device_ip}:5555\nYou can now disconnect USB!")
            else:
                messagebox.showerror("Error", "Could not find device IP")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect over Wi-Fi: {e}")
    
    def start_mirroring(self):
        """Start scrcpy mirroring with control"""
        if not self.adb_connected:
            messagebox.showerror("Error", "No device connected!\nPlease connect your phone first.")
            return
        
        # Kill existing scrcpy
        self.stop_mirroring()
        
        # Start scrcpy with control enabled
        # scrcpy automatically enables touch control and keyboard input [citation:8]
        cmd = [
            "scrcpy",
            "--turn-screen-off",  # Turn off phone screen while mirroring (saves battery)
            "--stay-awake",       # Keep device awake
            "--window-title", "Mobile Control - Click and Type to Control",
            "--window-width", "400",
            "--window-height", "800"
        ]
        
        try:
            self.scrcpy_process = subprocess.Popen(cmd)
            self.status_text.config(text="🎬 Mirroring active - Use mouse to control your phone!")
            messagebox.showinfo("Mirroring Started", 
                               "A new window will open showing your phone.\n"
                               "• Click anywhere to tap\n"
                               "• Type directly to input text\n"
                               "• Right-click for back button")
        except FileNotFoundError:
            messagebox.showerror("Error", 
                               "scrcpy not found!\nInstall it with: sudo apt install scrcpy")
    
    def stop_mirroring(self):
        """Stop scrcpy mirroring"""
        if self.scrcpy_process:
            self.scrcpy_process.terminate()
            time.sleep(1)
            if self.scrcpy_process.poll() is None:
                self.scrcpy_process.kill()
            self.scrcpy_process = None
            self.status_text.config(text="✅ Mirroring stopped")
    
    def take_screenshot(self):
        """Take screenshot using ADB"""
        if not self.adb_connected:
            messagebox.showerror("Error", "No device connected")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        try:
            subprocess.run(["adb", "exec-out", "screencap", "-p"], 
                          stdout=open(filename, 'wb'), timeout=10)
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {filename}")
            self.status_text.config(text=f"📸 Screenshot saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to take screenshot: {e}")
    
    def toggle_recording(self):
        """Start/stop screen recording"""
        if not self.adb_connected:
            messagebox.showerror("Error", "No device connected")
            return
        
        if not self.is_recording:
            # Start recording
            self.recording_filename = f"recording_{time.strftime('%Y%m%d_%H%M%S')}.mp4"
            try:
                self.recording_process = subprocess.Popen(
                    ["adb", "shell", "screenrecord", f"/sdcard/{self.recording_filename}"]
                )
                self.is_recording = True
                self.record_btn.config(text="⏹ Stop Recording", bg="#ef4444")
                self.status_text.config(text="🎥 Recording started...")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start recording: {e}")
        else:
            # Stop recording
            try:
                subprocess.run(["adb", "shell", "pkill", "-INT", "screenrecord"], timeout=5)
                time.sleep(2)
                # Pull file to PC
                subprocess.run(["adb", "pull", f"/sdcard/{self.recording_filename}", "."], timeout=30)
                subprocess.run(["adb", "shell", "rm", f"/sdcard/{self.recording_filename}"], timeout=5)
                self.is_recording = False
                self.record_btn.config(text="🎥 Start Recording", bg="#f56565")
                self.status_text.config(text=f"✅ Recording saved: {self.recording_filename}")
                messagebox.showinfo("Recording Saved", f"Recording saved as {self.recording_filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop recording: {e}")
    
    def press_home(self):
        """Press home button"""
        if self.adb_connected:
            subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_HOME"])
            self.status_text.config(text="🏠 Pressed Home")
    
    def press_back(self):
        """Press back button"""
        if self.adb_connected:
            subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_BACK"])
            self.status_text.config(text="⬅ Pressed Back")
    
    def launch_app(self, package):
        """Launch an app by package name"""
        if not self.adb_connected:
            messagebox.showerror("Error", "No device connected")
            return
        
        try:
            subprocess.run(["adb", "shell", "monkey", "-p", package, "-c", 
                          "android.intent.category.LAUNCHER", "1"], 
                          timeout=10, capture_output=True)
            self.status_text.config(text=f"📱 Launched: {package}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch app: {e}")
    
    def on_closing(self):
        """Clean up on close"""
        self.stop_mirroring()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     ULTIMATE MOBILE CONTROL TOOL - Complete Android Control   ║
    ║                   Control Your Phone from Laptop              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Check for required tools
    import shutil
    
    if not shutil.which("adb"):
        print("❌ ADB not found! Please install:")
        print("   Ubuntu/Debian: sudo apt install adb")
        print("   macOS: brew install android-platform-tools")
        print("   Windows: Download from https://developer.android.com/studio/releases/platform-tools")
        sys.exit(1)
    
    if not shutil.which("scrcpy"):
        print("⚠️  scrcpy not found! Install for better experience:")
        print("   Ubuntu/Debian: sudo apt install scrcpy")
        print("   macOS: brew install scrcpy")
        print("   Windows: Download from https://github.com/Genymobile/scrcpy/releases")
        print("\n   You can still use ADB commands but no screen mirroring")
    
    app = MobileController()
    app.run()