import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
import random

BROADCAST_PORT = 50000
BROADCAST_IP = '<broadcast>'
TIMEOUT = 6
BUFFER_SIZE = 1024

class AppMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyzer")
        self.running = True
        self.local_port = random.randint(4000, 11000)
        self.id = f"{self.get_local_ip()}:{self.local_port}"
        self.peers = {}
        self.lock = threading.Lock()

        self.count_var = tk.StringVar(value="0")
        self.wait_var = tk.StringVar(value="2000")

        tk.Label(root, text="Number of instances running:").pack()
        tk.Label(root, textvariable=self.count_var).pack()

        tk.Label(root, text="Interval (ms):").pack()
        self.wait_entry = tk.Entry(root, textvariable=self.wait_var)
        self.wait_entry.pack()

        self.text_area = scrolledtext.ScrolledText(root, height=10)
        self.text_area.pack()

        tk.Button(root, text="Close", command=self.on_close).pack()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.socket.bind(('0.0.0.0', self.local_port))

        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.broadcast_loop, daemon=True).start()
        threading.Thread(target=self.cleanup_loop, daemon=True).start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def broadcast_loop(self):
        while self.running:
            wait_ms = int(self.wait_var.get())
            self.send_message(f"HELLO|{self.id}")
            time.sleep(wait_ms / 1000)

    def send_message(self, message):
        self.socket.sendto(message.encode(), (BROADCAST_IP, BROADCAST_PORT))

    def listen(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(BUFFER_SIZE)
                message = data.decode()
                if "|" not in message:
                    continue
                msg_type, sender_id = message.split("|", 1)
                if sender_id == self.id:
                    continue

                now = time.time()
                with self.lock:
                    if msg_type == "HELLO":
                        self.peers[sender_id] = now
                        self.send_message(f"ALIVE|{self.id}")
                    elif msg_type == "ALIVE":
                        self.peers[sender_id] = now
                    elif msg_type == "BYE":
                        if sender_id in self.peers:
                            del self.peers[sender_id]
                self.update_display()
            except Exception:
                continue

    def cleanup_loop(self):
        while self.running:
            now = time.time()
            with self.lock:
                to_remove = [peer for peer, t in self.peers.items() if now - t > TIMEOUT]
                for peer in to_remove:
                    del self.peers[peer]
            self.update_display()
            time.sleep(1)

    def update_display(self):
        all_peers = [self.id] + list(self.peers.keys())
        all_peers.sort()
        self.count_var.set(str(len(all_peers)))
        self.text_area.delete(1.0, tk.END)
        for peer in all_peers:
            self.text_area.insert(tk.END, peer + "\n")

    def on_close(self):
        self.send_message(f"BYE|{self.id}")
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMonitor(root)
    root.mainloop()
