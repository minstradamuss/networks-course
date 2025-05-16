import socket
import threading
import json
import random
import time
from queue import Queue

print_lock = threading.Lock()
result_queue = Queue()        

class RouterThread(threading.Thread):
    def __init__(self, ip, neighbors, port):
        super().__init__()
        self.ip = ip
        self.neighbors = neighbors
        self.port = port
        self.routing_table = {ip: (ip, 0)}
        self.running = True

    def send_table(self):
        for neighbor_ip, neighbor_port in self.neighbors.items():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                message = json.dumps({
                    "sender": self.ip,
                    "table": self.routing_table
                }).encode()
                s.sendto(message, ("127.0.0.1", neighbor_port))

    def update_table(self, received_table, sender_ip):
        changed = False
        for dest_ip, (next_hop, metric) in received_table.items():
            if dest_ip == self.ip:
                continue
            new_metric = metric + 1
            if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip][1]:
                self.routing_table[dest_ip] = (sender_ip, new_metric)
                changed = True
        return changed

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", self.port))
        sock.settimeout(1)

        for _ in range(5):
            self.send_table()
            try:
                while True:
                    data, _ = sock.recvfrom(4096)
                    msg = json.loads(data.decode())
                    self.update_table(msg['table'], msg['sender'])
            except socket.timeout:
                pass
            time.sleep(1)

        sock.close()
        result_queue.put((self.ip, dict(self.routing_table)))

def print_table(ip, table):
    with print_lock:
        print(f"\nRouter {ip} final table:")
        print(f"{'[Source IP]':<17}{'[Destination IP]':<20}{'[Next Hop]':<17}{'[Metric]'}")
        for dest_ip in sorted(table):
            next_hop, metric = table[dest_ip]
            print(f"{ip:<17}{dest_ip:<20}{next_hop:<17}{metric}")

def generate_network_threads():
    base_port = 10000
    routers = {}
    ips = [f"10.0.0.{i}" for i in range(1, 6)]
    ports = {ip: base_port + i for i, ip in enumerate(ips)}

    connections = {ip: {} for ip in ips}
    for ip in ips:
        neighbors = random.sample([i for i in ips if i != ip], random.randint(1, 3))
        for neighbor in neighbors:
            connections[ip][neighbor] = ports[neighbor]
            connections[neighbor][ip] = ports[ip]

    for ip in ips:
        routers[ip] = RouterThread(ip, connections[ip], ports[ip])

    return list(routers.values())

if __name__ == "__main__":
    threads = generate_network_threads()
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    while not result_queue.empty():
        ip, table = result_queue.get()
        print_table(ip, table)
