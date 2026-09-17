# GSM Fix Hub — Auto Mobile Device Mode Detector & Web Linker (Pro Edition 2026)
**Lead Architect & Developer: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal**
**Official Portal: https://www.gsmfixhub.com/ | https://bhuwanbastola.com.np/**

This software automatically detects when any mobile phone is plugged into a Windows PC via USB across 8 distinct hardware, bootloader, and diagnostic modes, identifies the exact hardware chip and COM port, and **automatically launches the matching GSM Fix Hub web portal section** (ROMs, flashing tools, motherboard EDL pinouts, and masterclass tutorials) in your browser.

---

## ⚡ Supported Mobile Modes & Hardware Signatures

1. **Qualcomm Snapdragon EDL 9008 Mode**:
   - Hardware: `Qualcomm HS-USB QDLoader 9008 (COMx)`, VID `05C6` PID `9008`
   - Auto Link: Opens `#flashing-tools` (QFIL v2.0.3.5 / Mi Flash) & `#testpoints` (Hardware EDL Pinouts).
2. **MediaTek BootROM (BROM) Mode**:
   - Hardware: `MediaTek USB Port (COMx)`, VID `0E8D` PID `0003`
   - Auto Link: Opens `#flashing-tools` (SP Flash Tool Auth SLA Bypass & LibUSB Filter Driver).
3. **MediaTek Preloader / VCOM Mode**:
   - Hardware: `MediaTek Preloader USB VCOM Port`, VID `0E8D` PID `2000` / `2001`
   - Auto Link: Opens `#flashing-tools` & `#flash-files` (Scatter firmware).
4. **Samsung Galaxy Download Mode (Odin / LOKE)**:
   - Hardware: `SAMSUNG Mobile USB CDC Composite Device / Modem`, VID `04E8` PID `685D` / `6860`
   - Auto Link: Opens `#flash-files` (Samsung Galaxy 4-File Repair TARs) & Odin3 v3.14.4 Patched 3B.
5. **Android Fastboot / Bootloader Mode**:
   - Hardware: `Android Bootloader Interface`, Xiaomi/Google Fastboot (`18D1:4EE0` / `2717:FF40`)
   - Queries product model via `fastboot getvar product`.
   - Auto Link: Opens `#flash-files` filtered to the exact device model.
6. **Unisoc / Spreadtrum SCI USB2Serial Mode**:
   - Hardware: `Spreadtrum SCI USB2Serial`, `SPRD U2S Diag (COMx)`, VID `1782` PID `4D00` / `4D01`
   - Auto Link: Opens `#flashing-tools` (SPD Research & Upgrade Tool) & `#testpoints`.
7. **Normal Boot MTP Mode**:
   - Hardware: `MTP USB Device`, Media Transfer Protocol
   - Auto Link: Opens `#frp-bypass` (Samsung *#0*# 1-click MTP FRP / BFT Free Unlock).
8. **ADB Debugging / Recovery Mode**:
   - Hardware: `Android Composite ADB Interface`
   - Queries `adb devices -l` and reads `ro.product.model`, `ro.product.brand`, and Android version.
   - Auto Link: Opens `#frp-bypass` and diagnostic tools.

---

## 🚀 How to Run the Software

### Option 1: Double-Click the Windows Launcher
1. Open the `software/` folder on your Windows PC.
2. Double-click **`Run_GSM_Device_Detector.bat`**.
3. The dark-themed technician GUI window will open.
4. Plug in your mobile phone — the software will detect the mode and automatically pop up the matching GSM Fix Hub portal page in your default browser!

### Option 2: Compile to Standalone `.EXE` (No Python Required)
1. Double-click **`Build_EXE.bat`**.
2. PyInstaller will compile `gsm_device_detector_gui.py` into a single, standalone executable:
   `dist\GSM_Device_Detector_Pro\GSM_Device_Detector_Pro.exe`
3. You can distribute or run this `.exe` on any Windows 10/11 PC without installing Python!

### Option 3: In-Browser WebUSB / WebSerial Live Monitor
1. Open **`software/web_usb_monitor.html`** (or click **"USB Auto Detector"** in the top console of the web portal) in Google Chrome or Microsoft Edge.
2. Click **"Scan / Connect USB Device"** or **"Scan COM Serial Port"**.
3. Plug in your phone — Chrome will read the USB descriptor and instantly link to the matching GSM Fix Hub tools!

---

© 2026 GSM Fix Hub by Bhuwan Bastola | Gopal Electronics, Surkhet. All Rights Reserved.
