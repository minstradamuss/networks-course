import socket
import time
import tkinter as tk
from tkinter import messagebox
import os

def send_udp_packets(ip, port, count):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = int(count)
    start = time.time()
    for _ in range(count):
        data = os.urandom(1024)
        s.sendto(data, (ip, int(port)))
    end = time.time()
    duration = end - start
    s.close()
    #messagebox.showinfo("Transfer Complete", f"Sent {count} packets in {duration:.2f} seconds")

def create_sender_gui():
    win = tk.Tk()
    win.title("UDP Sender")

    tk.Label(win, text="Enter receiver IP").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter port").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter number of packets").grid(row=2, column=0, padx=5, pady=5)

    ip_entry = tk.Entry(win)
    port_entry = tk.Entry(win)
    count_entry = tk.Entry(win)

    ip_entry.insert(0, "127.0.0.1")
    port_entry.insert(0, "8888")
    count_entry.insert(0, "5")

    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    count_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(win, text="Send", command=lambda: send_udp_packets(ip_entry.get(), port_entry.get(), count_entry.get())).grid(row=3, column=1, pady=10)

    win.mainloop()

create_sender_gui()
