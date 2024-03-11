import networkx as nx
from matplotlib import pyplot as plt

clique_graph = nx.Graph()
clique_graph.add_edges_from(
    [
        ("Tom", "Jerry"),("Butch", "Jerry"),("Spike","Jerry"),
        ("Spike","Tom"),("Tom", "Squeek"),("Tom", "Butch"),
        ("Squeek","Butch")
    ]
)

clq = nx.algorithms.number_of_cliques(clique_graph)
tot = nx.algorithms.graph_number_of_cliques(clique_graph)
for m in clq:
    print(m, (clq[m]/tot))
