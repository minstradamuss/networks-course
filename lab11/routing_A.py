from collections import defaultdict
import copy

class Node:
    INF = float('inf')

    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = defaultdict(lambda: self.INF)
        self.next_hop = {}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.name] = cost
        self.routing_table[neighbor.name] = cost
        self.next_hop[neighbor.name] = neighbor.name

    def send_vector(self):
        return copy.deepcopy(self.routing_table)

    def update_table(self, sender, vector):
        updated = False
        for dest, cost in vector.items():
            if dest == self.name:
                continue

            new_cost = self.neighbors[sender] + cost
            if new_cost < self.routing_table[dest]:
                self.routing_table[dest] = new_cost
                self.next_hop[dest] = sender
                updated = True
        return updated

    def __str__(self):
        table = dict(self.routing_table)
        return f'Node {self.name} routing table: {table}'

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

def distance_vector_routing(nodes):
    updated = True
    while updated:
        updated = False
        for node in nodes.values():
            vector = node.send_vector()
            for neighbor_name in node.neighbors:
                neighbor = nodes[neighbor_name]
                if neighbor.update_table(node.name, vector):
                    updated = True

if __name__ == "__main__":
    nodes = build_network()
    distance_vector_routing(nodes)

    for node in nodes.values():
        print(node)
