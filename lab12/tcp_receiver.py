import socket
import time
import tkinter as tk
import threading

def receive_data(ip, port, speed_entry, count_entry):
    def run_server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, int(port)))
        s.listen(1)
        conn, addr = s.accept()

        received_packets = 0
        start_time = time.time()

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                received_packets += 1
        except:
            pass

        end_time = time.time()
        conn.close()

        duration = max(end_time - start_time, 0.0001)
        speed = (received_packets * 1024) / duration

        speed_entry.config(state="normal")
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, f"{speed:.2f} B/s")
        speed_entry.config(state="readonly")

        count_entry.config(state="normal")
        count_entry.delete(0, tk.END)
        count_entry.insert(0, f"{received_packets} packets")
        count_entry.config(state="readonly")

    threading.Thread(target=run_server, daemon=True).start()

def create_receiver_gui():
    win = tk.Tk()
    win.title("TCP Receiver")

    tk.Label(win, text="Enter IP").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(win, text="Enter port to receive").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(win, text="Transfer speed").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(win, text="Packets received").grid(row=3, column=0, padx=5, pady=5)

    ip_entry = tk.Entry(win)
    port_entry = tk.Entry(win)
    speed_entry = tk.Entry(win, state="readonly")
    count_entry = tk.Entry(win, state="readonly")

    ip_entry.insert(0, "127.0.0.1")
    port_entry.insert(0, "8080")

    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    speed_entry.grid(row=2, column=1, padx=5, pady=5)
    count_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(win, text="Receive", command=lambda: receive_data(ip_entry.get(), port_entry.get(), speed_entry, count_entry)).grid(row=4, column=1, pady=10)

    win.mainloop()

create_receiver_gui()
