"""
Definitions of many functions designed for simplify work of students during
 the practical session.

"""
from __future__ import print_function
import scipy.stats as stats


def phyper(pop_size, pop_condition_count,
           subset_size, subset_condition_count):
    """Return the likelihood of get a number of elements with a condition
    in a population subset.

    pop_size: total number of elements in population
    pop_condition_count: total number of elements with condition in population
    subset_size: number of element in subset
    subset_condition_count: number of element with condition in subset

    A loss of precision is expected for big values.

    sources:
        - https://www.biostars.org/p/66729/
        - http://stackoverflow.com/questions/6594840/what-are-equivalents-to-rs-phyper-function-in-python
        - http://stackoverflow.com/questions/32859103/python-scipys-hypergeometric-test-not-equal-to-r-or-sas
    Other interesting links about hypergeometric tests: 404 not found

    """
    return stats.hypergeom.sf(subset_condition_count - 1,  # without -1, results are generally false
                              pop_size, pop_condition_count, subset_size)


def get_edges(graph, vertex):
    """Return tuple of edges of the given graph that are linked to given vertex"""
    try:
        vertex = vertex.index
    except AttributeError:
        pass
    pairs = (
        (vertex, cur_vertex)
        for cur_vertex in range(graph.vcount())
        if graph[vertex, cur_vertex] > 0
    )
    return tuple(graph.es[idx] for idx in graph.get_eids(tuple(pairs)))


def RkNN(graph, k=2):
    """Return a new graph, equivalent of the RkNN of given graph

    graph: an igraph Graph instance, non directed
    k: an integer > 0, the RNN order
    return: a new directed graph

    """
    # Create the RNN graph from the given one, with same vertices
    rnn = ig.Graph(directed=True)
    for vertex in graph.vs:
        rnn.add_vertex(**vertex.attributes())
    for i, vertex in enumerate(graph.vs):
        assert vertex.index == rnn.vs[i].index
    # Add directed edges that represent the RNN topology
    for vertex in graph.vs:
        edges = get_edges(graph, vertex)
        weights = tuple(e.attributes()['weight'] for e in edges)
        # sort edges, according to their weight
        sorted_edges = sorted(edges, key=lambda e: e.attributes()['weight'])
        # add the directed edges, from vertex to neighbor, for the k first edges
        for edge in itertools.islice(sorted_edges, k):
            idvertex = vertex.index
            source, target = edge.source, edge.target  # source and target indexes
            assert idvertex in (source, target)  # vertex is source or target
            target = target if idvertex == source else source
            assert idvertex != target
            weight = edge.attributes()['weight']
            rnn.add_edge(idvertex, target, weight=weight)
    return rnn


