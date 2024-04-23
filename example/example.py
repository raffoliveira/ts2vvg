import pickle
import matplotlib.pyplot as plt

import networkx as nx
from ts2vvg.graph import build_graph


time_series_1 = [8.0, 2.0, 13.0, 11.0, 7.0]
time_series_2 = [5.0, 1.5, 13.0, 9.5, 6.0]

print(f"time_series_1 = {time_series_1}")
print(f"time_series_2 = {time_series_2}")

adjlist_ = build_graph(series=(time_series_1, time_series_2), time_direction=False)
G = nx.DiGraph(adjlist_)

mapping = {}
pos = {}
for i in range(len(time_series_1)):
    pos[i+1] = (i,0)
    mapping[i] = i+1

# mapping: to rename edges from 0,1,2... to 1,2,3...
G = nx.relabel_nodes(G, mapping)

# saving the graph object
nx.write_gml(G, "graph_simple.gml")

# plotting the graph
plt.figure(3,figsize=(9,2.5)) 
# pos: to guarantee the nodes are plotted sequentially side by side
# connectionstyle: to produce rounded arcs between nodes
nx.draw_networkx(G, pos=pos, connectionstyle="arc3,rad=0.5", node_color='orange')
plt.savefig("graph.png", dpi=300)