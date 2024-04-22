
from collections import defaultdict
import numpy as np


def __projection_vectors_vvg(series_a: np.ndarray, series_b: np.ndarray, norm_a: float) -> float:
    """calculate the projection

    Args:
        series_a: time series 
        series_b: time series 
        norm_a: vector norm

    Returns:
        float: result of projection
    """

    return np.dot(series_a, series_b) / norm_a


def __criteria_vvg(series_a: np.ndarray,
                   series_b: np.ndarray,
                   series_c: np.ndarray,
                   time_a: int,
                   time_b: int,
                   time_c: int) -> bool:
    """calculate criteria of visibility graph 

    Args:
        series_a: time_series 
        series_b: time_series 
        series_c: time_series 
        time_a: time of series 
        time_b: time of series 
        time_c: time of series 

    Returns:
        bool: True if the criteria is satisfied, False otherwise
    """
    proj_aa = float(np.linalg.norm(series_a))
    proj_ab = __projection_vectors_vvg(series_a, series_b, proj_aa)
    proj_ac = __projection_vectors_vvg(series_a, series_c, proj_aa)
    time_frac = (time_b - time_c) / (time_b - time_a)
    vg = proj_ab + (proj_aa - proj_ab) * time_frac
    return proj_ac < vg


def build_graph(series: tuple) -> dict:
    """calculate the visibility graph of the two series

    Args:
        series: time_series with n-dimensional. 
        Must be in tuple format ([series_1], [series_2], [series_3], ..., [series_n])

    Returns:
        dict: adjacency list of the visibility graph
    """

    adjacency_list = defaultdict(list)
    all_samples = np.column_stack(series)

    for i, sample_i in enumerate(all_samples):
        for s, sample_s in enumerate(all_samples[i + 1:], start=i + 1):
            if s == i + 1:
                adjacency_list[i].append(s)
                adjacency_list[s].append(i)
            else:
                for t, sample_t in enumerate(all_samples[i + 1:s], start=i + 1):
                    if __criteria_vvg(series_a=sample_i, series_b=sample_s, series_c=sample_t,
                                      time_a=i, time_b=s, time_c=t):
                        adjacency_list[i].append(s)
                        adjacency_list[s].append(i)
                        break
    return adjacency_list
