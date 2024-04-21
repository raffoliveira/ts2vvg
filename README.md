# ts2vvg

![GitHub](https://img.shields.io/github/license/raffoliveira/ts2vvg)
![GitHub last commit](https://img.shields.io/github/last-commit/raffoliveira/ts2vvg)
![GitHub stars](https://img.shields.io/github/stars/raffoliveira/ts2vvg?style=social)
![GitHub downloads](https://img.shields.io/github/downloads/raffoliveira/ts2vvg/total)

ts2vvg: a Python package with an implementation of the Vector Visibility Graph (VVG) [(REN and JIN, 2019)](https://link.springer.com/article/10.1007/s11071-019-05147-7), to convert multivariate time series into graphs. 

Author: Rafael Oliveira. 

Last updated: 2024.02.29.

If you use this package, please cite the following paper:

`REF Software impacts`

# Summary

- [Vector Visibility Graph](#vector-visibility-graph)
- [Installation](#installation)
- [Running example](#running-example)
- [Usage in real projects](#usage-in-real-projects)

# Vector Visibility Graph

  
The VVG is based on the [Visibiility Graph (VG)](https://www.pnas.org/doi/abs/10.1073/pnas.0709247105), available in the well-known package [ts2vg](https://pypi.org/project/ts2vg/). We propose here an implementation for VVG, using numpy and networkX libraries. Find below an illustration of how the algorithm works, from an input multivariate time series to the resulting directed network.

![vvg](./docs/vvg.png)

Source: Adapted from (REN and JIN, 2019).

# Installation

To install the ts2vvg package in a Python environment:

```shell
pip install git+https://github.com/raffoliveira/ts2vvg@main
```

## Requirements

The required packages are listed below: 

+ matplotlib==3.8.3
+ networkx==3.2.1
+ numpy==1.26.4

# Running example

We provide a simple example to demonstrate the conversion of a multivariate time series into a graph. The data are available in two pickle files: `time_series_1.pkl` and `time_series_2.pkl`, whose values are [5.5, 4.3, 1.0, 7.8, 2.7, 1.2, 3.6, 2.2, 7.1, 5.3] and [0.6, 3.6, 0.1, 4.3, 6.4, 2.1, 1.6, 4.5, 8.2, 6.6], respectively. The result is the following graph:

![graph](./example/graph.png)

To run the the example:

```
python example_simple.py
```

# Usage in real projects:

- **Leveraging Visibility Graphs for Enhanced Arrhythmia Classification**. [code](https://github.com/raffoliveira/VG_for_arrhythmia_classification_with_GCN).


# References

`ARXIV do artigo GNN+VVG+ECG`

Ren, W., Jin, N. Vector visibility graph from multivariate time series: a new method for characterizing nonlinear dynamic behavior in two-phase flow. Nonlinear Dyn 97, 2547–2556 (2019). https://doi.org/10.1007/s11071-019-05147-7