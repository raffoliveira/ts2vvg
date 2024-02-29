# For more information about ts2vg package, check its documentation on https://pypi.org/project/ts2vg/.

import pickle
import igraph as ig
from ts2vg import NaturalVG, HorizontalVG

if __name__ == "__main__":

    # reading the time series. The time series passed can be any one-dimensional,
    # like [1.0,2.5,3.9,5.7] or numpy array format
    with open("time_series.pkl", "rb") as file:
        time_series = pickle.load(file)

    # generating different graphs from ts2vg package
    g = NaturalVG(directed=None).build(time_series)
    gh = HorizontalVG(directed=None).build(time_series)
    ghw = HorizontalVG(directed="left_to_right", weighted="h_distance").build(time_series)

    # converting the generated graph into graph objects using igraph package
    G = g.as_igraph()
    GH = gh.as_igraph()
    GHW = ghw.as_igraph()

    # saving the graph object
    G.write("graph_simple.gml", format="gml")

    # plotting the graph
    ig.plot(G, "graph.pdf")
    ig.plot(GH, "graphGH.pdf")
    ig.plot(GHW, "graphGHW.pdf")
