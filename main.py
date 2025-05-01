import subprocess
import re
import tkinter as tk
from tkinter import messagebox

def scan_networks():
    try:
        output = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'], stderr=subprocess.DEVNULL).decode()
        ssids = re.findall(r'ESSID:"([^"]+)"', output)
        ssid_listbox.delete(0, tk.END)
        for ssid in sorted(set(ssids)):
            ssid_listbox.insert(tk.END, ssid)
    except Exception as e:
        messagebox.showerror("Fehler beim Scannen", str(e))

def connect_to_wifi():
    selected_index = ssid_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Kein Netzwerk ausgewählt", "Bitte wähle ein WLAN aus.")
        return

    ssid = ssid_listbox.get(selected_index)
    password = password_entry.get()

    if not password:
        messagebox.showwarning("Kein Passwort", "Bitte gib das WLAN-Passwort ein.")
        return

    try:
        # WPA-Konfiguration schreiben
        config = f'''
network={{
    ssid="{ssid}"
    psk="{password}"
}}
'''
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.write(config)

        # Verbindung neu starten
        subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"], check=True)
        subprocess.run(["sudo", "dhclient", "wlan0"], check=True)

        messagebox.showinfo("Erfolg", f"Mit '{ssid}' verbunden!")
    except Exception as e:
        messagebox.showerror("Verbindungsfehler", str(e))

# GUI bauen
root = tk.Tk()
root.title("WLAN-Verbindung")
root.geometry("400x300")

tk.Label(root, text="Verfügbare Netzwerke:").pack(pady=5)

ssid_listbox = tk.Listbox(root, height=8)
ssid_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

scan_button = tk.Button(root, text="Netzwerke scannen", command=scan_networks)
scan_button.pack(pady=5)

tk.Label(root, text="WLAN-Passwort:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

connect_button = tk.Button(root, text="Verbinden", command=connect_to_wifi)
connect_button.pack(pady=10)

# Beim Start automatisch scannen
scan_networks()

root.mainloop()
