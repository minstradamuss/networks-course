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

    def change_weight(self, neighbor_name, new_weight):
        print(f"[Node {self.name}] Changing weight to neighbor {neighbor_name} to {new_weight}")
        self.neighbors[neighbor_name] = new_weight
        self.routing_table[neighbor_name] = new_weight
        self.next_hop[neighbor_name] = neighbor_name

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

def compare_tables(actual, expected):
    for node_name, expected_table in expected.items():
        actual_table = {k: actual[node_name].routing_table[k] for k in expected_table.keys()}
        if actual_table != expected_table:
            print(f"Test failed for node {node_name}.")
            print(f"Expected: {expected_table}")
            print(f"Got: {actual_table}\n")
            return False
    print("All tests passed!\n")
    return True

def test_change_weights():
    nodes = build_network()
    print("=== Initial network setup ===")
    distance_vector_routing(nodes)

    for node in nodes.values():
        print(node)

    print("\n=== Changing weights ===")
    nodes['1'].change_weight('2', 7)
    nodes['2'].change_weight('1', 7)
    nodes['0'].change_weight('3', 2)
    nodes['3'].change_weight('0', 2)

    distance_vector_routing(nodes)

    print("\n=== Updated routing tables ===")
    for node in nodes.values():
        print(node)

    expected_tables = {
        '0': {'1': 1, '2': 2, '3': 2},
        '1': {'0': 1, '2': 3, '3': 3},
        '2': {'0': 2, '1': 4, '3': 2},
        '3': {'0': 2, '2': 2, '1': 3},
    }

    compare_tables(nodes, expected_tables)

def test_simple_network():
    nodes = build_network()
    distance_vector_routing(nodes)

    expected_tables = {
        '0': {'1': 1, '2': 2, '3': 4},
        '1': {'0': 1, '2': 1, '3': 3},
        '2': {'0': 2, '1': 1, '3': 2},
        '3': {'0': 4, '2': 2, '1': 3},
    }

    print("\n=== Running simple network test ===")
    compare_tables(nodes, expected_tables)

if __name__ == "__main__":
    test_simple_network()
    test_change_weights()
