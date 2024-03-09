import random


class Node:
    def __init__(self, id):
        self.id = id
        self.edges = []


# Classe Réseau
class Network:
    def __init__(self, n):
        self.nodes = [Node(i) for i in range(n)]
        self.graph = {}

    def add_edge(self, id_node1, id_node2, time_comm):
        self.nodes[id_node1].edges.append((id_node2, time_comm))
        self.nodes[id_node2].edges.append((id_node1, time_comm))

    def create_network(self):

        # Backbone

        for i in range(10):
            for j in range(i + 1, 10):
                prob = random.random()
                if prob < 0.75:
                    time_comm = random.randint(5, 10)
                    self.add_edge(i, j, time_comm)
                    self.graph[(i, j)] = time_comm

        # Tier 2

        for i in range(10, 30):
            nb_tier1 = random.randint(1, 2)
            nb_tier2 = random.randint(2, 3)

            for _ in range(nb_tier1):
                tier1 = random.randint(0, 9)
                time_comm = random.randint(10, 20)
                self.add_edge(i, tier1, time_comm)
                self.graph[(i, tier1)] = time_comm

            for _ in range(nb_tier2):
                tier2 = i
                while tier2 == i:
                    tier2 = random.randint(i+1, 30)
                time_comm = random.randint(10, 20)
                self.add_edge(i, tier2, time_comm)
                self.graph[(i, tier2)] = time_comm

        # Tier 3

        for i in range(30, 100):
            tier2_1 = random.randint(10, 29)
            tier2_2 = random.randint(10, 29)
            while tier2_2 == tier2_1:
                tier2_2 = random.randint(20, 50)
            time_comm = random.randint(20, 50)
            self.add_edge(i, tier2_1, time_comm)
            self.add_edge(i, tier2_2, time_comm)
            self.graph[(i, tier2_1)] = time_comm
            self.graph[(i, tier2_2)] = time_comm


network = Network(100)
network.create_network()

print(network.graph)
