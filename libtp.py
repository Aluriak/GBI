"""
Definitions of many functions designed for simplify work of students during
 the practical session.

"""
from __future__ import print_function
import itertools
import igraph as ig
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

from load_graph import *


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


def plot_stats(prot_number, essential_prot_number, stat_value,
               stat_name='degree', all_color='grey', essential_color='red'):
    """Plot given data with bars and colors.

    prot_number: iterable of protein counts (its the first bar).
    essential_prot_number: iterable of essential protein counts (second bar).
    stat_value: iterable of values (example: minimal degree), used as labels for
        each bar couple.
    stat_name: given name for the X axis couples of bars.
    all_color: given color for the bar showing the number
        of protein (essential or not).
    essential_color: given color for the bar showing the number
        of essential protein.

    Obviously, prot_number, essential_prot_number and stat_value must be equals
        in length, as they just gives different data of the same experiment.

    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ## the data
    assert len(prot_number) == len(stat_value)
    assert len(prot_number) == len(essential_prot_number)
    N = len(stat_value)

    ## necessary variables
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35        # the width of the bars

    ## the bars
    rects1 = ax.bar(ind, prot_number, width, color=all_color)

    rects2 = ax.bar(ind+width, essential_prot_number, width,
                    color=essential_color)

    # axes and labels
    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylim(0, max(prot_number) + int(max(prot_number)*0.1) + 1)
    ax.set_ylabel('Number of (essential) proteins')
    ax.set_title('Essential protein proportion function to the minimal ' + stat_name + ' value')
    xTickMarks = [stat_name + ' >= ' + str(i) for i in stat_value]
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)

    ## add a legend
    ax.legend( (rects1[0], rects2[0]), ('All proteins', 'Essential proteins'))

    plt.show()


def plot_phyper(pvalues, thresholds, stat_name='degree'):
    """Plot a simple graphics of pvalues function to thresholds"""
    ## initialize the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    line = ax.plot(thresholds, pvalues, color='red', marker='+')

    ## the top axes
    ax.set_ylim(0., 1.)
    ax.set_ylabel('p-value')
    ax.set_xlabel(stat_name + ' thresholds')
    ax.set_title('probability of the essential proteins distribution '
                 'function to ' + stat_name + ' minimal thresholds')

    assert len(pvalues) == len(thresholds)
    plt.show()


def read_essentials(path="./essentials.txt"):
    """his function loads all yeast_id of essential genes.

    The file was taken from stanford :
    http://www-sequence.stanford.edu/group/yeast_deletion_project/Essential_ORFs.txt

    ..Note: Return of 1122/1156 references in file.

    :param arg1: Path of txt file.
    :type arg1: <str>
    :return: set of yeast_id of essential genes
    :rtype: <set>

    """

    with open("essentials.txt", 'r') as file:
        essentials_prots = {line.strip() for line in file}

    print("{} essential genes.".format(len(essentials_prots)))

    return essentials_prots


def compute_biological_data():
    """Parse csv file from BIOGRID & Cytoscape; Then make a graph & return it.

    """

    # Load a graph
    return ig.Graph.Read_GML('biological_data_118.gml')


