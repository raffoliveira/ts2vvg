import pickle
import matplotlib.pyplot as plt

import networkx as nx
from ts2vvg.graph import build_graph

# reading the time series. The time series passed can be any n-dimensional.
# Two time series are used here like [5.5,4.3,1.0,7.8,2.7,1.2,3.6,2.2,7.1]

with open("time_series_example_1.pkl", "rb") as file:
    time_series_1 = pickle.load(file)
with open("time_series_example_2.pkl", "rb") as file:
    time_series_2 = pickle.load(file)

print(f"time_series_1 = {time_series_1}")
print(f"time_series_2 = {time_series_2}")

adjlist_ = build_graph(series=(time_series_1, time_series_2))
G = nx.DiGraph(adjlist_)

# saving the graph object
nx.write_gml(G, "graph_simple.gml")

# plotting the graph
nx.draw_networkx(G)
plt.savefig("graph.png", dpi=300)
