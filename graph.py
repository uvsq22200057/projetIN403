import random


class Node:
    def __init__(self, idt):
        self.idt = idt
        self.edges = []

    def affichage(self):
        return self.edges


class Network:
    def __init__(self, n):
        self.nodes = [Node(i) for i in range(n)]
        self.graph = {}

    def add_edge(self, id_node1, id_node2, time_comm):
        self.nodes[id_node1].edges.append((id_node2, time_comm))
        self.nodes[id_node2].edges.append((id_node1, time_comm))

    def create_network(self):

        """Backbone"""

        print('TIER 1')
        for i in range(10):
            for j in range(i + 1, 10):
                prob = random.random()
                if prob <= 0.75:
                    time_comm = random.randint(5, 10)
                    self.add_edge(i, j, time_comm)
                    self.graph[(i, j)] = time_comm
                    print(f"Noeud {i} (1) à {j} (1)")

        """Tier 2"""

        print('\nTIER 2')
        for i in range(10, 30):
            nb_tier1 = random.randint(1, 2)

            for _ in range(nb_tier1):
                tier1 = random.randint(0, 9)
                time_comm = random.randint(10, 20)
                self.add_edge(i, tier1, time_comm)
                self.graph[(i, tier1)] = time_comm
                print(f"Noeud {i} (2) à {tier1} (1)")

        edges2_not_full = [[x.idt, 0] for x in self.nodes[10:30]]
        edges2_2 = []

        while edges2_not_full or len(edges2_not_full) == 1:
            n1 = random.randint(0, len(edges2_not_full) - 1)
            n2 = random.randint(0, len(edges2_not_full) - 1)

            while n1 == n2 or n2 in self.nodes[edges2_not_full[n1][0]].edges or n1 in self.nodes[edges2_not_full[n2][0]].edges:
                n1 = random.randint(0, len(edges2_not_full) - 1)
                n2 = random.randint(0, len(edges2_not_full) - 1)

            self.add_edge(edges2_not_full[n1][0], edges2_not_full[n2][0], random.randint(10, 20))
            edges2_not_full[n1][1] += 1
            edges2_not_full[n2][1] += 1
            n1_tier2_edges = edges2_not_full[n1][1]
            n2_tier2_edges = edges2_not_full[n2][1]
            print(f"Noeud {edges2_not_full[n1][0]} (2) à {edges2_not_full[n2][0]} (2)")

            if n1_tier2_edges == 3:
                edges2_not_full.pop(n1)
                if n1 < n2:
                    n2 -= 1
            if n2_tier2_edges == 3:
                edges2_not_full.pop(n2)
                if n2 < n1:
                    n1 -= 1
            if n1_tier2_edges == 2:
                prob = random.random()
                if prob <= 0.5:
                    edges2_2.append(edges2_not_full.pop(n1)[0])
                    if n1 < n2:
                        n2 -= 1
            if n2_tier2_edges == 2:
                prob = random.random()
                if prob <= 0.5:
                    edges2_2.append(edges2_not_full.pop(n2)[0])
        if len(edges2_not_full) == 1:
            while edges2_not_full[0][1] < 2:
                n1 = edges2_not_full[0][0]
                n2 = random.choice(edges2_2)
                self.add_edge(n1, n2, random.randint(10, 20))
                edges2_2.remove(n2)

        """Tier 3"""

        print('\nTIER 3')
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
            print(f"Noeud {i} (3) à {tier2_1} (2)")
            print(f"Noeud {i} (3) à {tier2_2} (2)")


network = Network(100)
network.create_network()

print(network.graph)

for n in network.nodes:
    print(n.affichage())