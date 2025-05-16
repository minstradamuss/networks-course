import random
import json
from collections import defaultdict

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = []
        self.routing_table = {ip: (ip, 0)}

    def add_neighbor(self, neighbor_ip):
        self.neighbors.append(neighbor_ip)
        self.routing_table[neighbor_ip] = (neighbor_ip, 1)

    def update_table(self, neighbor_router):
        updated = False
        for dest_ip, (next_hop, metric) in neighbor_router.routing_table.items():
            if dest_ip == self.ip:
                continue
            new_metric = metric + 1
            if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip][1]:
                self.routing_table[dest_ip] = (neighbor_router.ip, new_metric)
                updated = True
        return updated

def generate_network(num_routers=5):
    routers = {}
    ips = [f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
           for _ in range(num_routers)]
    for ip in ips:
        routers[ip] = Router(ip)

    for router in routers.values():
        neighbors = random.sample(list(routers.keys()), random.randint(1, 3))
        for neighbor in neighbors:
            if neighbor != router.ip:
                router.add_neighbor(neighbor)
                routers[neighbor].add_neighbor(router.ip)
    return routers

def run_rip(routers, iterations=5):
    for _ in range(iterations):
        for router in routers.values():
            for neighbor_ip in router.neighbors:
                neighbor = routers[neighbor_ip]
                router.update_table(neighbor)

def print_tables(routers):
    for router in routers.values():
        print(f"\nFinal state of router {router.ip} table:")
        print(f"{'[Source IP]':<17}{'[Destination IP]':<20}{'[Next Hop]':<17}{'[Metric]'}")
        for dest_ip, (next_hop, metric) in router.routing_table.items():
            print(f"{router.ip:<17}{dest_ip:<20}{next_hop:<17}{metric}")

if __name__ == "__main__":
    routers = generate_network()
    run_rip(routers)
    print_tables(routers)