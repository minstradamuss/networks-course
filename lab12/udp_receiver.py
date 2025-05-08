import socket
import time
import tkinter as tk
import threading

def receive_udp_packets(ip, port, speed_entry, count_entry):
    def run_receiver():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, int(port)))
        s.settimeout(2.0)

        packet_count = 0
        start_time = time.time()

        try:
            while True:
                data, _ = s.recvfrom(2048)
                if not data:
                    break
                packet_count += 1
        except socket.timeout:
            pass

        end_time = time.time()
        duration = max(end_time - start_time, 0.0001)
        speed = (packet_count * 1024) / duration

        speed_entry.config(state="normal")
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, f"{speed / 1024:.2f} KB/s")
        speed_entry.config(state="readonly")

        count_entry.config(state="normal")
        count_entry.delete(0, tk.END)
        count_entry.insert(0, f"{packet_count} packets")
        count_entry.config(state="readonly")

        s.close()

    threading.Thread(target=run_receiver, daemon=True).start()

def create_receiver_gui():
    win = tk.Tk()
    win.title("UDP Receiver")

    tk.Label(win, text="Enter IP").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter port").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(win, text="Packets received").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(win, text="Transfer speed").grid(row=3, column=0, padx=5, pady=5)

    ip_entry = tk.Entry(win)
    port_entry = tk.Entry(win)
    count_entry = tk.Entry(win, state="readonly")
    speed_entry = tk.Entry(win, state="readonly")

    ip_entry.insert(0, "127.0.0.1")
    port_entry.insert(0, "8888")

    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    count_entry.grid(row=2, column=1, padx=5, pady=5)
    speed_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(win, text="Receive", command=lambda: receive_udp_packets(ip_entry.get(), port_entry.get(), speed_entry, count_entry)).grid(row=4, column=1, pady=10)

    win.mainloop()

create_receiver_gui()
