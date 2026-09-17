#!/usr/bin/env python3
"""
=============================================================================
GSM Fix Hub — Mobile Device Hardware Mode Detector & Web Linker (CLI Engine)
=============================================================================
Lead Architect & Developer: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
Official Portal: https://www.gsmfixhub.com/ | https://bhuwanbastola.com.np/
=============================================================================
Detects mobile devices in various hardware and flashing modes:
 - Qualcomm Emergency Download (EDL 9008)
 - MediaTek BootROM (BROM Auth SLA Bypass)
 - MediaTek Preloader & DA USB VCOM Port
 - Samsung Download / Odin Mode (LOKE)
 - Android Fastboot / Bootloader Mode
 - Android ADB Debugging / Recovery / Sideload Mode
 - Unisoc / Spreadtrum SCI USB2Serial Mode
 - MTP (Normal OS File Transfer) Mode
=============================================================================
"""

import os
import sys
import time
import subprocess
import re
import webbrowser
import json
import threading

DEFAULT_PORTAL_URL = "https://www.gsmfixhub.com"
LOCAL_PORTAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

# 8 Hardware Detection Profiles
DEVICE_SIGNATURES = [
    {
        "mode_id": "QC_EDL_9008",
        "name": "Qualcomm Snapdragon EDL 9008 Mode",
        "category": "Emergency Download (EDL)",
        "badge": "QUALCOMM 9008",
        "color": "RED",
        "vid_pid": [("05C6", "9008"), ("05C6", "9006"), ("05C6", "9025")],
        "keywords": ["Qualcomm HS-USB QDLoader 9008", "QDLoader 9008", "Qualcomm HS-USB Diagnostics 9008"],
        "recommended_tool": "QFIL v2.0.3.5 / Mi Flash 2024 Official (QPST Suite)",
        "recommended_driver": "Qualcomm QDLoader HS-USB 9008 64-bit WHQL Driver",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flashing-tools",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Device in Qualcomm 9008 mode. Firehose MBN loader required. Use QFIL Flat Build."
    },
    {
        "mode_id": "MTK_BROM",
        "name": "MediaTek BootROM (BROM) Auth Bypass Mode",
        "category": "BootROM Hardware Auth",
        "badge": "MTK BROM",
        "color": "ORANGE",
        "vid_pid": [("0E8D", "0003")],
        "keywords": ["MediaTek USB Port", "MTK USB Port", "MTK VCOM"],
        "recommended_tool": "SP Flash Tool v5.2124 (Auth SLA Bypass Edition) / MTK Client GUI",
        "recommended_driver": "MediaTek Auto Driver v1.0.8 + LibUSB Win32 Filter Driver",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flashing-tools",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Device in MediaTek BROM mode. Requires LibUSB filter driver for SLA/DAA bypass."
    },
    {
        "mode_id": "MTK_PRELOADER",
        "name": "MediaTek Preloader / VCOM Flashing Port",
        "category": "Preloader Port",
        "badge": "MTK PRELOADER",
        "color": "YELLOW",
        "vid_pid": [("0E8D", "2000"), ("0E8D", "2001")],
        "keywords": ["MediaTek Preloader USB VCOM", "MediaTek DA USB VCOM", "MTK Preloader"],
        "recommended_tool": "SP Flash Tool v5.2124 / Maui META IMEI & NVRAM Tool",
        "recommended_driver": "MTK Auto Driver v1.0.8 (CDC / VCOM Port)",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flashing-tools",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "MediaTek Preloader active. Select verified factory scatter XML to flash firmware."
    },
    {
        "mode_id": "SAMSUNG_DOWNLOAD",
        "name": "Samsung Galaxy Download Mode (Odin / LOKE)",
        "category": "Samsung Download Protocol",
        "badge": "SAMSUNG ODIN",
        "color": "BLUE",
        "vid_pid": [("04E8", "685D"), ("04E8", "6860"), ("04E8", "685E")],
        "keywords": ["SAMSUNG Mobile USB CDC Composite Device", "SAMSUNG Mobile USB Modem", "SAMSUNG Android Modem"],
        "recommended_tool": "Samsung Odin3 v3.14.4 Official (Patched 3B) / Frija High-Speed Downloader",
        "recommended_driver": "Samsung Official Mobile USB Drivers v1.7.59.0 WHQL",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flash-files",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Samsung Download Mode detected. Flash official 4-File Repair TAR (BL, AP, CP, CSC)."
    },
    {
        "mode_id": "FASTBOOT",
        "name": "Android Fastboot / Bootloader Mode",
        "category": "Bootloader Protocol",
        "badge": "FASTBOOT",
        "color": "CYAN",
        "vid_pid": [("18D1", "4EE0"), ("2717", "FF40"), ("2717", "FF48"), ("22D4", "2769")],
        "keywords": ["Android Bootloader Interface", "Fastboot Device", "Xiaomi Fastboot"],
        "recommended_tool": "Xiaomi Mi Flash Tool 2024 / Android SDK Fastboot CLI",
        "recommended_driver": "Google / Xiaomi Fastboot WHQL USB Drivers",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flash-files",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Device in Fastboot mode. Can read bootloader unlock state and flash fastboot partitions."
    },
    {
        "mode_id": "UNISOC_SPRD",
        "name": "Unisoc / Spreadtrum SCI USB2Serial Mode",
        "category": "Spreadtrum PAC Download",
        "badge": "UNISOC / SPD",
        "color": "PURPLE",
        "vid_pid": [("1782", "4D00"), ("1782", "4D01"), ("1782", "0001")],
        "keywords": ["Spreadtrum SCI USB2Serial", "SPRD U2S Diag", "SPRD COM Port"],
        "recommended_tool": "SPD Research & Upgrade Download Tool R24.0.0003",
        "recommended_driver": "Unisoc / Spreadtrum SCI USB Drivers v2.0.0.1",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#flashing-tools",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Unisoc PAC download mode detected. Hold Volume Down while connecting."
    },
    {
        "mode_id": "MTP_NORMAL",
        "name": "Normal Boot Mode (MTP File Transfer)",
        "category": "Media Transfer Protocol",
        "badge": "MTP STORAGE",
        "color": "GREEN",
        "vid_pid": [("04E8", "6860"), ("2717", "FF40"), ("0E8D", "2008")],
        "keywords": ["MTP USB Device", "Media Transfer Protocol", "MTP Device"],
        "recommended_tool": "Samsung Universal FRP Tool v4.9 (*#0*# Enabler) / GSM BFT Free Tool",
        "recommended_driver": "All-in-One Universal Driver Setup 2026",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#frp-bypass",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "Normal OS MTP mode. Dial *#0*# in emergency dialer for instant ADB authorization."
    },
    {
        "mode_id": "ADB_DEBUG",
        "name": "Android ADB Debugging / Recovery Mode",
        "category": "Android Debug Bridge",
        "badge": "ADB ACTIVE",
        "color": "TEAL",
        "vid_pid": [("18D1", "4EE7"), ("2717", "FF48"), ("04E8", "6860")],
        "keywords": ["Android Composite ADB Interface", "Android ADB Interface", "SAMSUNG Android ADB Interface"],
        "recommended_tool": "GSM Fix Hub Terminal / SamFw FRP Enabler / Fastboot Sideload",
        "recommended_driver": "Universal ADB & Fastboot Drivers 2026",
        "portal_url": f"{DEFAULT_PORTAL_URL}/#frp-bypass",
        "testpoint_url": f"{DEFAULT_PORTAL_URL}/#testpoints",
        "video_url": f"{DEFAULT_PORTAL_URL}/#video-tutorials",
        "action_guide": "ADB authorized. Full diagnostic readback and 1-click reboot to EDL / Bootloader enabled."
    }
]


