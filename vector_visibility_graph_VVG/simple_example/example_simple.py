import pickle
from collections import defaultdict
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def projection_vectors_vvg(series_a: np.ndarray, series_b: np.ndarray, norm_a: float) -> float:
    """calculate the projection from series_a to series_b

    Args:
        series_a: time series 1
        series_b: time series 2
        norm_a: vector norm

    Returns:
        float: result of projection between two time series
    """

    return np.dot(series_a, series_b) / norm_a


def criteria_vvg(series_a: np.ndarray,
                 series_b: np.ndarray,
                 series_c: np.ndarray,
                 time_a: int,
                 time_b: int,
                 time_c: int,
                 norm_a: float) -> bool:
    """calculate criteria of visibility graph of the three series

    Args:
        series_a: time_series 1
        series_b: time_series 2
        series_c: time_series 3
        time_a: time of series 1
        time_b: time of series 2
        time_c: time of series 3
        norm_a: vector norm 

    Returns:
        bool: True if the visibility graph of the three series is possible, False otherwise
    """
    proj_aa = norm_a
    proj_ab = projection_vectors_vvg(series_a, series_b, norm_a)
    proj_ac = projection_vectors_vvg(series_a, series_c, norm_a)
    time_frac = (time_b - time_c) / (time_b - time_a)
    vg = proj_ab + (proj_aa - proj_ab) * time_frac
    return proj_ac < vg


def vector_visibility_graph_vvg(series_a: np.ndarray, series_b: np.ndarray) -> dict:
    """calculate the visibility graph of the two series

    Args:
        series_a: time_series 1
        series_b: time_series 2

    Returns:
        dict: adjacency list of the visibility graph
    """

    norm_a = float(np.linalg.norm(series_a))
    adjacency_list = defaultdict(list)
    all_samples = np.column_stack((series_a, series_b))

    for i, sample_i in enumerate(all_samples):
        for s, sample_s in enumerate(all_samples[i + 1:], start=i + 1):
            if s == i + 1:
                adjacency_list[i].append(s)
                adjacency_list[s].append(i)
            else:
                for t, sample_t in enumerate(all_samples[i + 1:s], start=i + 1):
                    if criteria_vvg(sample_i, sample_s, sample_t, i, s, t, norm_a):
                        adjacency_list[i].append(s)
                        adjacency_list[s].append(i)
                        break
    return adjacency_list


if __name__ == "__main__":

    # reading the time series. The time series passed can be any n-dimensional.
    # Two time series are used here like [5.5,4.3,1.0,7.8,2.7,1.2,3.6,2.2,7.1]

    with open("time_series_1.pkl", "rb") as file:
        time_series_1 = pickle.load(file)
    with open("time_series_2.pkl", "rb") as file:
        time_series_2 = pickle.load(file)

    adjlist_ = vector_visibility_graph_vvg(series_a=time_series_1, series_b=time_series_2)
    G = nx.DiGraph(adjlist_)

    # saving the graph object
    nx.write_gml(G, "graph_simple.gml")

    # plotting the graph
    nx.draw_networkx(G)
    plt.savefig("graph.png", dpi=300)
