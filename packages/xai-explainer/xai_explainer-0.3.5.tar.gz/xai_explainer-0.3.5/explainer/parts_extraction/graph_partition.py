from typing import Any, Callable, Tuple

import networkx as nx
import numpy as np
from sklearn.cluster import SpectralClustering

__all__ = [
    "list_partition_methods",
    "get_partition_method",
]

REGISTERED_PARTITION_METHODS = {}


class Partition_Wrapper:
    def __init__(self, handle: Callable, num_parts: int = 10) -> None:
        self.handle: Callable = handle
        self.num_parts: int = (
            num_parts  # TODO: choose num_parts based on the input graph @Daniel
        )

    def __call__(self, adj_matrix: np.ndarray, **kwargs) -> Any:
        return self.handle(adj_matrix, self.num_parts, **kwargs)


def register_partition_method(handle: Callable):
    REGISTERED_PARTITION_METHODS[handle.__name__] = Partition_Wrapper(handle)


def list_partition_methods():
    return list(REGISTERED_PARTITION_METHODS.keys())


def get_partition_method(name: str) -> Callable:
    return REGISTERED_PARTITION_METHODS[name]


@register_partition_method
def identity(adj_matrix: np.ndarray, num_parts: int, **kwargs) -> Tuple[int, list[int]]:
    return adj_matrix.shape[0], range(
        adj_matrix.shape[0]
    )  # if there are fewer vertices than clusters, just give each vertex its own cluster


@register_partition_method
def normalized_graph_cut(
    adj_matrix: np.ndarray, num_parts: int, **kwargs
) -> Tuple[int, list[int]]:
    if adj_matrix.shape[0] <= num_parts:
        return adj_matrix.shape[0], range(
            adj_matrix.shape[0]
        )  # if there are fewer vertices than clusters, just give each vertex its own cluster

    clustering = SpectralClustering(
        n_clusters=num_parts, affinity="precomputed", **kwargs
    ).fit(adj_matrix)
    return num_parts, clustering.labels_


@register_partition_method
def greedy_modularity(
    adj_matrix: np.ndarray, num_parts: int, **kwargs
) -> Tuple[int, list[int]]:
    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    res = nx.community.greedy_modularity_communities(graph, **kwargs)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering


@register_partition_method
def girvan_newman(
    adj_matrix: np.ndarray, num_parts: int, **kwargs
) -> Tuple[int, list[int]]:
    if adj_matrix.shape[0] <= num_parts:
        return adj_matrix.shape[0], range(
            adj_matrix.shape[0]
        )  # if there are fewer vertices than clusters, just give each vertex its own cluster

    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    comp = nx.community.girvan_newman(graph, **kwargs)

    res = next(comp)
    while len(res) < num_parts:
        res = next(comp)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering


@register_partition_method
def louvain(adj_matrix: np.ndarray, num_parts: int, **kwargs) -> Tuple[int, list[int]]:
    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    res = nx.community.louvain_communities(graph, **kwargs)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering
