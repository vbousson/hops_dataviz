import networkx as nx
import matplotlib.pyplot as plt

G = nx.dodecahedral_graph()
nx.draw(G)
plt.draw()

plt.show()