import networkx as nx
from matplotlib import pyplot as plt

G = nx.DiGraph() #Create the default Graph Object
G.add_node('f') #adds a node manually
G.add_node('g') #adds another node manually
G.add_edge('a', 'b', weight = 0.6) #Will add missing nodes
G.add_edge('a', 'c', weight = 0.2) #and connecting edges
G.add_edge('c', 'd', weight = 0.1) #Weight is one type of edge attribute
G.add_edge('c', 'e', weight = 0.7)
G.add_edge('g', 'c', weight = 0.8)
G.add_edge('f', 'a', weight = 0.5)
i_scores = nx.in_degree_centrality(G)
o_scores = nx.out_degree_centrality(G)
nx.set_node_attributes(G, name='in-degree', values=i_scores)
nx.set_node_attributes(G, name='out-degree', values=o_scores)
print(G.nodes["c"]["in-degree"], G.nodes["c"]["out-degree"])
pos = nx.layout.spring_layout(G, seed=42) #Try to optimize layout
nx.draw(G, pos, with_labels = True, font_color='w')
plt.show()

#3-4 graph
#d_scores = nx.degree_centrality(G)
#nx.set_node_attributes(G, name='degree', values=d_scores)
#print(G.nodes["c"]["degree"])
