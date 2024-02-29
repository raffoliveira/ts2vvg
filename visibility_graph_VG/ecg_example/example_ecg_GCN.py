from collections import defaultdict
from typing import Tuple
import pandas as pd

import igraph as ig
from scipy.io import loadmat
from ts2vg import NaturalVG

from helpers.generate_graph_dataset import SyntheticDataset


def segmentation_signals(path: str, size_beat_before: int, size_beat_after: int) -> defaultdict:
    """
    Segment the ECG signal into beats with a fixed number of points.

    Args:
        path: path of the file
        size_beat_before: number of points before peak
        size_beat_after: number of points after peak

    Returns:
        Dictionary with all beats separated by class.
    """

    dict_signals_II = defaultdict(list)  # dict to load beats II

    struct = loadmat(path)  # loading the original file
    data = struct["individual"][0][0]  # loading info of the signal
    ecg_II = data["signal_r"][:, 0]  # reading lead II

    beat_peaks = data["anno_anns"]  # reading R-peak
    beat_types = data["anno_type"]  # reading type of beat

    for peak, beat_type in zip(beat_peaks, beat_types):

        beat_samples_II = []  # list to save samples of beat II

        if (peak - size_beat_before) < 0 or (peak + size_beat_after) > len(ecg_II):
            continue

        # if type of beat is different than this list, do nothing
        if beat_type not in "NLRejAaJSVEFP/fUQ":
            continue

        # taking the samples of beat window
        beat_samples_II = ecg_II[int(peak - size_beat_before): int(peak + size_beat_after)]

        # taking the type of beat and saving in dict
        if beat_type in "NLRej":
            dict_signals_II["N"].append(beat_samples_II)
        elif beat_type in "AaJS":
            dict_signals_II["S"].append(beat_samples_II)
        elif beat_type in "VE":
            dict_signals_II["V"].append(beat_samples_II)

    return dict_signals_II


def subsampling_beats(beats: dict) -> dict:
    """
    Sampling the beats on N and V class. A sampling rate of 10% was adopted, selectively choosing the final
    heartbeat in every sequence of ten.

    Args:
        beats: A dictionary with all beats

    Returns:
        Sampled dictionary 
    """
    select_classes = ["N", "V"]

    for _class in select_classes:
        select_beats = []
        for index, beat in enumerate(beats[_class], 1):
            if (index % 10) == 0:
                select_beats.append(beat)

        beats[_class] = select_beats

    return beats


def convert_beats_into_graphs(beats: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert beats into graphs.

    Args:
        beats: A dictionary containing beats separated by class.

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

    for class_, beat in beats.items():
        for beat_ in beat:
            label = classes.index(class_)
            g = NaturalVG(directed=None).build(beat_)
            G = g.as_igraph()
            source_nodes_ids = [i[0] for i in ig.Graph.get_edgelist(G)]
            destination_nodes_ids = [i[1] for i in ig.Graph.get_edgelist(G)]
            num_nodes = G.vcount()
            graph_id.extend([graph_it] * len(ig.Graph.get_edgelist(G)))
            graph_src.extend(source_nodes_ids)
            graph_dst.extend(destination_nodes_ids)
            graph_nodes.extend([num_nodes] * len(ig.Graph.get_edgelist(G)))
            graph_label.extend([label] * len(ig.Graph.get_edgelist(G)))
            graph_it += 1
            del G

    edges = pd.DataFrame({"graph_id": graph_id, "src": graph_src, "dst": graph_dst})
    properties = pd.DataFrame({"graph_id": graph_id, "label": graph_label, "num_nodes": graph_nodes})
    properties.drop_duplicates(inplace=True)

    edges.to_csv("./files/edges_graph.csv")
    properties.to_csv("./files/properties_graph.csv")

    del graph_id, graph_src, graph_dst, graph_nodes, graph_label

    return edges, properties


if __name__ == "__main__":

    PATH = "../../Data/MIT_BIH/119.mat"

    print("Segmenting...")
    beats = segmentation_signals(path=PATH, size_beat_before=100, size_beat_after=180)

    print("Subsampling...")
    beats = subsampling_beats(beats=beats)

    print("converting into graphs...")
    edges, properties = convert_beats_into_graphs(beats=beats)

    print("creating graph dataset...")
    dataset = SyntheticDataset(attr_edges=edges, attr_properties=properties)
