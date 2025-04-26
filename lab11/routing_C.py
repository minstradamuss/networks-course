import threading
import queue
import time
from collections import defaultdict

class Node(threading.Thread):
    INF = float('inf')

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.neighbors = {}
        self.routing_table = defaultdict(lambda: self.INF)
        self.next_hop = {}
        self.message_queue = queue.Queue()
        self.running = True
        self.lock = threading.Lock()

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.name] = cost
        self.routing_table[neighbor.name] = cost
        self.next_hop[neighbor.name] = neighbor.name

    def send_vector(self, network):
        vector = dict(self.routing_table)
        for neighbor_name in self.neighbors:
            network[neighbor_name].message_queue.put(('vector', self.name, vector))

    def receive_message(self, message, network):
        type, sender, data = message

        if type == 'vector':
            updated = False
            for dest, cost in data.items():
                if dest == self.name:
                    continue
                new_cost = self.neighbors[sender] + cost
                if new_cost < self.routing_table[dest]:
                    self.routing_table[dest] = new_cost
                    self.next_hop[dest] = sender
                    updated = True

            if updated:
                print(f'[Node {self.name}] Updated routing table: {dict(sorted(self.routing_table.items()))}')
                self.send_vector(network)

        elif type == 'weight':
            new_weight = data
            print(f'[Node {self.name}] Changing weight to {sender} to {new_weight}')
            with self.lock:
                self.neighbors[sender] = new_weight
                self.routing_table[sender] = new_weight
                self.next_hop[sender] = sender
                self.send_vector(network)

    def change_link_cost(self, neighbor_name, new_cost, network):
        self.message_queue.put(('weight', neighbor_name, new_cost))
        network[neighbor_name].message_queue.put(('weight', self.name, new_cost))

    def run(self):
        while self.running:
            try:
                message = self.message_queue.get(timeout=1)
                self.receive_message(message, network)
            except queue.Empty:
                continue

    def stop(self):
        self.running = False

    def __str__(self):
        return f'Node {self.name} routing table: {dict(self.routing_table)}'

def build_network():
    nodes = {str(i): Node(str(i)) for i in range(4)}

    nodes['0'].add_neighbor(nodes['1'], 1)
    nodes['0'].add_neighbor(nodes['2'], 3)
    nodes['0'].add_neighbor(nodes['3'], 7)

    nodes['1'].add_neighbor(nodes['0'], 1)
    nodes['1'].add_neighbor(nodes['2'], 1)

    nodes['2'].add_neighbor(nodes['0'], 3)
    nodes['2'].add_neighbor(nodes['1'], 1)
    nodes['2'].add_neighbor(nodes['3'], 2)

    nodes['3'].add_neighbor(nodes['0'], 7)
    nodes['3'].add_neighbor(nodes['2'], 2)

    return nodes

if __name__ == "__main__":
    network = build_network()

    for node in network.values():
        node.start()

    time.sleep(2)

    for node in network.values():
        node.send_vector(network)

    time.sleep(5)

    print("\n=== Changing the cost of channels ===\n")
    network['1'].change_link_cost('2', 7, network)
    network['0'].change_link_cost('3', 2, network)

    time.sleep(10)

    print("\n=== Final routing tables ===\n")
    for node in network.values():
        print(node)

    for node in network.values():
        node.stop()
        node.join()
