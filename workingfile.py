"""
This file is dedicated to the practical session.
Functions and routines have to be completed, according to the subject provided by
 the standing guys.

By default, useful functions defined in local library (libtp) are imported,
 as many __future__ features that allows user to code in Python 3 style,
 even if dinopython is used.
 For all functions of libtp, don't hesitate to use the help() function for
 get the documentation about it.
  example: help(plot_stats)

Moreover, example functions are defined in the examples.py file.
 Maybe one of them will help you.

If the subject or the standing guys are not clear enough, please take a look
 to the following webpages:
    - http://python-igraph.readthedocs.org/en/latest/tutorial.html
    - http://stackoverflow.com/questions/tagged/igraph
    - https://en.wikipedia.org/wiki/Centrality

"""
from __future__ import print_function
import igraph as ig
from libtp import phyper, plot_stats


def five_vertices():
    """
    Reproduce the graph in the subject.
    """
    g = ig.Graph()
    # TODO
    ig.plot(g)


def centrality_degree(g):
    """
    Return a list of 2-tuple (vertex, degree), for each vertex of given graph.
    g: graph
    """
    result = []
    for vertex in g.vs:
        result.append((vertex, ?))  # TODO
    return result


def analyse_degree_graph(g, threshold):
    """
    Return, for a graph, the number of vertex with a degree >= threshold, and 
    the number of essentials vertex in those ones.
    g: graph
    threshold: int
    """
    graph_degree         = function_degree(g)
    nb_vertex            = 0
    nb_essentials_vertex = 0
    for vertex_stat in graph_degree:
        pass # TODO
    return (nb_vertex, nb_essentials_vertex)


if __name__ == '__main__':
    five_vertices()
    #TODO: create a graph here
    centrality_degree()
