import random

MAX_METRIC = 15

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = {}
        self.routing_table = {ip: (ip, 0)} 

    def update_table(self, from_ip, from_table):
        updated = False
        cost_to_neighbor = self.neighbors[from_ip]
        for dest_ip, (next_hop, metric) in from_table.items():
            if dest_ip == self.ip:
                continue
            new_metric = min(metric + cost_to_neighbor, MAX_METRIC)
            if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip][1]:
                self.routing_table[dest_ip] = (from_ip, new_metric)
                updated = True
        return updated

    def print_table(self, step=None):
        if step is not None:
            print(f"Simulation step {step} of router {self.ip}")
        else:
            print(f"Final state of router {self.ip} table:")
        print(f"{'[Source IP]':<18}{'[Destination IP]':<20}{'[Next Hop]':<18}{'[Metric]'}")
        for dest_ip, (next_hop, metric) in sorted(self.routing_table.items()):
            print(f"{self.ip:<18}{dest_ip:<20}{next_hop:<18}{metric}")
        print()

def generate_network(n=5):
    routers = {}
    ips = [f"10.0.0.{i}" for i in range(1, n + 1)]
    for ip in ips:
        routers[ip] = Router(ip)

    for router in routers.values():
        possible = [ip for ip in ips if ip != router.ip]
        neighbors = random.sample(possible, random.randint(1, len(possible) - 1))
        for n in neighbors:
            if n not in router.neighbors:
                metric = random.randint(1, 3)
                router.neighbors[n] = metric
                routers[n].neighbors[router.ip] = metric
    return routers

def simulate_rip(routers, max_steps=10):
    step = 0
    while step < max_steps:
        changed = False
        step += 1
        for router in routers.values():
            for neighbor_ip in router.neighbors:
                neighbor = routers[neighbor_ip]
                updated = neighbor.update_table(router.ip, router.routing_table)
                if updated:
                    changed = True

        for router in routers.values():
            router.print_table(step)

        if not changed:
            break

def main():
    routers = generate_network(5)
    simulate_rip(routers)
    print("=" * 60)
    print("Final routing tables:")
    for router in routers.values():
        router.print_table()

if __name__ == "__main__":
    main()
