import tkinter as tk
from threading import Thread
from scapy.all import sniff
from collections import defaultdict

my_ip = "192.168.0.187" 

incoming = defaultdict(int)
outgoing = defaultdict(int)
running = False


def update_display_safe():
    display.delete(1.0, tk.END)
    display.insert(tk.END, "Incoming Traffic by Destination Port:\n")
    for port, size in incoming.items():
        display.insert(tk.END, f"Port {port}: {size} bytes\n")
    display.insert(tk.END, "\nOutgoing Traffic by Source Port:\n")
    for port, size in outgoing.items():
        display.insert(tk.END, f"Port {port}: {size} bytes\n")


def analyze(packet):
    if packet.haslayer("IP") and packet.haslayer("TCP"):
        size = len(packet)
        ip = packet["IP"]
        tcp = packet["TCP"]
        if ip.dst == my_ip:
            incoming[tcp.dport] += size
        elif ip.src == my_ip:
            outgoing[tcp.sport] += size
        root.after(0, update_display_safe)


def start_sniff():
    global running
    running = True
    sniff(prn=analyze, store=0, stop_filter=lambda x: not running)


def stop_sniff():
    global running
    running = False


# GUI
root = tk.Tk()
root.title("Traffic Counter by Ports")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

display = tk.Text(frame, width=60, height=25)
display.pack()

start_btn = tk.Button(frame, text="Start", command=lambda: Thread(target=start_sniff, daemon=True).start())
start_btn.pack(side="left", padx=5)

stop_btn = tk.Button(frame, text="Stop", command=stop_sniff)
stop_btn.pack(side="right", padx=5)

root.mainloop()