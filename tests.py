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

        """Tier 2"""

        """2-2"""
        edges2_not_full = [i for i in self.nodes[10:30]]
        edges2_2 = []

        while edges2_not_full:
            if len(edges2_not_full) > 1:
                n1 = random.choice(edges2_not_full)
                n2 = random.choice(edges2_not_full)
                while n1 == n2:
                    n1 = random.choice(edges2_not_full)
                    n2 = random.choice(edges2_not_full)
                test = True
                for i in edges2_not_full:
                    for j in edges2_not_full:
                        if i !=j:
                            if i not in (lambda lst: [ngb[0] for ngb in lst])(j.edges) and j not in (lambda lst: [ngb[0] for ngb in lst])(i.edges):
                                test = False
                if test:
                    n2 = random.choice(edges2_2)
                else:
                    while (n1 == n2
                           or n2 in (lambda lst: [ngb[0] for ngb in lst])(n1.edges)
                           or n1 in (lambda lst: [ngb[0] for ngb in lst])(n2.edges)):
                        n1 = random.choice(edges2_not_full)
                        n2 = random.choice(edges2_not_full)
                self.add_edge(n1.idt, n2.idt, random.randint(10, 20))
                n1_tier2_edges = len(n1.edges)
                n2_tier2_edges = len(n2.edges)

            elif len(edges2_not_full) == 1:
                n1 = random.choice(edges2_not_full)
                n2 = random.choice(edges2_2)
                self.add_edge(n1.idt, n2.idt, random.randint(10, 20))
                edges2_2.remove(n2)
                n1_tier2_edges = len(n1.edges)
                n2_tier2_edges = len(n2.edges)

            if n1_tier2_edges == 2:
                edges2_2.append(n1)
                edges2_not_full.remove(n1)

            if n2_tier2_edges == 2:
                edges2_2.append(n2)
                edges2_not_full.remove(n2)

        for i in range(10, 30):
            print(self.nodes[i].edges)

        """"2-1"""""
        for i in range(10, 30):
            nb_tier1 = random.randint(1, 2)

            for _ in range(nb_tier1):
                tier1 = random.randint(0, 9)
                time_comm = random.randint(10, 20)
                self.add_edge(i, tier1, time_comm)
                self.graph[(i, tier1)] = time_comm


        """Backbone"""

        for i in range(10):
            for j in range(i + 1, 10):
                prob = random.random()
                if prob <= 0.75:
                    time_comm = random.randint(5, 10)
                    self.add_edge(i, j, time_comm)
                    self.graph[(i, j)] = time_comm

        """Tier 3"""
        for i in range(30, 100):
            tier2_1 = random.randint(10, 29)
            tier2_2 = random.randint(10, 29)
            while tier2_2 == tier2_1:
                tier2_2 = random.randint(10, 29)
            time_comm = random.randint(20, 50)
            self.add_edge(i, tier2_1, time_comm)
            self.add_edge(i, tier2_2, time_comm)
            self.graph[(i, tier2_1)] = time_comm
            self.graph[(i, tier2_2)] = time_comm


network = Network(100)
network.create_network()

print(network.graph)

for n in network.nodes:
    print(n.idt, n.affichage())