def scan_adb_devices():
    """Detect devices connected via ADB and extract model details."""
    devices = []
    try:
        res = subprocess.run(["adb", "devices", "-l"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            for line in res.stdout.strip().split("\n")[1:]:
                line = line.strip()
                if not line or "offline" in line:
                    continue
                parts = line.split()
                serial = parts[0]
                state = parts[1] if len(parts) > 1 else "unknown"
                
                model_match = re.search(r"model:([^\s]+)", line)
                model = model_match.group(1) if model_match else "Android Device"
                device_match = re.search(r"device:([^\s]+)", line)
                dev_name = device_match.group(1) if device_match else ""
                
                mode_id = "ADB_DEBUG" if state == "device" else ("FASTBOOT" if state == "fastboot" else "MTP_NORMAL")
                devices.append({
                    "raw_name": f"ADB [{state.upper()}]: {model} ({serial})",
                    "serial": serial,
                    "state": state,
                    "model": model,
                    "device_code": dev_name,
                    "mode_id": mode_id,
                    "source": "ADB Engine"
                })
    except Exception:
        pass
    return devices


def scan_fastboot_devices():
    """Detect devices connected in Fastboot mode."""
    devices = []
    try:
        res = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            for line in res.stdout.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                serial = parts[0]
                
                # Query product name via fastboot getvar product
                product_name = ""
                try:
                    p_res = subprocess.run(["fastboot", "-s", serial, "getvar", "product"], capture_output=True, text=True, timeout=2)
                    m = re.search(r"product:\s*([^\s\r\n]+)", p_res.stderr + p_res.stdout)
                    if m:
                        product_name = m.group(1)
                except Exception:
                    pass

                model_str = f"Fastboot Bootloader: {product_name or 'Universal'}"
                devices.append({
                    "raw_name": f"{model_str} ({serial})",
                    "serial": serial,
                    "state": "fastboot",
                    "model": product_name,
                    "device_code": product_name,
                    "mode_id": "FASTBOOT",
                    "source": "Fastboot Engine"
                })
    except Exception:
        pass
    return devices


def scan_windows_hardware_devices():
    """Scan Windows Plug-and-Play (PnP) hardware entities via PowerShell."""
    devices = []
    if sys.platform != "win32":
        return devices

    try:
        # Query Windows PnP devices with USB and COM connections
        ps_script = """
        Get-CimInstance Win32_PnPEntity | 
        Where-Object { $_.DeviceID -like 'USB*' -or $_.Caption -like '*COM*' -or $_.Name -like '*QDLoader*' -or $_.Name -like '*MediaTek*' -or $_.Name -like '*Spreadtrum*' } | 
        Select-Object Name, DeviceID, Caption | 
        ConvertTo-Json -Compress
        """
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            raw = json.loads(res.stdout.strip())
            if isinstance(raw, dict):
                raw = [raw]
            for item in raw:
                name = item.get("Name") or item.get("Caption") or ""
                dev_id = item.get("DeviceID") or ""
                if name:
                    devices.append({"name": name, "device_id": dev_id})
    except Exception:
        pass
    return devices


def classify_hardware_device(device_text, dev_id=""):
    """Classify a raw hardware string against known GSM device signatures."""
    target_str = (device_text + " " + dev_id).upper()
    
    # Check by keywords first
    for sig in DEVICE_SIGNATURES:
        for kw in sig["keywords"]:
            if kw.upper() in target_str:
                # Extract COM port if present (e.g. COM7)
                com_match = re.search(r"\((COM\d+)\)", device_text, re.I)
                com_port = com_match.group(1).upper() if com_match else ""
                return sig, com_port

    # Check by VID/PID
    for sig in DEVICE_SIGNATURES:
        for vid, pid in sig["vid_pid"]:
            pattern = f"VID_{vid}&PID_{pid}"
            if pattern in target_str:
                com_match = re.search(r"\((COM\d+)\)", device_text, re.I)
                com_port = com_match.group(1).upper() if com_match else ""
                return sig, com_port

    return None, ""


def get_recommended_web_link(sig, model_name="", com_port=""):
    """Generate the exact GSM Fix Hub portal link matching the detected mode."""
    base = DEFAULT_PORTAL_URL
    # Prefer local file if available on the machine
    if os.path.exists(LOCAL_PORTAL_PATH):
        base = f"file:///{LOCAL_PORTAL_PATH.replace(os.sep, '/')}"

    mode = sig["mode_id"]
    if mode == "QC_EDL_9008":
        return f"{base}#testpoints"
    elif mode in ["MTK_BROM", "MTK_PRELOADER"]:
        return f"{base}#flashing-tools"
    elif mode == "SAMSUNG_DOWNLOAD":
        return f"{base}#flash-files"
    elif mode == "FASTBOOT":
        if model_name:
            return f"{base}#flash-files"
        return f"{base}#flash-files"
    elif mode == "UNISOC_SPRD":
        return f"{base}#flashing-tools"
    elif mode in ["MTP_NORMAL", "ADB_DEBUG"]:
        return f"{base}#frp-bypass"
    return f"{base}#home"


class GSMDeviceDetectorEngine:
    def __init__(self, auto_open_browser=True, check_interval=1.5):
        self.auto_open_browser = auto_open_browser
        self.check_interval = check_interval
        self.running = False
        self.detected_devices_history = set()
        self.current_connected_device = None
        self.callbacks = []

    def register_callback(self, cb):
        self.callbacks.append(cb)

    def trigger_callbacks(self, event_type, data):
        for cb in self.callbacks:
            try:
                cb(event_type, data)
            except Exception:
                pass

    def start_monitoring(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        self.running = False

    def _monitor_loop(self):
        while self.running:
            active_devs = self._scan_all_interfaces()
            if active_devs:
                top_dev = active_devs[0]
                sig = top_dev["signature"]
                dev_key = f"{sig['mode_id']}_{top_dev.get('com_port')}_{top_dev.get('raw_name')}"
                
                if dev_key not in self.detected_devices_history:
                    self.detected_devices_history.add(dev_key)
                    self.current_connected_device = top_dev
                    web_link = get_recommended_web_link(sig, top_dev.get("model", ""), top_dev.get("com_port", ""))
                    top_dev["web_link"] = web_link
                    
                    self.trigger_callbacks("DEVICE_CONNECTED", top_dev)
                    
                    if self.auto_open_browser and web_link:
                        try:
                            webbrowser.open(web_link)
                        except Exception:
                            pass
            else:
                if self.current_connected_device is not None:
                    self.trigger_callbacks("DEVICE_DISCONNECTED", self.current_connected_device)
                    self.current_connected_device = None
                    self.detected_devices_history.clear()

            time.sleep(self.check_interval)

    def _scan_all_interfaces(self):
        found = []
        
        # 1. Check Fastboot
        fb_devices = scan_fastboot_devices()
        for d in fb_devices:
            sig, _ = classify_hardware_device(d["raw_name"])
            if not sig:
                sig = next(s for s in DEVICE_SIGNATURES if s["mode_id"] == "FASTBOOT")
            found.append({
                "mode_name": sig["name"],
                "signature": sig,
                "raw_name": d["raw_name"],
                "model": d.get("model", ""),
                "com_port": "USB Fastboot",
                "badge": sig["badge"]
            })

        # 2. Check ADB
        adb_devices = scan_adb_devices()
        for d in adb_devices:
            sig = next((s for s in DEVICE_SIGNATURES if s["mode_id"] == d["mode_id"]), None)
            if not sig:
                sig = next(s for s in DEVICE_SIGNATURES if s["mode_id"] == "ADB_DEBUG")
            found.append({
                "mode_name": sig["name"],
                "signature": sig,
                "raw_name": d["raw_name"],
                "model": d.get("model", ""),
                "com_port": "USB Debugging",
                "badge": sig["badge"]
            })

        # 3. Check Windows Hardware Entities (COM & USB)
        hw_devices = scan_windows_hardware_devices()
        for d in hw_devices:
            sig, com = classify_hardware_device(d["name"], d.get("device_id", ""))
            if sig:
                found.append({
                    "mode_name": sig["name"],
                    "signature": sig,
                    "raw_name": d["name"],
                    "model": "",
                    "com_port": com or "USB Interface",
                    "badge": sig["badge"]
                })

        return found


# Demonstration / CLI Runner
if __name__ == "__main__":
    print("=" * 75)
    print(" GSM Fix Hub — Auto Mobile Device Mode Detector & Web Linker Pro (2026)")
    print(" Lead Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal")
    print("=" * 75)
    print(" Supported Modes: Fastboot, MTP, Recovery, MTK BROM, MTK Preloader,")
    print("                  Qualcomm EDL 9008, Samsung Odin Download, Unisoc SPD.")
    print("=" * 75)
    print(f" [*] Local Portal: {LOCAL_PORTAL_PATH}")
    print(f" [*] Cloud Portal: {DEFAULT_PORTAL_URL}")
    print(" [*] Monitoring USB & Hardware Ports for Mobile Devices in Real-Time...")
    print(" [*] Plug in any mobile device via USB cable to test...")
    print("=" * 75)

    def on_device_event(event_type, dev):
        if event_type == "DEVICE_CONNECTED":
            sig = dev["signature"]
            print(f"\n[+] >>> MOBILE DEVICE DETECTED! <<<")
            print(f"    Mode:         {sig['name']} [{sig['badge']}]")
            print(f"    Port / Conn:  {dev.get('com_port', 'USB')}")
            print(f"    Hardware:     {dev.get('raw_name')}")
            print(f"    Recommend:    {sig['recommended_tool']}")
            print(f"    Driver:       {sig['recommended_driver']}")
            print(f"    Action:       {sig['action_guide']}")
            print(f"    [WEB LINK]:   {dev['web_link']}")
            print(f"    >>> Launching GSM Fix Hub in browser automatically...\n")
        elif event_type == "DEVICE_DISCONNECTED":
            print(f"[-] Mobile device unplugged / disconnected.\n")

    detector = GSMDeviceDetectorEngine(auto_open_browser=False, check_interval=1.0)
    detector.register_callback(on_device_event)
    
    # Run mock simulation or real scan
    print("Checking initial hardware state...")
    initial = detector._scan_all_interfaces()
    if initial:
        print(f"Found {len(initial)} active mobile interface(s) right now.")
        for item in initial:
            print(" -", item["mode_name"], item["raw_name"])
    else:
        print("No mobile devices currently in active flashing or diagnostic mode.")
        print("Detector engine successfully verified and ready.")
