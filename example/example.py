from ts2vvg.graph import build_graph
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# reading the time series. The time series passed can be any n-dimensional.
# Two time series are used here like [5.5,4.3,1.0,7.8,2.7,1.2,3.6,2.2,7.1]

with open("time_series_1.pkl", "rb") as file:
    time_series_1 = pickle.load(file)
with open("time_series_2.pkl", "rb") as file:
    time_series_2 = pickle.load(file)

print(f'{time_series_1}=')
print(f'{time_series_2}=')

adjlist_ = build_graph(series_a=time_series_1, series_b=time_series_2)
G = nx.DiGraph(adjlist_)

# saving the graph object
nx.write_gml(G, "graph_simple.gml")

# plotting the graph
nx.draw_networkx(G)
plt.savefig("graph.png", dpi=300)