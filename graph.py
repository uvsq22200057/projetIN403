import random
import plotly.graph_objects as go
import numpy as np
import gradio as gr


"""CLASSES NOEUD ET RÉSEAU"""


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
                        if i != j:
                            if i not in (lambda lst: [ngb[0] for ngb in lst])(j.edges) and j not in (
                                    lambda lst: [ngb[0] for ngb in lst])(i.edges):
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

            # S'il ne restait qu'un élément dans la liste, on prend n2 dans la liste de nœuds à 2 arêtes.
            elif len(edges2_not_full) == 1:
                n1 = random.choice(edges2_not_full)
                n2 = random.choice(edges2_2)
                time_comm = random.randint(10, 20)
                self.add_edge(n1.idt, n2.idt, time_comm)
                edges2_2.remove(n2)

            # On vérifie à chaque fois si les nœuds choisis contiennent 2 arêtes après la création de la nouvelle et si
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


"""FONCTIONS"""


# Fonctions du Parcours en Profondeur pour vérifier la connexité du graphe.
def connected_pp(graph):
    n = len(graph)
    # On initialise la liste des nœuds visités à False.
    visited = {node: False for node in range(n)}
    # On prend un nœud au hasard pour commencer le parcours
    start_node = random.choice(list(graph.keys()))
    pp(graph, start_node, visited)
    # Si tous les nœuds ont été visités, on renvoie True s'ils sont tous à True.
    return all(visited.values())


def pp(graph, node, visited):
    # On dit que le nœud sur lequel on se trouve a été visité.
    visited[node] = True
    # On regarde pour chaque arête de la liste l'id du voisin, s'il n'est pas visité, on continue le parcours en
    # profondeur depuis celui-ci.
    for neighbor, _ in graph[node]:
        if not visited[neighbor]:
            pp(graph, neighbor, visited)


# Fonction de l'algorithme de Dijkstra pour calculer les plus courts chemins.
def dijkstra(graph, node_0):
    # On initialise les distances pour chaque nœud à + infini et on met 0 pour le nœud de départ.
    d = {node: float('infinity') for node in graph}
    d[node_0] = 0
    # On initialise un dictionnaire pour stocker le chemin le plus court pour chaque nœud destination.
    shortest_paths = {}
    # On met tous les nœuds non visités dans une liste.
    unvisited = list(graph.keys())

    # Tant que la liste de nœuds non visités contient des nœuds, on continue.
    while unvisited:
        # On crée une variable pour représenter le nœud le plus proche et on ne met rien dedans au début.
        node_d_min = None
        # On regarde pour chaque nœud non visité s'il a une distance inférieure au nœud le plus proche et si oui, on
        # remplace le nœud le plus proche par celui-ci.
        for node in unvisited:
            if node_d_min is None or d[node] < d[node_d_min]:
                node_d_min = node
        # Si la valeur du nœud le plus proche est à l'infini, on break, sinon on le retire des nœuds non visités.
        if d[node_d_min] == float('infinity'):
            break
        unvisited.remove(node_d_min)

        # On regarde chaque voisin du nœud de distance min et on ajoute le poids de leur arête à la valeur du nœud min
        # puis si cette valeur est meilleure, on la remplace et on ajoute le nœud au chemin actuel.
        for neighbor, weight in graph[node_d_min]:
            dist = d[node_d_min] + weight
            if dist < d[neighbor]:
                d[neighbor] = dist
                shortest_paths[neighbor] = shortest_paths.get(node_d_min, []) + [neighbor]

    items = shortest_paths.items()
    sorted_items = sorted(items)
    sorted_paths = {k: v for k, v in sorted_items}
    return sorted_paths


# Fonction tables de routage
def routing_table(graph):
    # On crée un dictionnaire qui contiendra pour chaque nœud dont le numéro sera la clé, une valeur étant un
    # dictionnaire représentant sa table de routage.
    tables = {}
    # On crée une table pour chaque nœud qui est un dictionnaire qui pour donne pour chaque nœud (clé), le premier
    # nœud par lequel il faut passer (valeur). On calcule Dijkstra pour chaque nœud.
    for node in graph:
        table = {}
        paths = dijkstra(graph, node)

        # Pour chaque plus court chemin depuis le nœud, on prend le premier nœud du chemin.
        for destination_node, path in paths.items():
            if destination_node != node and path:
                next_node = path[0]
                table[destination_node] = next_node

        tables[node] = table

    return tables


