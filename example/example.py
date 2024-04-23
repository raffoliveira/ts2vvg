import pickle
import matplotlib.pyplot as plt

import networkx as nx
from ts2vvg.graph import build_graph


#time_series_1 = [0.5, 1.3, 8.0, 1.8, 2.7, 1.2, 3.6, 2.2, 7.1, 5.3]
#time_series_2 = [0.6, 0.2, 12.1, 1.3, 2.4, 2.1, 1.6, 2.5, 3.2, 6.6]

time_series_1 = [1.0, 1.0, 1.0, 1.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0]
time_series_2 = [1.0, 1.0, 1.0, 1.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0]

print(f"time_series_1 = {time_series_1}")
print(f"time_series_2 = {time_series_2}")

adjlist_ = build_graph(series=(time_series_1, time_series_2))
print(adjlist_)
G = nx.DiGraph(adjlist_)

# saving the graph object
nx.write_gml(G, "graph_simple.gml")

pos = {}
for i in range(len(time_series_1)):
    pos[i] = (i,0)

# plotting the graph
nx.draw_networkx(G, pos=pos,connectionstyle="arc3,rad=0.5")
plt.savefig("graph.png", dpi=300)

print(list(G.degree()))