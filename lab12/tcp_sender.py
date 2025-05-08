import socket
import time
import tkinter as tk
from tkinter import messagebox
import os

def send_packets(ip, port, count):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        start = time.time()
        for _ in range(int(count)):
            data = os.urandom(1024)
            s.sendall(data)
        end = time.time()
        s.close()
        duration = end - start
        #messagebox.showinfo("Transfer Complete", f"Sent {count} packets in {duration:.2f} seconds")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_sender_gui():
    win = tk.Tk()
    win.title("TCP Sender")

    tk.Label(win, text="Enter receiver IP address").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter port to send").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter number of packets to send").grid(row=2, column=0, padx=5, pady=5)

    ip_entry = tk.Entry(win)
    port_entry = tk.Entry(win)
    count_entry = tk.Entry(win)

    ip_entry.insert(0, "127.0.0.1")
    port_entry.insert(0, "8080")
    count_entry.insert(0, "5")

    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    count_entry.grid(row=2, column=1, padx=5, pady=5)

    send_button = tk.Button(win, text="Send", command=lambda: send_packets(ip_entry.get(), port_entry.get(), count_entry.get()))
    send_button.grid(row=3, column=1, pady=10)

    win.mainloop()

create_sender_gui()