# Fonction permettant de retracer le chemin demandé par l'utilisateur
def path_user(graph, n1, n2):
    path = [n1]
    n = n1
    while n != n2:
        path.append(routing_table(graph)[n][n2])
        n = routing_table(graph)[n][n2]

    return path


"""CRÉATION DU RÉSEAU"""

network = Network(100)
network.create_network()

graph = {}
for n in network.nodes:
    graph[n.idt] = n.affichage()

# On relance la création d'un réseau s'il n'est pas connexe
while not connected_pp(graph):
    network = Network(100)
    network.create_network()
    graph = {}
    for n in network.nodes:
        graph[n.idt] = n.affichage()

print("Graphe : ", graph)
print("Connexe : ", connected_pp(graph))
print("Dijkstra 0 : ", dijkstra(graph, 0))
print("Tables de routage : ", routing_table(graph))
# print(path_user(graph, int(input("Saisissez le numéro du noeud émetteur de message:")),
# int(input("Saisissez le numéro du noeud destinataire:"))))


"""VISUALISATION"""

# Création de la fonction pour visualiser le graphe
def visualize_graph_3d(node1, node2):
    # Fixer le nombre de nœuds à 100
    num_nodes = 100

    # Création de la figure
    fig = go.Figure()

    # Création des nœuds avec des coordonnées aléatoires
    for node in range(num_nodes):
        x = np.random.rand()
        y = np.random.rand()
        z = np.random.rand()
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', name=f'Node {node}'))

    # Si les nœuds de départ et d'arrivée sont spécifiés
    if node1 != 0 or node2 != 0:
        # Affichage des arêtes du chemin calculé
        path = path_user(graph, node1, node2)
        for i in range(len(path) - 1):
            x1, y1, z1 = fig.data[int(path[i])].x[0], fig.data[int(path[i])].y[0], fig.data[int(path[i])].z[0]
            x2, y2, z2 = fig.data[int(path[i + 1])].x[0], fig.data[int(path[i + 1])].y[0], fig.data[int(path[i + 1])].z[0]
            fig.add_trace(
                go.Scatter3d(x=[x1, x2], y=[y1, y2], z=[z1, z2], mode='lines', name=f'Path {path[i]}-{path[i + 1]}',
                             line=dict(color='red', width=4)))
        shortest_path_text = "Le plus court chemin du noeud {} au noeud {} est :".format(node1, node2)
        shortest_path_text += "<br>" + " -> ".join(str(node) for node in path)
    else:
        # Ajout des arêtes en noir
        for node1 in range(num_nodes):
            for node2, _ in graph[node1]:
                x1, y1, z1 = fig.data[node1].x[0], fig.data[node1].y[0], fig.data[node1].z[0]
                x2, y2, z2 = fig.data[node2].x[0], fig.data[node2].y[0], fig.data[node2].z[0]
                fig.add_trace(
                    go.Scatter3d(x=[x1, x2], y=[y1, y2], z=[z1, z2], mode='lines', name=f'Edge {node1}-{node2}',
                                 line=dict(color='black', width=2)))
        shortest_path_text = ""

    # Configuration de la mise en page
    fig.update_layout(title='3D Graph Visualization', autosize=True)
    fig.update_layout(annotations=[
        dict(x=0.5, y=-0.15, showarrow=False, text=shortest_path_text, xref="paper", yref="paper", align="center",
             font=dict(size=12))])

    # Affichage de la figure
    return fig


# Création des entrées pour Gradio
node1_input = gr.Slider(label="Choix du nœud 1", minimum=0, maximum=100, step=1)
node2_input = gr.Slider(label="Choix du nœud 2", minimum=0, maximum=100, step=1)

# Interface Gradio

gr.Interface(fn=visualize_graph_3d, inputs=[node1_input, node2_input], outputs="plot", title="En route avec Thierry").launch()
