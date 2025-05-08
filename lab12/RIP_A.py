import json
import random
from collections import defaultdict

MAX_METRIC = 15 

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = {}
        self.routing_table = {ip: (ip, 0)}

    def update_table(self, from_ip, from_table):
        updated = False
        for dest_ip, (next_hop, metric) in from_table.items():
            new_metric = min(metric + self.neighbors[from_ip], MAX_METRIC)
            if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip][1]:
                self.routing_table[dest_ip] = (from_ip, new_metric)
                updated = True
        return updated

    def __str__(self):
        lines = [f"Final state of router {self.ip} table:"]
        lines.append(f"{'[Source IP]':<18}{'[Destination IP]':<20}{'[Next Hop]':<18}{'[Metric]'}")
        for dest_ip, (next_hop, metric) in sorted(self.routing_table.items()):
            lines.append(f"{self.ip:<18}{dest_ip:<20}{next_hop:<18}{metric}")
        return "\n".join(lines)

def generate_random_network(num_routers=5):
    routers = {}
    ip_list = [f"192.168.1.{i}" for i in range(1, num_routers + 1)]
    for ip in ip_list:
        routers[ip] = Router(ip)

    for router in routers.values():
        possible_neighbors = [ip for ip in ip_list if ip != router.ip]
        neighbors = random.sample(possible_neighbors, random.randint(1, len(possible_neighbors)-1))
        for n in neighbors:
            metric = random.randint(1, 5)
            router.neighbors[n] = metric
            routers[n].neighbors[router.ip] = metric

    return routers

def simulate_rip(routers):
    changed = True
    while changed:
        changed = False
        for router in routers.values():
            for neighbor_ip in router.neighbors:
                neighbor = routers[neighbor_ip]
                if neighbor.update_table(router.ip, router.routing_table):
                    changed = True

def main():
    routers = generate_random_network(5)
    simulate_rip(routers)
    for router in routers.values():
        print(router)
        print()

if __name__ == "__main__":
    main()
