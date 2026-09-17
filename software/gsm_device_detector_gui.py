#!/usr/bin/env python3
# GSM Fix Hub - Auto Mobile Device Mode Detector & Web Linker (GUI Edition)
# Lead Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
# Portal: https://www.gsmfixhub.com/ | https://bhuwanbastola.com.np/

import os, sys, time, subprocess, re, webbrowser, threading, json
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except ImportError:
    print("[!] Tkinter not installed. On Windows, Tkinter comes with standard Python 3.")
    sys.exit(1)

DEFAULT_PORTAL_URL = "https://www.gsmfixhub.com"
LOCAL_PORTAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

DEVICE_SIGNATURES = [
    {
        "mode_id": "QC_EDL_9008",
        "name": "Qualcomm Snapdragon EDL 9008 Mode",
        "badge": "QUALCOMM EDL 9008",
        "color": "#ef4444",
        "bg_color": "#450a0a",
        "vid_pid": [("05C6", "9008"), ("05C6", "9006"), ("05C6", "9025")],
        "keywords": ["Qualcomm HS-USB QDLoader 9008", "QDLoader 9008", "Qualcomm HS-USB Diagnostics 9008"],
        "recommended_tool": "QFIL v2.0.3.5 / Mi Flash 2024 (QPST Suite)",
        "recommended_driver": "Qualcomm QDLoader HS-USB 9008 64-bit WHQL Driver",
        "hash_target": "#flashing-tools",
        "testpoint_target": "#testpoints",
        "guide": "Sahara Handshake Ready: Use Flat Build in QFIL with prog_firehose_ddr programmer."
    },
    {
        "mode_id": "MTK_BROM",
        "name": "MediaTek BootROM (BROM) Auth SLA Mode",
        "badge": "MTK BROM MODE",
        "color": "#f59e0b",
        "bg_color": "#451a03",
        "vid_pid": [("0E8D", "0003")],
        "keywords": ["MediaTek USB Port", "MTK USB Port"],
        "recommended_tool": "SP Flash Tool v5.2124 (Auth SLA Bypass Edition) / MTK Client GUI",
        "recommended_driver": "MTK Auto Driver v1.0.8 + LibUSB Win32 Filter Driver",
        "hash_target": "#flashing-tools",
        "testpoint_target": "#testpoints",
        "guide": "BROM Mode Active: Filter MediaTek USB port in LibUSB to bypass SLA/DAA authentication."
    },
    {
        "mode_id": "MTK_PRELOADER",
        "name": "MediaTek Preloader / VCOM Flashing Port",
        "badge": "MTK PRELOADER",
        "color": "#eab308",
        "bg_color": "#422006",
        "vid_pid": [("0E8D", "2000"), ("0E8D", "2001")],
        "keywords": ["MediaTek Preloader USB VCOM", "MediaTek DA USB VCOM", "MTK Preloader"],
        "recommended_tool": "SP Flash Tool v5.2124 / Maui META IMEI Repair",
        "recommended_driver": "MediaTek Auto Driver v1.0.8 (CDC / VCOM)",
        "hash_target": "#flashing-tools",
        "testpoint_target": "#testpoints",
        "guide": "Preloader Port Connected: Ready for scatter-based firmware write and NVRAM repair."
    },
    {
        "mode_id": "SAMSUNG_DOWNLOAD",
        "name": "Samsung Galaxy Download Mode (Odin / LOKE)",
        "badge": "SAMSUNG ODIN MODE",
        "color": "#38bdf8",
        "bg_color": "#082f49",
        "vid_pid": [("04E8", "685D"), ("04E8", "6860")],
        "keywords": ["SAMSUNG Mobile USB CDC Composite Device", "SAMSUNG Mobile USB Modem"],
        "recommended_tool": "Samsung Odin3 v3.14.4 Official (Patched 3B) / Frija Downloader",
        "recommended_driver": "Samsung Official Mobile USB Drivers v1.7.59.0 WHQL",
        "hash_target": "#flash-files",
        "testpoint_target": "#testpoints",
        "guide": "Samsung Download Mode Active: Load BL, AP, CP, CSC in Odin3 v3.14.4 to recover device."
    },
    {
        "mode_id": "FASTBOOT",
        "name": "Android Fastboot / Bootloader Mode",
        "badge": "FASTBOOT MODE",
        "color": "#06b6d4",
        "bg_color": "#083344",
        "vid_pid": [("18D1", "4EE0"), ("2717", "FF40"), ("22D4", "2769")],
        "keywords": ["Android Bootloader Interface", "Fastboot Device", "Xiaomi Fastboot"],
        "recommended_tool": "Xiaomi Mi Flash Tool 2024 / Android SDK Fastboot Engine",
        "recommended_driver": "Google / Xiaomi Fastboot WHQL USB Driver",
        "hash_target": "#flash-files",
        "testpoint_target": "#testpoints",
        "guide": "Bootloader Mode Active: Can query partition table, unlock bootloader, or flash fastboot ROM."
    },
    {
        "mode_id": "UNISOC_SPRD",
        "name": "Unisoc / Spreadtrum SCI USB2Serial Mode",
        "badge": "UNISOC / SPD PAC",
        "color": "#a855f7",
        "bg_color": "#3b0764",
        "vid_pid": [("1782", "4D00"), ("1782", "4D01")],
        "keywords": ["Spreadtrum SCI USB2Serial", "SPRD U2S Diag", "SPRD COM Port"],
        "recommended_tool": "SPD Research & Upgrade Download Tool R24.0.0003",
        "recommended_driver": "Unisoc / Spreadtrum SCI USB Drivers v2.0.0.1",
        "hash_target": "#flashing-tools",
        "testpoint_target": "#testpoints",
        "guide": "Spreadtrum PAC Download Mode: Hold Volume Down while connecting USB for full unbrick."
    },
    {
        "mode_id": "MTP_NORMAL",
        "name": "Normal Boot Mode (MTP File Transfer)",
        "badge": "MTP NORMAL OS",
        "color": "#10b981",
        "bg_color": "#022c22",
        "vid_pid": [("04E8", "6860"), ("2717", "FF40"), ("0E8D", "2008")],
        "keywords": ["MTP USB Device", "Media Transfer Protocol"],
        "recommended_tool": "Samsung Universal FRP Tool v4.9 (*#0*# Enabler) / GSM BFT Free Tool",
        "recommended_driver": "All-in-One Universal Driver Setup 2026",
        "hash_target": "#frp-bypass",
        "testpoint_target": "#testpoints",
        "guide": "Normal OS Mode Active: Use emergency dialer *#0*# on Samsung or MTP exploit for FRP bypass."
    },
    {
        "mode_id": "ADB_DEBUG",
        "name": "Android ADB Debugging / Recovery Mode",
        "badge": "ADB AUTHORIZED",
        "color": "#14b8a6",
        "bg_color": "#042f2e",
        "vid_pid": [("18D1", "4EE7"), ("2717", "FF48")],
        "keywords": ["Android Composite ADB Interface", "Android ADB Interface"],
        "recommended_tool": "GSM Fix Hub Console / SamFw ADB Tool",
        "recommended_driver": "Universal ADB & Fastboot Drivers 2026",
        "hash_target": "#frp-bypass",
        "testpoint_target": "#testpoints",
        "guide": "ADB Shell Authorized: 1-click reboot to EDL 9008, Bootloader, or Recovery available."
    }
]

class GSMDetectorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GSM Fix Hub — Auto Mobile Device Mode Detector & Web Linker Pro 2026")
        self.geometry("960x680")
        self.minsize(860, 600)
        self.configure(bg="#0b1329")

        self.auto_open_var = tk.BooleanVar(value=True)
        self.use_local_portal = tk.BooleanVar(value=True)
        self.monitoring = True
        self.current_device = None
        self.detected_history = set()

        self.setup_ui()
        self.log_event("Application initialized. GSM Fix Hub Device Detection Engine active.")
        self.log_event("Monitoring Windows USB PnP, COM Ports, ADB, and Fastboot interfaces...")

        self.watcher_thread = threading.Thread(target=self.hardware_watcher_loop, daemon=True)
        self.watcher_thread.start()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0f172a", height=70, highlightthickness=1, highlightbackground="#06b6d4")
        header.pack(fill=tk.X, side=tk.TOP)

        title_frame = tk.Frame(header, bg="#0f172a")
        title_frame.pack(side=tk.LEFT, padx=16, pady=12)

        lbl_app_name = tk.Label(title_frame, text="GSM FIX HUB PRO", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#0f172a")
        lbl_app_name.pack(side=tk.LEFT)
        lbl_badge = tk.Label(title_frame, text="AUTO-DETECTOR 2026", font=("Segoe UI", 9, "bold"), fg="#06b6d4", bg="#083344", padx=6, pady=2)
        lbl_badge.pack(side=tk.LEFT, padx=8)

        lbl_author = tk.Label(header, text="Lead Architect: Bhuwan Bastola | Gopal Electronics, Surkhet", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a")
        lbl_author.pack(side=tk.RIGHT, padx=16, pady=16)

        content_frame = tk.Frame(self, bg="#0b1329")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        left_panel = tk.Frame(content_frame, bg="#0b1329", width=520)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_panel = tk.Frame(content_frame, bg="#0b1329", width=380)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        card_border = tk.Frame(left_panel, bg="#1e293b", bd=1, relief=tk.SOLID)
        card_border.pack(fill=tk.X, pady=(0, 10))

        card_inner = tk.Frame(card_border, bg="#0f172a", padx=14, pady=12)
        card_inner.pack(fill=tk.X)

        top_status = tk.Frame(card_inner, bg="#0f172a")
        top_status.pack(fill=tk.X, pady=(0, 8))

        self.lbl_status_dot = tk.Label(top_status, text="●", font=("Segoe UI", 14), fg="#10b981", bg="#0f172a")
        self.lbl_status_dot.pack(side=tk.LEFT)

        self.lbl_status_text = tk.Label(top_status, text="MONITORING ACTIVE — WAITING FOR MOBILE USB CONNECTION", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#0f172a")
        self.lbl_status_text.pack(side=tk.LEFT, padx=6)

        self.lbl_mode_badge = tk.Label(card_inner, text="NO DEVICE CONNECTED", font=("Segoe UI", 13, "bold"), fg="#64748b", bg="#1e293b", padx=12, pady=8)
        self.lbl_mode_badge.pack(fill=tk.X, pady=6)

        attr_grid = tk.Frame(card_inner, bg="#0f172a")
        attr_grid.pack(fill=tk.X, pady=6)

        self.add_attr_row(attr_grid, 0, "Interface / Port:", "lbl_port", "None")
        self.add_attr_row(attr_grid, 1, "Detected Hardware:", "lbl_hw", "No USB Device")
        self.add_attr_row(attr_grid, 2, "Recommended Tool:", "lbl_tool", "SP Flash Tool / QFIL / Odin3")
        self.add_attr_row(attr_grid, 3, "Required Driver:", "lbl_driver", "WHQL Signed Drivers")

        self.lbl_guide = tk.Label(card_inner, text="Connect mobile phone via genuine USB data cable. Tool will automatically recognize mode.", font=("Segoe UI", 9, "italic"), fg="#94a3b8", bg="#0f172a", wraplength=480, justify=tk.LEFT)
        self.lbl_guide.pack(fill=tk.X, pady=(6, 4))

        link_card = tk.Frame(left_panel, bg="#0f172a", highlightthickness=1, highlightbackground="#334155", padx=14, pady=12)
        link_card.pack(fill=tk.X, pady=(0, 10))

        lbl_link_title = tk.Label(link_card, text="AUTOMATIC GSM FIX HUB WEB PORTAL LINKER", font=("Segoe UI", 11, "bold"), fg="#38bdf8", bg="#0f172a")
        lbl_link_title.pack(anchor="w", pady=(0, 6))

        cb_frame = tk.Frame(link_card, bg="#0f172a")
        cb_frame.pack(fill=tk.X, pady=4)

        chk_auto = tk.Checkbutton(cb_frame, text="Auto-Launch Portal in Browser when Phone Connects", variable=self.auto_open_var, font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#0f172a", selectcolor="#083344", activebackground="#0f172a", activeforeground="#38bdf8")
        chk_auto.pack(side=tk.LEFT)

        btn_frame1 = tk.Frame(link_card, bg="#0f172a")
        btn_frame1.pack(fill=tk.X, pady=(8, 4))

        self.btn_open_portal = tk.Button(btn_frame1, text="🌐 Open Matching Portal Section", font=("Segoe UI", 10, "bold"), bg="#06b6d4", fg="#020617", activebackground="#22d3ee", relief=tk.FLAT, padx=12, pady=6, cursor="hand2", command=self.open_current_web_link)
        self.btn_open_portal.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_open_pinout = tk.Button(btn_frame1, text="📌 View EDL Test Points", font=("Segoe UI", 9, "bold"), bg="#1e293b", fg="#38bdf8", activebackground="#334155", relief=tk.FLAT, padx=8, pady=6, cursor="hand2", command=lambda: self.open_portal_hash("#testpoints"))
        self.btn_open_pinout.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        btn_frame2 = tk.Frame(link_card, bg="#0f172a")
        btn_frame2.pack(fill=tk.X, pady=4)

        self.btn_open_video = tk.Button(btn_frame2, text="🎓 Watch Video Academy", font=("Segoe UI", 9, "bold"), bg="#1e293b", fg="#f43f5e", activebackground="#334155", relief=tk.FLAT, padx=8, pady=5, cursor="hand2", command=lambda: self.open_portal_hash("#video-tutorials"))
        self.btn_open_video.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_open_tools = tk.Button(btn_frame2, text="🛠️ Flashing Tools & Drivers", font=("Segoe UI", 9, "bold"), bg="#1e293b", fg="#10b981", activebackground="#334155", relief=tk.FLAT, padx=8, pady=5, cursor="hand2", command=lambda: self.open_portal_hash("#flashing-tools"))
        self.btn_open_tools.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        cmd_card = tk.Frame(left_panel, bg="#0f172a", highlightthickness=1, highlightbackground="#334155", padx=12, pady=10)
        cmd_card.pack(fill=tk.X)

        lbl_cmd_title = tk.Label(cmd_card, text="LABORATORY 1-CLICK DIAGNOSTIC SHORTCUTS", font=("Segoe UI", 10, "bold"), fg="#e2e8f0", bg="#0f172a")
        lbl_cmd_title.pack(anchor="w", pady=(0, 6))

        btn_cmd_grid = tk.Frame(cmd_card, bg="#0f172a")
        btn_cmd_grid.pack(fill=tk.X)

        tk.Button(btn_cmd_grid, text="Reboot to EDL (ADB)", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg="#ef4444", relief=tk.FLAT, pady=4, command=lambda: self.run_cli_command(["adb", "reboot", "edl"])).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Button(btn_cmd_grid, text="Reboot Bootloader", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg="#38bdf8", relief=tk.FLAT, pady=4, command=lambda: self.run_cli_command(["adb", "reboot", "bootloader"])).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        tk.Button(btn_cmd_grid, text="Fastboot Getvar All", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg="#22d3ee", relief=tk.FLAT, pady=4, command=lambda: self.run_cli_command(["fastboot", "getvar", "all"])).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        tk.Button(btn_cmd_grid, text="Reboot Recovery", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg="#a855f7", relief=tk.FLAT, pady=4, command=lambda: self.run_cli_command(["adb", "reboot", "recovery"])).grid(row=0, column=3, sticky="ew", padx=2, pady=2)

        for col in range(4):
            btn_cmd_grid.columnconfigure(col, weight=1)

        right_header = tk.Frame(right_panel, bg="#0b1329")
        right_header.pack(fill=tk.X, pady=(0, 6))

        lbl_log_title = tk.Label(right_header, text="REAL-TIME HARDWARE & EVENT LOG", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#0b1329")
        lbl_log_title.pack(side=tk.LEFT)

        btn_clear_log = tk.Button(right_header, text="Clear Log", font=("Segoe UI", 8), bg="#1e293b", fg="#94a3b8", relief=tk.FLAT, padx=6, pady=2, command=self.clear_log)
        btn_clear_log.pack(side=tk.RIGHT)

        self.txt_log = scrolledtext.ScrolledText(right_panel, bg="#020617", fg="#38bdf8", font=("Consolas", 9), bd=0, highlightthickness=1, highlightbackground="#1e293b", insertbackground="#38bdf8")
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        sim_card = tk.Frame(right_panel, bg="#0f172a", highlightthickness=1, highlightbackground="#334155", padx=10, pady=8)
        sim_card.pack(fill=tk.X)

        lbl_sim_title = tk.Label(sim_card, text="TECH TEST SIMULATOR (Test Detection & Web Linking)", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a")
        lbl_sim_title.pack(anchor="w", pady=(0, 4))

        sim_btns = tk.Frame(sim_card, bg="#0f172a")
        sim_btns.pack(fill=tk.X)

        tk.Button(sim_btns, text="Qualcomm 9008", font=("Segoe UI", 8), bg="#450a0a", fg="#fca5a5", relief=tk.FLAT, command=lambda: self.simulate_mode("QC_EDL_9008", "COM7 (Qualcomm HS-USB QDLoader 9008)")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(sim_btns, text="MTK BROM", font=("Segoe UI", 8), bg="#451a03", fg="#fcd34d", relief=tk.FLAT, command=lambda: self.simulate_mode("MTK_BROM", "COM5 (MediaTek USB Port)")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(sim_btns, text="Samsung Odin", font=("Segoe UI", 8), bg="#082f49", fg="#7dd3fc", relief=tk.FLAT, command=lambda: self.simulate_mode("SAMSUNG_DOWNLOAD", "SAMSUNG Mobile USB Composite Device")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(sim_btns, text="Fastboot", font=("Segoe UI", 8), bg="#083344", fg="#67e8f9", relief=tk.FLAT, command=lambda: self.simulate_mode("FASTBOOT", "Android Bootloader Interface (Poco X3 Pro)")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

    def add_attr_row(self, parent, row_idx, label_text, attr_name, default_val):
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a", width=18, anchor="w")
        lbl.grid(row=row_idx, column=0, sticky="w", pady=2)
        val = tk.Label(parent, text=default_val, font=("Segoe UI", 9), fg="#e2e8f0", bg="#0f172a", anchor="w")
        val.grid(row=row_idx, column=1, sticky="w", pady=2)
        setattr(self, attr_name, val)

    def log_event(self, text):
        now = datetime.now().strftime("%H:%M:%S")
        msg = f"[{now}] {text}\n"
        self.txt_log.insert(tk.END, msg)
        self.txt_log.see(tk.END)

    def clear_log(self):
        self.txt_log.delete("1.0", tk.END)
        self.log_event("Hardware event log cleared.")

    def run_cli_command(self, cmd_args):
        cmd_str = " ".join(cmd_args)
        self.log_event(f"Executing: {cmd_str}")
        try:
            res = subprocess.run(cmd_args, capture_output=True, text=True, timeout=5)
            output = (res.stdout + res.stderr).strip()
            if output:
                self.log_event(f"Output: {output}")
            else:
                self.log_event(f"Command '{cmd_str}' finished with exit code {res.returncode}")
        except Exception as e:
            self.log_event(f"Error running '{cmd_str}': {e}")

    def get_web_url_for_hash(self, hash_route):
        base = DEFAULT_PORTAL_URL
        if self.use_local_portal.get() and os.path.exists(LOCAL_PORTAL_PATH):
            base = "file:///" + LOCAL_PORTAL_PATH.replace(os.sep, "/")
        return f"{base}{hash_route}"

    def open_portal_hash(self, hash_route):
        url = self.get_web_url_for_hash(hash_route)
        self.log_event(f"Launching URL: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            self.log_event(f"Browser launch error: {e}")

    def open_current_web_link(self):
        if self.current_device and "web_link" in self.current_device:
            url = self.current_device["web_link"]
            self.log_event(f"Opening target link: {url}")
            webbrowser.open(url)
        else:
            self.open_portal_hash("#home")

    def simulate_mode(self, mode_id, mock_raw_name):
        sig = next((s for s in DEVICE_SIGNATURES if s["mode_id"] == mode_id), DEVICE_SIGNATURES[0])
        mock_dev = {
            "mode_name": sig["name"],
            "signature": sig,
            "raw_name": mock_raw_name,
            "com_port": "COM7" if "COM7" in mock_raw_name else ("COM5" if "COM5" in mock_raw_name else "USB"),
            "badge": sig["badge"]
        }
        self.on_device_detected(mock_dev)

    def on_device_detected(self, dev):
        sig = dev["signature"]
        web_link = self.get_web_url_for_hash(sig["hash_target"])
        dev["web_link"] = web_link
        self.current_device = dev

        self.lbl_status_dot.config(fg="#10b981")
        self.lbl_status_text.config(text=f"CONNECTED — {sig['badge']} DETECTED", fg="#10b981")
        
        self.lbl_mode_badge.config(
            text=f"{sig['badge']} — {sig['name'].upper()}",
            fg=sig["color"],
            bg=sig.get("bg_color", "#1e293b")
        )
        self.lbl_port.config(text=dev.get("com_port", "USB Interface"), fg="#38bdf8")
        self.lbl_hw.config(text=dev.get("raw_name", "Unknown"), fg="#ffffff")
        self.lbl_tool.config(text=sig["recommended_tool"], fg="#10b981")
        self.lbl_driver.config(text=sig["recommended_driver"], fg="#f59e0b")
        self.lbl_guide.config(text=sig["guide"], fg="#cbd5e1")

        self.log_event(f"Hardware Connected: {sig['name']} on {dev.get('com_port')}")
        self.log_event(f"Recommended Tool: {sig['recommended_tool']}")
        self.log_event(f"Auto-generated link: {web_link}")

        if self.auto_open_var.get():
            self.log_event("Auto-Launch enabled: Opening default browser to GSM Fix Hub...")
            try:
                webbrowser.open(web_link)
            except Exception as e:
                self.log_event(f"Failed to open browser: {e}")

    def on_device_disconnected(self):
        self.current_device = None
        self.lbl_status_dot.config(fg="#94a3b8")
        self.lbl_status_text.config(text="MONITORING ACTIVE — WAITING FOR MOBILE USB CONNECTION", fg="#94a3b8")
        self.lbl_mode_badge.config(text="NO DEVICE CONNECTED", fg="#64748b", bg="#1e293b")
        self.lbl_port.config(text="None", fg="#e2e8f0")
        self.lbl_hw.config(text="No USB Device", fg="#e2e8f0")
        self.lbl_tool.config(text="SP Flash Tool / QFIL / Odin3", fg="#e2e8f0")
        self.lbl_driver.config(text="WHQL Signed Drivers", fg="#e2e8f0")
        self.lbl_guide.config(text="Connect mobile phone via genuine USB data cable. Tool will automatically recognize mode.", fg="#94a3b8")
        self.log_event("Device disconnected. Ready for next mobile phone.")

    def hardware_watcher_loop(self):
        while self.monitoring:
            try:
                found = self.scan_devices()
                if found:
                    top = found[0]
                    key = f"{top['signature']['mode_id']}_{top.get('com_port')}"
                    if key not in self.detected_history:
                        self.detected_history.clear()
                        self.detected_history.add(key)
                        self.after(0, self.on_device_detected, top)
                else:
                    if self.current_device is not None:
                        self.detected_history.clear()
                        self.after(0, self.on_device_disconnected)
            except Exception as e:
                pass
            time.sleep(1.5)

    def scan_devices(self):
        found = []
        try:
            res = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=1)
            if res.returncode == 0 and res.stdout.strip():
                sig = next(s for s in DEVICE_SIGNATURES if s["mode_id"] == "FASTBOOT")
                serial = res.stdout.strip().split()[0]
                found.append({
                    "signature": sig,
                    "raw_name": f"Fastboot Interface ({serial})",
                    "com_port": "USB Fastboot",
                    "mode_name": sig["name"]
                })
                return found
        except Exception:
            pass

        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=1)
            if res.returncode == 0 and res.stdout.strip():
                lines = [l.strip() for l in res.stdout.strip().split("\n")[1:] if l.strip()]
                if lines:
                    line = lines[0]
                    state = line.split()[1] if len(line.split()) > 1 else "device"
                    mode_id = "ADB_DEBUG" if state == "device" else "MTP_NORMAL"
                    sig = next(s for s in DEVICE_SIGNATURES if s["mode_id"] == mode_id)
                    found.append({
                        "signature": sig,
                        "raw_name": f"ADB Device ({line.split()[0]})",
                        "com_port": "USB Debugging",
                        "mode_name": sig["name"]
                    })
                    return found
        except Exception:
            pass

        if sys.platform == "win32":
            try:
                ps_cmd = "Get-CimInstance Win32_PnPEntity | Where-Object { $_.DeviceID -like 'USB*' -or $_.Caption -like '*COM*' } | Select-Object Caption, DeviceID | ConvertTo-Json -Compress"
                res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=2)
                if res.returncode == 0 and res.stdout.strip():
                    items = json.loads(res.stdout.strip())
                    if isinstance(items, dict):
                        items = [items]
                    for it in items:
                        name = it.get("Caption") or ""
                        dev_id = it.get("DeviceID") or ""
                        for sig in DEVICE_SIGNATURES:
                            for kw in sig["keywords"]:
                                if kw.lower() in name.lower():
                                    com_m = re.search(r"\(COM\d+\)", name)
                                    com_p = com_m.group(0) if com_m else "USB Port"
                                    found.append({
                                        "signature": sig,
                                        "raw_name": name,
                                        "com_port": com_p,
                                        "mode_name": sig["name"]
                                    })
                                    return found
            except Exception:
                pass

        return found

if __name__ == "__main__":
    app = GSMDetectorGUI()
    app.mainloop()
