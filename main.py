import random


# Classe Noeud
class Node:
    def __init__(self, idt):
        # Chaque objet nœud qui va être créé aura un identifiant à lui (qui correspondra à un numéro entre 0 et 99)
        # et une liste d'arêtes.
        self.idt = idt
        self.edges = []


# Classe Réseau
class Network:
    def __init__(self, n):
        # Le réseau est caractérisé par l'attribut nœuds qui correspond à une liste de n nœuds, ainsi qu'un attribut
        # graphe qui permet d'afficher toutes les caractéristiques dans un dictionnaire.
        self.nodes = [Node(i) for i in range(n)]
        self.graph = {}

    # Cette fonction permet d'ajouter une arête au réseau en prenant en paramètre le nœud de depart, celui d'arrivée,
    # et la valeur de l'arête càd le temps de communication.
    def add_edge(self, id_node1, id_node2, time_comm):
        # La fonction ajoute aux 2 nœuds (qui sont contenus dans la liste de nœuds), l'arête que l'on souhaite créer
        # entre les 2 avec un temps de communication.
        self.nodes[id_node1].edges.append((id_node2, time_comm))
        self.nodes[id_node2].edges.append((id_node1, time_comm))

    # Cette fonction met en place le réseau càd qu'elle crée tous les nœuds et arêtes et notamment les liens entre eux.
    def create_network(self):

        """Backbone"""

        # Pour les 10 nœuds qui ont un id allant de 0 à 9.
        for i in range(10):
            # On itère sur les nœuds de i+1 à 9 pour créer des connexions qui ne se répètent pas.
            for j in range(i + 1, 10):
                # On choisit à chaque fois un nombre entre 0 et 1 aléatoirement qui correspond à la probabilité que
                # l'arête existe entre les nœuds i et j, et si on se trouve sous 0,75 on crée alors l'arête.
                prob = random.random()
                if prob <= 0.75:
                    # On donne une valeur de temps de communication comprise entre 5 et 10.
                    time_comm = random.randint(5, 10)
                    # On ajoute au réseau l'arête entre i et j avec son temps de communication.
                    self.add_edge(i, j, time_comm)
                    # On la stocke également dans le dictionnaire graphe pour le moment pour les affichages et vérifs.
                    self.graph[(i, j)] = time_comm

        """Tier 2"""

        # Pour les 20 nœuds qui ont un id de 10 à 29
        for i in range(10, 30):
            # On choisit un nombre aléatoirement entre 1 et 2 pour savoir combien d'arête on lui crée avec les nœuds
            # du Tier1.
            nb_tier1 = random.randint(1, 2)
            # Pour le nombre d'arêtes à créer, on fait :
            for _ in range(nb_tier1):
                # On choisit un nœud aléatoire du Tier1 càd avec un id entre 0 et 9.
                tier1 = random.randint(0, 9)
                # On attribue une valeur de temps de communication entre 10 et 20.
                time_comm = random.randint(10, 20)
                # On crée l'arête.
                self.add_edge(i, tier1, time_comm)
                self.graph[(i, tier1)] = time_comm

        # On crée une liste avec les nœuds du Tier 2 qui peuvent créer des relations avec d'autres du Tier 2 càd qui
        # ne sont pas au max (3).
        edges2_not_full = [[x.idt, 0] for x in self.nodes[10:30]]

        # Tant que la liste est vide càd qu'on n'a pas tous les sommets du Tier 2 qui ont 2 ou 3 arêtes avec les autres.
        while edges2_not_full or len(edges2_not_full) == 1:
            # On choisit 2 positions aléatoires pour prendre dans la liste de nœuds, entre 0 et la taille de la liste.
            n1 = random.randint(0, len(edges2_not_full) - 1)
            n2 = random.randint(0, len(edges2_not_full) - 1)

            # Tant qu'on a les 2 mêmes valeurs pour les positions des nœuds dans la liste, on retire des nombres
            # aléatoires, de même lorsqu'on a déja une arête entre les 2 nœuds.
            while n1 == n2 or n2 in self.nodes[edges2_not_full[n1][0]].edges or n1 in self.nodes[edges2_not_full[n2][0]].edges:
                n1 = random.randint(0, len(edges2_not_full) - 1)
                n2 = random.randint(0, len(edges2_not_full) - 1)

            # Une fois que les valeurs sont bonnes, on crée l'arête et
            self.add_edge(edges2_not_full[n1][0], edges2_not_full[n2][0], random.randint(10, 20))
            edges2_not_full[n1][1] += 1
            edges2_not_full[n2][1] += 1
            n1_tier2_edges = edges2_not_full[n1][1]
            n2_tier2_edges = edges2_not_full[n2][1]

            # Si le nombre d'arêtes du nœud 1 ou du nœud 2 est 3 alors on le retire de la liste.
            if n1_tier2_edges == 3:
                edges2_not_full.pop(n1)
                if n1 < n2:
                    n2 -= 1
            if n2_tier2_edges == 3:
                edges2_not_full.pop(n2)
                if n2 < n1:
                    n1 -= 1
            # Si le nombre d'arêtes est 2, alors on choisit un nombre aléatoire entre 0 e 1 et s'il se trouve sous la
            # probabilité de 0.5 alors on retire le nœud de la liste. Ainsi on a pour chacun soit 2 soit 3 arêtes.
            if n1_tier2_edges == 2:
                prob = random.random()
                if prob <= 0.5:
                    edges2_not_full.pop(n1)
                    if n1 < n2:
                        n2 -= 1
            if n2_tier2_edges == 2:
                prob = random.random()
                if prob <= 0.5:
                    edges2_not_full.pop(n2)

        """Tier 3"""

        # Pour les 30 nœuds qui ont un id de 30 à 99.
        for i in range(30, 100):
            # On choisit 2 id de nœuds du Tier 2 avec lesquels créer des arêtes.
            tier2_1 = random.randint(10, 29)
            tier2_2 = random.randint(10, 29)
            # Tant quu'il ne sont pas différents on re tire des nombres.
            while tier2_2 == tier2_1:
                tier2_2 = random.randint(20, 50)
            # On donne un temps de communication entre 20 et 50.
            time_comm = random.randint(20, 50)
            # On crée les 2 arêtes.
            self.add_edge(i, tier2_1, time_comm)
            self.add_edge(i, tier2_2, time_comm)
            self.graph[(i, tier2_1)] = time_comm
            self.graph[(i, tier2_2)] = time_comm


# On crée 100 noeuds
network = Network(100)
# On crée le réseau càd le graphe
network.create_network()

# J'affiche juste le dico graphe qui contient toutes les arêtes pour vérif.
print(network.graph)
