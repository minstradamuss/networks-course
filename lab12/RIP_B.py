from RIP_A import generate_network, Router

def run_rip_verbose(routers, iterations=5):
    for i in range(1, iterations + 1):
        print(f"\n--- Simulation step {i} ---")
        for router in routers.values():
            for neighbor_ip in router.neighbors:
                neighbor = routers[neighbor_ip]
                router.update_table(neighbor)
        for router in routers.values():
            print(f"\nSimulation step {i} of router {router.ip}")
            print(f"{'[Source IP]':<17}{'[Destination IP]':<20}{'[Next Hop]':<17}{'[Metric]'}")
            for dest_ip, (next_hop, metric) in router.routing_table.items():
                print(f"{router.ip:<17}{dest_ip:<20}{next_hop:<17}{metric}")

if __name__ == "__main__":
    routers = generate_network()
    run_rip_verbose(routers)
