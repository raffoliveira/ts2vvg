from collections import defaultdict
from typing import Tuple
import pandas as pd
import numpy as np
import pickle

import networkx as nx
from scipy.io import loadmat

from helpers.generate_graph_dataset import SyntheticDataset


def segmentation_signals(path: str, size_beat_before: int, size_beat_after: int) -> Tuple[defaultdict, defaultdict]:
    """
    Segment the ECG signal into beats with a fixed number of points.

    Args:
        path: path of the file
        size_beat_before: number of points before peak
        size_beat_after: number of points after peak

    Returns:
        Tuple of dictionary with all beats separated by class.
    """

    dict_signals_v1 = defaultdict(list)  # dict to load beats
    dict_signals_ii = defaultdict(list)  # dict to load beats

    struct = loadmat(path)  # loading the original file
    data = struct["individual"][0][0]  # loading info of the signal

    beat_peaks = data["anno_anns"]  # reading R-peak
    beat_types = data["anno_type"]  # reading type of beat

    ecg_v1 = data["signal_r"][:, 1]  # reading lead V1
    ecg_ii = data["signal_r"][:, 0]  # reading lead II

    for peak, beat_type in zip(beat_peaks, beat_types):

        beat_samples_v1 = []  # list to save samples of beat V1
        beat_samples_ii = []  # list to save samples of beat II

        # half_beat = int(size_beat/2) #half of size beat

        # if the position is before the begining or
        # if the position is after the ending
        # do nothing
        if (peak - size_beat_before) < 0 or (peak + size_beat_after) > len(ecg_ii):
            continue

        # if type of beat is different than this list, do nothing
        if beat_type not in "NLRejAaJSVEFP/fUQ":
            continue

        # taking the samples of beat window
        beat_samples_ii = ecg_ii[int(peak - size_beat_before): int(peak + size_beat_after)]
        beat_samples_v1 = ecg_v1[int(peak - size_beat_before): int(peak + size_beat_after)]

        # taking the type of beat and saving in dict
        if beat_type in "NLRej":
            dict_signals_v1["N"].append(beat_samples_v1)
            dict_signals_ii["N"].append(beat_samples_ii)
        elif beat_type in "AaJS":
            dict_signals_v1["S"].append(beat_samples_v1)
            dict_signals_ii["S"].append(beat_samples_ii)
        elif beat_type in "VE":
            dict_signals_v1["V"].append(beat_samples_v1)
            dict_signals_ii["V"].append(beat_samples_ii)

    return dict_signals_v1, dict_signals_ii


def subsampling_beats(beat_v1: defaultdict, beat_ii: defaultdict) -> Tuple[defaultdict, defaultdict]:
    """
    Sampling the beats on N and V class. A sampling rate of 10% was adopted, selectively choosing the final
    heartbeat in every sequence of ten.

    Args:
        beat_v1: A dictionary with all beats
        beat_ii: A dictionary with all beats

    Returns:
        Tuple of dictionary
    """

    select_classes = ["N", "V"]

    for _class in select_classes:
        select_beats_v1 = []
        select_beats_ii = []

        for index, beat in enumerate(beat_v1[_class], 1):
            if (index % 10) == 0:
                select_beats_v1.append(beat)

        for index, beat in enumerate(beat_ii[_class], 1):
            if (index % 10) == 0:
                select_beats_ii.append(beat)

        beat_v1[_class] = select_beats_v1
        beat_ii[_class] = select_beats_ii

    return beat_v1, beat_ii


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


def convert_beats_into_graphs(beat_v1: dict, beat_ii: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert beats into graphs.

    Args:
        beat_v1: A dictionary with all beats
        beat_ii: A dictionary with all beats

    Returns:
        A tuple containing two DataFrames:
            1. edges: DataFrame representing edges in the graphs with columns:
                <> 'graph_id': the ID of the graph, 
                <> 'src': the source node of an edge of the given graph, and
                <> 'dst': the destination node of an edge of the given graph.
            2. properties: DataFrame representing properties of the graphs with columns:
                <> 'graph_id': the ID of the graph, 
                <> 'label': the label of the graph, and 
                <> 'num_nodes': the number of nodes in the graph, 
    """
    graph_id = []
    graph_src = []
    graph_dst = []
    graph_nodes = []
    graph_label = []
    classes = ["N", "S", "V"]
    graph_it = 0

    for (class_, beats_V1), (_, beats_II) in zip(beat_v1.items(), beat_ii.items()):
        for beat_V1, beat_II in zip(beats_V1, beats_II):
            label = classes.index(class_)
            adjlist_ = vector_visibility_graph_vvg(series_a=beat_V1, series_b=beat_II)
            G = nx.DiGraph(adjlist_)
            source_nodes_ids = [i[0] for i in nx.to_edgelist(G)]
            destination_nodes_ids = [i[1] for i in nx.to_edgelist(G)]
            num_nodes = nx.number_of_nodes(G)

            graph_id.extend([graph_it] * len(nx.to_edgelist(G)))
            graph_src.extend(source_nodes_ids)
            graph_dst.extend(destination_nodes_ids)
            graph_nodes.extend([num_nodes] * len(nx.to_edgelist(G)))
            graph_label.extend([label] * len(nx.to_edgelist(G)))
            del G
            graph_it += 1

    edges = pd.DataFrame({"graph_id": graph_id, "src": graph_src, "dst": graph_dst})
    properties = pd.DataFrame({"graph_id": graph_id, "label": graph_label, "num_nodes": graph_nodes})
    properties.drop_duplicates(inplace=True)

    edges.to_csv("./files/edges_graph.csv")
    properties.to_csv("./files/properties_graph.csv")

    del graph_id, graph_src, graph_dst, graph_nodes, graph_label

    return edges, properties


if __name__ == "__main__":

    PATH = "../../Data/MIT_BIH/222.mat"

    print("Segmenting...")
    beats_v1, beats_ii = segmentation_signals(path=PATH, size_beat_before=100, size_beat_after=180)

    print("Subsampling...")
    beats_v1, beats_ii = subsampling_beats(beat_v1=beats_v1, beat_ii=beats_ii)

    print("converting into graphs...")
    edges, properties = convert_beats_into_graphs(beat_v1=beats_v1, beat_ii=beats_ii)

    print("creating graph dataset...")
    dataset = SyntheticDataset(attr_edges=edges, attr_properties=properties)

    with open("dataset_GCN.pkl", "wb") as file:
        pickle.dump(dataset, file)
