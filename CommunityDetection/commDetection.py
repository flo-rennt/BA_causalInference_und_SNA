import pandas as pd
import ast
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
import collections
from community import community_louvain
from networkx import algorithms
from cdlib import algorithms

# Daten einlesen
data = pd.read_csv('updated_final_user_data.csv')

# Liste aus following
data['following'] = data['following'].apply(ast.literal_eval)

# Erstellen eines gerichteten Graphen
G = nx.DiGraph()

# Knoten und Kanten hinzufügen
for _, row in data.iterrows():
    follower = row['username']
    follows = row['following']
    for followee in follows:
        if followee != follower:  # Selbstkanten ausschließen
            G.add_edge(followee, follower)

# Farben für die Communities festlegen
community_colors = {
    'Centrist': 'lightblue',
    'Environmental': 'green',
    'Left-Wing': 'red',
    'Right-Wing': 'orange',
    'Economic Reform': 'purple'
}

# Knoten entsprechend der Community einfärben
def assign_colors(G, data):
    node_colors = []
    for node in G.nodes():
        community = data.loc[data['username'] == node, 'community']
        if not community.empty:
            color = community_colors.get(community.values[0], 'gray')
            node_colors.append(color)
        else:
            node_colors.append('gray') 
    return node_colors

# Visualisieren und Speichern des Graphen
def visualize_graph(G, title, filename):
    pos = nx.spring_layout(G)  # Layout
    plt.figure(figsize=(12, 8))
    node_colors = assign_colors(G, data)
    nx.draw(G, pos, node_size=150, node_color=node_colors, edge_color='gray', with_labels=False, alpha=1.0)
    plt.title(title)
    plt.savefig(filename, dpi=300)
    plt.show()
    print(f"Graph gespeichert als {filename}")

# Graph vor Community Detection
visualize_graph(G, "Graph vor Community Detection", "original_graph.png")

# ------ Community Detection durchführen ------ #

# Konvertieren zu ungerichtetem Graphen 
G_undirected = G.to_undirected()

# Louvain-Algorithmus
print("-----")
print("1. Louvain-Algorithmus")
louvain_partition = community_louvain.best_partition(G_undirected) #Aufruf louvain Algorithmus nach best_partition Methode
louvain_communities = {}
for node, community_id in louvain_partition.items():
    louvain_communities.setdefault(community_id, []).append(node)

num_louvain_communities = len(louvain_communities)
print(f"Anzahl der gefundenen Communities: {num_louvain_communities}")
for i, (comm_id, members) in enumerate(louvain_communities.items()):
    if i < num_louvain_communities:
        print(f"Community {comm_id}: {members[:10]} ... ({len(members)} Mitglieder)")
print("\n")

# Girvan-Newman-Algorithmus Abbruchkriterium mit Größenverhältnis der Communities
print("-----")
print("2. Girvan-Newman-Algorithmus")

# festlegen einer Mindestanzahl an Knoten für die kleinste Community
min_community_size_ratio = 0.05  

total_nodes = G_undirected.number_of_nodes()
cm = nx_comm.girvan_newman(G_undirected)

best_girvan_newman_communities = [list(G_undirected.nodes())] 

for communities in cm:
    communities_list = [list(c) for c in communities]
    smallest_community_size = min(len(c) for c in communities_list)
    
    if smallest_community_size / total_nodes < min_community_size_ratio:
        print(f"Kleinste Community zu klein ({smallest_community_size} Mitglieder, weniger als {min_community_size_ratio * 100}% der Gesamtnodes)")
        continue  # Versuche die nächste Aufteilung

    best_girvan_newman_communities = communities_list

num_gn_communities = len(best_girvan_newman_communities)
print(f"Anzahl der gefundenen Communities: {num_gn_communities}")

for i, community in enumerate(best_girvan_newman_communities):
    print(f"Community {i}: {community[:10]} ... ({len(community)} Mitglieder)")
print("\n")

# Walktrap-Algorithmus
print("-----")
print("3. Walktrap-Algorithmus")
walktrap_result = algorithms.walktrap(G_undirected)
walktrap_communities = walktrap_result.communities
num_walktrap_communities = len(walktrap_communities)
print(f"Anzahl der gefundenen Communities: {num_walktrap_communities}")

for i, community in enumerate(walktrap_communities):
    if i < num_walktrap_communities:
        print(f"Community {i}: {community[:10]} ... ({len(community)} Mitglieder)")
print("\n")

# Visualisierung der gefundenen Communities mit Sichtbarmachung der Fehler
def visualize_detected_communities(G, data, communities_dicts):
    pos = nx.spring_layout(G)  
    
    for algorithm_name, communities in communities_dicts.items():
        plt.figure(figsize=(12, 8))
        
        for community_id, members in communities.items():
            # Bestimme die Mehrheit und deren Farbe
            community_labels = [data.loc[data['username'] == member, 'community'].values[0] for member in members if member in data['username'].values]
            majority_label = collections.Counter(community_labels).most_common(1)[0][0] if community_labels else None
            majority_color = community_colors.get(majority_label, 'gray') # gray als default
            
            # Zeichne Kanten und Knoten für diese Community
            nx.draw_networkx_edges(G, pos, arrowsize=3, edge_color='gray')
            for member in members:
                if member in data['username'].values:
                    original_label = data.loc[data['username'] == member, 'community'].values[0]
                    if original_label != majority_label:
                        color = 'black'  # Falsch zugewiesen
                    else:
                        color = majority_color  # Korrekt zugewiesen
                    
                    nx.draw_networkx_nodes(G, pos, nodelist=[member], node_color=color, node_size=150)

        plt.title(f"Visualisierung der gefundenen Communities - {algorithm_name}")
        plt.savefig(f"visualization_{algorithm_name}.png", dpi=300)
        plt.show()

# Dictionary mit den gefundenen Communities von jedem Algorithmus
detected_comm_dicts = {
    "Louvain": louvain_communities,
    "Girvan-Newman": {i: comm for i, comm in enumerate(best_girvan_newman_communities)},
    "Walktrap": {i: comm for i, comm in enumerate(walktrap_communities)}
}

visualize_detected_communities(G, data, detected_comm_dicts)

# ------ Evaluierung ------ #

# Berechne die Anzahl der Mitglieder in den vordefinierten Communities
def evaluate_community_sizes(data):
    community_sizes = data['community'].value_counts()
    print("Anzahl der Mitglieder in den vordefinierten Communities:")
    print(community_sizes)
    return community_sizes

# Vergleiche die gefundenen Communities mit den echten Community-Größen
def compare_communities(communities_dicts, true_community_sizes):
    for algorithm_name, communities in communities_dicts.items():
        print(f"\nVergleich für {algorithm_name}:")
        for community_id, members in communities.items():
            community_size = len(members)
            true_size = true_community_sizes.get(data.loc[data['username'].isin(members), 'community'].values[0], 0)
            print(f"Community {community_id}: Gefunden: {community_size}, Echte Größe: {true_size}")

true_community_sizes = evaluate_community_sizes(data)
compare_communities(detected_comm_dicts, true_community_sizes)
