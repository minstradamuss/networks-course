import tkinter as tk
from tkinter import ttk
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from threading import Thread
from collections import defaultdict

running = False
packets_list = []
mode = "full"
incoming = defaultdict(int)
outgoing = defaultdict(int)


def packet_info(packet):
    if IP in packet:
        ip = packet[IP]
        proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "OTHER"
        src_ip, dst_ip = ip.src, ip.dst
        version = ip.version
        sport = packet.sport if hasattr(packet, 'sport') else "-"
        dport = packet.dport if hasattr(packet, 'dport') else "-"
        size = len(packet)

        packets_list.append((src_ip, dst_ip, sport, dport, proto, version, size))

        if dst_ip == my_ip:
            incoming[dport] += size
        elif src_ip == my_ip:
            outgoing[sport] += size

        update_display()


def update_display():
    tree.delete(*tree.get_children())

    if mode == "full":
        for idx, (src, dst, sport, dport, proto, ver, size) in enumerate(packets_list[-100:]):
            tree.insert("", "end", iid=idx, values=(f"{src}:{sport} -> {dst}:{dport} ({proto})", size))
    elif mode == "dst":
        summary = defaultdict(int)
        for _, dst, _, dport, _, _, size in packets_list:
            summary[dport] += size
        for port, total in summary.items():
            tree.insert("", "end", values=(f"Port: {port}", total))
    elif mode == "src":
        summary = defaultdict(int)
        for src, _, sport, _, _, _, size in packets_list:
            summary[sport] += size
        for port, total in summary.items():
            tree.insert("", "end", values=(f"Port: {port}", total))


def on_select(event):
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        src, dst, sport, dport, proto, ver, size = packets_list[idx]
        info = (f"IP Version: {ver}\nProtocol: {proto}\nSize: {size} bytes\n"
                f"Source IP: {src}\nSource Port: {sport}\n"
                f"Destination IP: {dst}\nDestination Port: {dport}")
        hint_label.config(text=info)


def start_sniff():
    global running
    running = True
    sniff(prn=packet_info, store=0, stop_filter=lambda x: not running)


def stop_sniff():
    global running
    running = False


def set_mode(value):
    global mode
    mode = value
    update_display()


my_ip = "192.168.0.187"

root = tk.Tk()
root.title("Net traffic")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

controls = tk.Frame(frame)
controls.pack(fill="x")

tk.Label(controls, text=my_ip).pack(side="left")
tk.Button(controls, text="Start", command=lambda: Thread(target=start_sniff).start()).pack(side="left")
tk.Button(controls, text="Stop", command=stop_sniff).pack(side="left")
tk.Button(controls, text="Reset", command=lambda: packets_list.clear()).pack(side="left")

mode_frame = tk.LabelFrame(controls, text="Display mode")
mode_frame.pack(side="left", padx=10)

modes = [
    ("Full", "full"),
    ("By destination ports", "dst"),
    ("By source ports", "src")
]

mode_var = tk.StringVar(value="full")
for text, val in modes:
    tk.Radiobutton(mode_frame, text=text, variable=mode_var, value=val,
                   command=lambda v=val: set_mode(v)).pack(anchor="w")

columns = ("description", "size")
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading("description", text="Description")
tree.heading("size", text="Size")
tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_select)

hint_label = tk.Label(root, text="", justify="left", anchor="w")
hint_label.pack(fill="x")

root.mainloop()
