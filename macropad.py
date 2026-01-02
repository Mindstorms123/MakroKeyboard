import serial.tools.list_ports
import serial
import keyboard
import time
import sys
import threading
try:
    import pystray
    from PIL import Image, ImageDraw
    import win10toast  # Windows Notifications
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("❌ pystray/win10toast fehlen → pip install pystray win10toast")

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='black')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill='blue')
    dc.text((22, 25), "M", fill='white')
    return image

def show_notification(title, message, icon_path=None):
    """Windows Notification"""
    try:
        toaster = win10toast.ToastNotifier()
        toaster.show_toast(title, message, icon_path, duration=3)
    except:
        print(f"🔔 {title}: {message}")

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'COM5' in port.device.upper():
            return port.device
        desc = port.description.lower()
        if any(x in desc for x in ['silicon labs', 'cp210x', 'ch340', 'serielles usb']):
            return port.device
    return None

def safe_close():
    global ser
    try:
        if ser and ser.is_open:
            ser.close()
    except:
        pass
    ser = None

def is_esp32_connected():
    global current_port
    if not current_port: return False
    try:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == current_port: return True
        return False
    except: return False

# GLOBAL
reconnect_needed = False
icon = None
ser = None
current_port = None

def main_loop():
    """Hauptloop - 100% unsichtbar"""
    global ser, current_port, reconnect_needed
    
    show_notification("🎮 ESP32 MacroPad", "Gestartet - Suche ESP32...")
    
    while True:
        # ESP32 finden
        if not current_port or reconnect_needed:
            current_port = find_esp32_port()
            if current_port:
                show_notification("⭐ ESP32", f"{current_port} gefunden!")
                reconnect_needed = False
        
        # Verbinden
        if current_port and not ser:
            try:
                ser = serial.Serial(current_port, 115200, timeout=0.1)
                time.sleep(1)
                show_notification("✅ ESP32 LIVE", f"{current_port} bereit!")
            except Exception as e:
                safe_close()
                time.sleep(0.5)
                continue
        
        # LESEN (superschnell)
        if ser and ser.is_open:
            try:
                if ser.in_waiting > 0:
                    cmd = ser.readline().decode().strip()
                    print(f"← {cmd}")  # Debug
                    
                    if "VOL_UP" in cmd or "VOL_UP_CONT" in cmd:
                        keyboard.press_and_release('volume up')
                    elif "VOL_DOWN" in cmd or "VOL_DOWN_CONT" in cmd:
                        keyboard.press_and_release('volume down')
                    elif "COPY" in cmd:
                        keyboard.press_and_release('ctrl+c')
                    elif "PASTE" in cmd:
                        keyboard.press_and_release('ctrl+v')
                    elif "WIN_SH_S" in cmd:
                        keyboard.press_and_release('win+shift+s')
                    elif "WIN_SH_N" in cmd:
                        keyboard.press_and_release('ctrl+shift+n')
                        
            except (serial.SerialException, OSError):
                show_notification("🔌 ESP32", "Ausgesteckt - Hotplug...")
                safe_close()
                reconnect_needed = True
            except:
                pass
        
        # Disconnect Check alle 2s
        if time.time() % 2 < 0.01 and not is_esp32_connected():
            show_notification("🔌 ESP32", "Weg - suche...")
            safe_close()
            reconnect_needed = True
        
        time.sleep(0.001)

def tray_menu():
    menu = pystray.Menu(
        pystray.MenuItem("ℹ️ Status", status_action),
        pystray.MenuItem("🔌 ESP32 Check", esp32_status),
        pystray.MenuItem("❌ Beenden", quit_action)
    )
    return menu

def status_action(icon_, item):
    show_notification("🎮 ESP32 MacroPad", "Läuft perfekt! Hotplug aktiv.")

def esp32_status(icon_, item):
    global current_port, ser
    if ser and ser.is_open and current_port:
        show_notification("✅ LIVE", f"ESP32 {current_port}")
    else:
        show_notification("⏳ Hotplug", "Suche ESP32...")

def quit_action(icon_, item):
    show_notification("👋 ESP32 MacroPad", "Beendet.")
    sys.exit(0)

# START - 100% UNSICHTBAR!
if __name__ == "__main__":
    ser = None
    current_port = None
    reconnect_needed = True
    
    if TRAY_AVAILABLE:
        # TRAY ICON
        icon = pystray.Icon("ESP32", create_tray_icon(), "ESP32 MacroPad", tray_menu())
        
        # MACROPAD THREAD
        macropad_thread = threading.Thread(target=main_loop, daemon=True)
        macropad_thread.start()
        
        # TRAY starten
        icon.run()
    else:
        main_loop()
