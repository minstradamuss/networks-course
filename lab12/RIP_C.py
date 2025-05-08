import threading
import socket
import json
import time
import random

MAX_METRIC = 15
ROUTER_COUNT = 4
BASE_PORT = 5000

print_lock = threading.Lock()

class Router(threading.Thread):
    def __init__(self, ip, port, neighbors):
        super().__init__()
        self.ip = ip
        self.port = port
        self.neighbors = neighbors
        self.routing_table = {ip: {"next_hop": ip, "metric": 0}}
        self.running = True

    def run(self):
        server_thread = threading.Thread(target=self.server)
        server_thread.start()

        time.sleep(1)

        for _ in range(5):
            self.broadcast_table()
            time.sleep(1)

        self.running = False
        server_thread.join()
        self.print_table()

    def server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", self.port))
        s.listen()
        while self.running:
            s.settimeout(1)
            try:
                conn, _ = s.accept()
                data = conn.recv(4096)
                if data:
                    message = json.loads(data.decode())
                    sender_ip = message["source"]
                    sender_table = message["table"]
                    self.update_table(sender_ip, sender_table)
                conn.close()
            except socket.timeout:
                continue
        s.close()

    def broadcast_table(self):
        table_to_send = {"source": self.ip, "table": self.routing_table}
        encoded = json.dumps(table_to_send).encode()
        for neighbor_ip, neighbor_port in self.neighbors.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(("localhost", neighbor_port))
                sock.send(encoded)
                sock.close()
            except:
                continue

    def update_table(self, sender_ip, sender_table):
        for dest_ip, entry in sender_table.items():
            if dest_ip == self.ip:
                continue
            new_metric = min(entry["metric"] + 1, MAX_METRIC)
            if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip]["metric"]:
                self.routing_table[dest_ip] = {
                    "next_hop": sender_ip,
                    "metric": new_metric
                }

    def print_table(self):
        with print_lock:
            print(f"\nFinal routing table of router {self.ip}:")
            print(f"{'[Source IP]':<18}{'[Destination IP]':<20}{'[Next Hop]':<18}{'[Metric]'}")
            for dest, data in sorted(self.routing_table.items()):
                print(f"{self.ip:<18}{dest:<20}{data['next_hop']:<18}{data['metric']}")
            print()

def generate_routers():
    routers = {}
    ports = {}

    for i in range(ROUTER_COUNT):
        ip = f"10.0.0.{i+1}"
        port = BASE_PORT + i
        routers[ip] = {"port": port, "neighbors": {}}
        ports[ip] = port

    for ip in routers:
        other_ips = [x for x in routers if x != ip]
        chosen = random.sample(other_ips, random.randint(1, len(other_ips)-1))
        for neighbor_ip in chosen:
            routers[ip]["neighbors"][neighbor_ip] = ports[neighbor_ip]

    return routers

def main():
    network = generate_routers()
    threads = []
    for ip, data in network.items():
        router = Router(ip, data["port"], data["neighbors"])
        threads.append(router)
        router.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
