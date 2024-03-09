import random


# Classe Noeud
class Node:
    def __init__(self, id):
        # Chaque nœud a un identifiant à lui et une liste d'arêtes
        self.id = id
        self.edges = []


# Classe Réseau
class Network:
    def __init__(self, n):
        # Le réseau est caractérisé par l'attribut noeuds qui correspond à une liste de n noeuds.
        self.nodes = [Node(i) for i in range(n)]
        # Le réseau comprend aussi un attribut graphe qui permet d'afficher toutes les caractéristiques dans un
        # dictionnaire.
        self.graph = {}

    # Cette fonction permet d'ajouter une arête au réseau en prenant en paramètre le noeud de depart, celui d'arrivée,
    # et la valeur de l'arête càd le temps de communication.
    def add_edge(self, id_node1, id_node2, time_comm):
        # La fonction ajoute à la liste de noeuds
        self.nodes[id_node1].edges.append((id_node2, time_comm))
        self.nodes[id_node2].edges.append((id_node1, time_comm))

    def create_network(self):

        # Backbone
        for i in range(10):  # 10 noeuds
            for j in range(i+1, 10):
                prob = random.random()
                if prob < 0.75:
                    time_comm = random.randint(5, 10)
                    self.add_edge(i, j, time_comm)
                    self.graph[(i, j)] = time_comm

        # Tier 2
        for i in range(10, 30):
            tier1 = random.randint(0, 9)
            tier2 = random.randint(0, 9)

            time_comm = random.randint(10, 20)
            self.add_edge(i, tier1, time_comm)
            self.add_edge(i, tier2, time_comm)
            self.graph[(i, tier1)] = time_comm
            self.graph[(i, tier2)] = time_comm


        # Tier 3
        for i in range(30, 100):
            tier2_1 = random.randint(10, 29)
            tier2_2 = random.randint(10, 29)
            temps_communication = random.randint(20, 50)
            self.add_edge(i, tier2_1, time_comm)
            self.add_edge(i, tier2_2, time_comm)
            self.graph[(i, tier2_1)] = time_comm
            self.graph[(i, tier2_2)] = time_comm



network = Network(100)
network.create_network()

print(network.graph)
