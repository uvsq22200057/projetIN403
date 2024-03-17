import random


class Node:
    # Chaque objet nœud qui va être créé aura un identifiant à lui (qui correspondra à un numéro entre 0 et 99)
    # et une liste d'arêtes, dont chacune correspondra à un tuple contenant d'abord le nœud auquel on se connecte
    # puis la valeur du temps de communication.
    def __init__(self, idt):
        self.idt = idt
        self.edges = []

    # Fonction pour afficher toutes les arêtes, à supprimer plus tard.
    def affichage(self):
        return self.edges


class Network:
    # Le réseau est caractérisé par l'attribut nœuds qui correspond à une liste de n nœuds (ainsi qu'un attribut
    # graphe qui correspond à un dictionnaire dont les clés sont des couples de nœuds reliés entre eux et la valeur
    # correspond au temps de communication de l'arête → juste pour les vérifications).
    def __init__(self, n):
        self.nodes = [Node(i) for i in range(n)]
        self.graph = {}

    # Cette fonction permet d'ajouter une arête au réseau en prenant en paramètre le nœud de depart, celui d'arrivée,
    # et la valeur de l'arête càd le temps de communication.
    def add_edge(self, id_node1, id_node2, time_comm):
        self.nodes[id_node1].edges.append((id_node2, time_comm))
        self.nodes[id_node2].edges.append((id_node1, time_comm))

    # Cette fonction met en place le réseau càd qu'elle crée tous les nœuds et arêtes et notamment les liens entre eux.
    def create_network(self):

        """Tier 2"""

        """Tier 2 - Tier 2"""
        # On crée une liste avec tous les nœuds qui ne sont pas pleins càd à 2 arêtes, puis une liste vide qui
        # accueillera tous ceux qui ont pile 2 arêtes.
        edges2_not_full = [i for i in self.nodes[10:30]]
        edges2_2 = []

        # Tant que la liste des nœuds qui ne sont pas pleins n'est pas vide, on continue.
        while edges2_not_full:
            # S'il reste plus d'un élément dans la liste, on en prend 2 au hasard à connecter et on s'assure qu'ils
            # sont différents.
            if len(edges2_not_full) > 1:
                n1 = random.choice(edges2_not_full)
                n2 = random.choice(edges2_not_full)
                while n1 == n2:
                    n1 = random.choice(edges2_not_full)
                    n2 = random.choice(edges2_not_full)
                # On met un flag test à True
                test = True
                # Pour chaque couple possible de nœuds parmi ceux dans la liste des non pleins, on vérifie qu'ils soient
                # différents et pas déjà présents dans les arêtes de l'autre, si c'est ok, on met test à False, sinon il
                # reste à True. S'il est à True, on choisit n2 dans la liste des nœuds à 2 arêtes, sinon dans la liste
                # des non pleins.
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
                time_comm = random.randint(10, 20)
                self.add_edge(n1.idt, n2.idt, time_comm)
                self.graph[(n1, n2)] = time_comm

            # S'il ne restait qu'un élément dans la liste, on prend n2 dans la liste de nœuds à 2 arêtes.
            elif len(edges2_not_full) == 1:
                n1 = random.choice(edges2_not_full)
                n2 = random.choice(edges2_2)
                time_comm = random.randint(10, 20)
                self.add_edge(n1.idt, n2.idt, time_comm)
                self.graph[(n1, n2)] = time_comm
                edges2_2.remove(n2)

            # On vérifie à chaque fois si les nœuds choisis contiennent 2 arêtes après la création de la noivelle et si
            # oui, on les supprime de la liste des nœuds non pleins pour l'ajouter à celle des nœuds à 2 arêtes
            if len(n1.edges) == 2:
                edges2_2.append(n1)
                edges2_not_full.remove(n1)

            if len(n2.edges) == 2:
                edges2_2.append(n2)
                edges2_not_full.remove(n2)

        """"Tier 2 - Tier 1"""""
        for i in range(10, 30):
            # On choisit un nombre aléatoirement entre 1 et 2 pour savoir combien d'arête on lui crée avec les nœuds
            # du Tier1.
            nb_tier1 = random.randint(1, 2)

            for _ in range(nb_tier1):
                tier1 = random.randint(0, 9)
                time_comm = random.randint(10, 20)
                self.add_edge(i, tier1, time_comm)
                self.graph[(i, tier1)] = time_comm

        """Backbone"""

        """Tier 1 - Tier 1"""
        for i in range(10):
            for j in range(i + 1, 10):
                # On choisit à chaque fois un nombre entre 0 et 1 aléatoirement qui correspond à la probabilité que
                # l'arête existe entre les nœuds i et j, et si on se trouve sous 0,75 on crée alors l'arête.
                prob = random.random()
                if prob <= 0.75:
                    time_comm = random.randint(5, 10)
                    self.add_edge(i, j, time_comm)
                    self.graph[(i, j)] = time_comm

        """Tier 3"""

        " Tier 3 - Tier 2"
        for i in range(30, 100):
            # On choisit 2 id de nœuds du Tier 2 avec lesquels créer des arêtes.
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
