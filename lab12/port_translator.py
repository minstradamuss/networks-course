import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, messagebox
from socket import gethostbyname
import os

CONFIG_FILE = "C:\\Users\\User\\Source\\Repos\\networks-course\\lab12\\port_rules.json"

class PortForwarder(threading.Thread):
    def __init__(self, listen_ip, listen_port, forward_ip, forward_port):
        super().__init__(daemon=True)
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.forward_ip = forward_ip
        self.forward_port = forward_port
        self.running = True

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.listen_ip, self.listen_port))
                s.listen()
                while self.running:
                    client_socket, _ = s.accept()
                    threading.Thread(target=self.handle, args=(client_socket,), daemon=True).start()
        except Exception as e:
            print(f"Error on port {self.listen_port}: {e}")

    def handle(self, client_socket):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
                forward_socket.connect((self.forward_ip, self.forward_port))

                threading.Thread(target=self.relay, args=(client_socket, forward_socket), daemon=True).start()
                self.relay(forward_socket, client_socket)
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            client_socket.close()

    def relay(self, src, dst):
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except:
            pass

class PortTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Translator")
        self.forwarders = []

        self.build_gui()
        self.load_config()

    def build_gui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top_frame, text="Host IP:").pack(side=tk.LEFT)
        self.local_ip_entry = tk.Entry(top_frame, width=15)
        self.local_ip_entry.insert(0, "127.0.0.1")
        self.local_ip_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(top_frame, text="Hostname:").pack(side=tk.LEFT, padx=10)
        self.hostname_entry = tk.Entry(top_frame, width=20)
        self.hostname_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(top_frame, text="Resolve IP", command=self.resolve_ip).pack(side=tk.LEFT, padx=2)
        self.ip_label = tk.Label(top_frame, text="")
        self.ip_label.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("name", "internal_ip", "internal_port", "external_ip", "external_port"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Start Translator", command=self.start_translators).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Reload Config", command=self.load_config).pack(side=tk.LEFT, padx=5, pady=5)

    def resolve_ip(self):
        hostname = self.hostname_entry.get()
        try:
            ip = gethostbyname(hostname)
            self.ip_label.config(text=ip)
        except Exception as e:
            messagebox.showerror("Error", f"Could not resolve IP: {e}")

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.rules = []
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.rules, f, indent=2)
        else:
            try:
                with open(CONFIG_FILE, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        raise ValueError("Empty config")
                    self.rules = json.loads(content)
            except Exception:
                messagebox.showerror("Error", "Invalid or empty config file.")
                self.rules = []

        for row in self.tree.get_children():
            self.tree.delete(row)

        for rule in self.rules:
            self.tree.insert('', tk.END, values=(rule.get('name', ''), rule['internal_ip'], rule['internal_port'], rule['external_ip'], rule['external_port']))

    def start_translators(self):
        self.stop_translators()
        for rule in self.rules:
            fwd = PortForwarder(
                listen_ip=rule['internal_ip'],
                listen_port=rule['internal_port'],
                forward_ip=rule['external_ip'],
                forward_port=rule['external_port']
            )
            fwd.start()
            self.forwarders.append(fwd)
        messagebox.showinfo("Success", "Port forwarding started")

    def stop_translators(self):
        for fwd in self.forwarders:
            fwd.running = False
        self.forwarders = []

if __name__ == '__main__':
    root = tk.Tk()
    app = PortTranslatorApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_translators(), root.destroy()))
    root.mainloop()