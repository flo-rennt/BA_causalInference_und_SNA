import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from cdlib import algorithms
import community as community_louvain
from networkx.algorithms import community as nx_comm
import itertools

# ------ Graph aus TikTok Daten erstellen ------ #

# Daten einlesen
data = pd.read_csv("tt_outlet_sample.csv")
# Standardisierung
data['id-account'] = data['id-account'].astype(str).str.strip()
data['follows'] = data['follows'].astype(str).str.strip()

G = nx.DiGraph()
G.add_nodes_from(data['id-account'].unique())
# Kanten über Follow-Relation
for _, row in data.iterrows():
    follower = row['id-account']
    follows = [f.strip() for f in row['follows'].split(',') if f.strip()]
    for followee in follows:
        G.add_edge(follower, followee)

print("== Grundlegende Graphinformationen ==")
print(f"Anzahl der Knoten: {G.number_of_nodes()}")
print(f"Anzahl der Kanten: {G.number_of_edges()}\n")

# ------ Community Detection durchführen ------ #

# Konvertieren zu ungerichtetem Graphen 
G_undirected = G.to_undirected()

# Louvain-Algorithmus
print("-----")
print("1. Louvain-Algorithmus")
louvain_partition = community_louvain.best_partition(G_undirected) #Dictionary das jedem Node seine Community zuordnet
louvain_communities = {}
# Erstellen eines Dictionary, das jeder Community alle darin enthaltenen Nodes zuordnet: 
for node, community_id in louvain_partition.items():
    louvain_communities.setdefault(community_id, []).append(node)

num_louvain_communities = len(louvain_communities)
print(f"Anzahl der gefundenen Communities: {num_louvain_communities}")
for i, (comm_id, members) in enumerate(louvain_communities.items()):
    if i < num_louvain_communities:
        print(f"Community {comm_id}: {members[:10]} ... ({len(members)} Mitglieder)")
print("\n")
print("-----")
print("\n")


# Girvan-Newman-Algorithmus
print("-----")
print("2. Girvan-Algorithmus")
# Festlegen des Abbruchskriteriums hier über gewünschte Anzahl an Communities
# Wir nutzen die gleiche Anzahl wie bei Louvain
number_coms = num_louvain_communities
cm = nx_comm.girvan_newman(G_undirected)
limited = itertools.takewhile(lambda c: len(c) <= number_coms, cm)
girvan_newman_communities = None
for communities in limited:
    girvan_newman_communities = [list(c) for c in communities]

num_gn_communities = len(girvan_newman_communities)
print(f"Anzahl der gefundenen Communities: {num_gn_communities}")

# Printausgabe der Communities
for i, community in enumerate(girvan_newman_communities):
    if i < number_coms:
        print(f"Community {i}: {community[:10]} ... ({len(community)} Mitglieder)")
print("\n")
print("-----")
print("\n")

# Walktrap-Algorithmus
print("-----")
print("3. Walktrap-Algorithmus")
walktrap_result = algorithms.walktrap(G_undirected)
walktrap_communities = walktrap_result.communities
num_walktrap_communities = len(walktrap_communities)
print(f"Anzahl der gefundenen Communities: {num_walktrap_communities}")
print(f"Hier die ersten {number_coms} Communities:")
# Ausgabe der ersten paar Communities (falls mehr als Louvain & Girvan werden genau so viele wie bei den beiden auch ausgegeben)
for i, community in enumerate(walktrap_communities):
    if i < number_coms:
        print(f"Community {i}: {community[:10]} ... ({len(community)} Mitglieder)")
print("\n")
print("-----")
print("\n")


# ------ Visualisierung ------ #

print("== Visualisierung der Communities ==")
print("\n")
def create_community_node_colors(graph, communities):
    number_of_colors = len(communities)
    cmap = plt.get_cmap("tab20")
    colors = [cmap(i) for i in range(number_of_colors)]
    node_colors = []
    for node in graph:
        current_community_index = 0
        for community in communities:
            if node in community:
                node_colors.append(colors[current_community_index])
                break
            current_community_index += 1
    return node_colors

def visualize_communities(G, communities, title, filename):
    pos = nx.spring_layout(G, k=0.4, iterations=50, seed=2)
    plt.figure(figsize=(12, 8))
    cmap = plt.get_cmap('tab20')
    node_colors = create_community_node_colors(G, communities)
    nx.draw(
        G,
        pos=pos,
        node_size=250,
        node_color=node_colors,
        with_labels=True,
        font_size=14,
        font_color="black",
        alpha=0.8,
    )
    plt.title(title)
    plt.savefig(filename, dpi=300)
    plt.show()
    print(f"Visualisierung gespeichert als {filename}\n")

# Visualisierung für Louvain
visualize_communities(G, louvain_communities.values(), "Louvain Community Detection", "louvain_communities.jpg")
# Visualisierung für Girvan-Newman
visualize_communities(G, girvan_newman_communities, "Girvan-Newman Community Detection", "girvan_newman_communities.jpg")
# Visualisierung für Walktrap
visualize_communities(G, walktrap_communities, "Walktrap Community Detection", "walktrap_communities.jpg")

# ------ Zusammenfassung ------ #

print("\n")
print("== Zusammenfassung ==")
print(f"- Louvain hat {num_louvain_communities} Communities gefunden.")
print(f"- Girvan-Newman hat {num_gn_communities} Communities gefunden. Dies liegt aber aufgrund der Implementierung. Die Anzahl der gewünschten Communities kann angegeben werden. Alternativ können andere Abbruchkriterien (Veränderungen bzgl. Modularität, Anzahl an Iterationen, an Laufzeit, etc.) angegeben werden.")
print(f"- Walktrap hat {num_walktrap_communities} Communities gefunden.\n")


# ------ QUELLEN ------ #

# Teile des Codes, vor allem zur (Visualisierung des) Girvan Algorithmus wurden hieraus kopiert: https://networkx.org/documentation/stable/auto_examples/algorithms/plot_girvan_newman.html
# Girvan-Newman Algorithmus: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html
# Walktrap: https://cdlib.readthedocs.io/en/v0.1.9/reference/cd_algorithms/algs/cdlib.algorithms.walktrap.html
# Louvain: https://readthedocs.org/projects/python-louvain/downloads/pdf/latest/
# Overview: https://towardsdatascience.com/community-detection-algorithms-9bd8951e7dae
