
from collections import defaultdict
import numpy as np


def __projection_vectors_vvg(Xa: np.ndarray, Xb: np.ndarray, norm_Xa: float) -> float:
    """calculate the projection

    Args:
        Xa: time series 
        Xb: time series 
        norm_Xa: vector norm

    Returns:
        float: result of projection
    """

    return np.dot(Xa, Xb) / norm_Xa


def __criteria_vvg(Xa: np.ndarray,
                   Xb: np.ndarray,
                   Xc: np.ndarray,
                   ta: int,
                   tb: int,
                   tc: int) -> bool:
    """calculate criteria of visibility graph 

    Args:
        Xa: time_series 
        Xb: time_series 
        Xc: time_series 
        ta: time of series 
        tb: time of series 
        tc: time of series 

    Returns:
        bool: True if the criteria is satisfied, False otherwise
    """
    Xaa = float(np.linalg.norm(Xa))
    Xab = __projection_vectors_vvg(Xa, Xb, Xaa)
    Xac = __projection_vectors_vvg(Xa, Xc, Xaa)
    time_frac = (tb - tc) / (tb - ta)
    vis_criterion = Xab + (Xaa - Xab) * time_frac
    #print(f'{ta=},{tb=},{tc=}:  {Xac=} < {vis_criterion=} == {Xac < vis_criterion}')
    return Xac < vis_criterion


def build_graph(series: tuple, time_direction: False) -> dict:
    """calculate the visibility graph of the two series

    Args:
        series: time_series with n-dimensional. 
        Must be in tuple format ([series_1], [series_2], [series_3], ..., [series_n])
        time_direction: True if only connections from ta to tb are allowed, with ta < tb

    Returns:
        dict: adjacency list of the visibility graph
    """

    adjacency_list = defaultdict(list)
    X = np.column_stack(series)

    #print(f'Vector norms = {[float(np.linalg.norm(Xa)) for ta, Xa in enumerate(X)]}')

    for ta, Xa in enumerate(X):
        for tb, Xb in enumerate(X[ta + 1:], start=ta + 1):
            if tb == ta + 1:
                adjacency_list[ta].append(tb)
                if(not time_direction):
                    adjacency_list[tb].append(ta)
            else:
                criteria_fullfiled = True # No vector Xc should "block" the visibility between Xa and Xb
                for tc, Xc in enumerate(X[ta + 1:tb], start=ta + 1):
                    #print(f'{ta=} {tb=} {tc=}  {Xa=} {Xb=} {Xc=}')
                    if __criteria_vvg(Xa=Xa, Xb=Xb, Xc=Xc, ta=ta, tb=tb, tc=tc) == False:
                        criteria_fullfiled = False
                if(criteria_fullfiled):
                    adjacency_list[ta].append(tb)
                    if(not time_direction):
                        adjacency_list[tb].append(ta)
    return adjacency_list
