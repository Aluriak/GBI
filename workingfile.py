"""
This file is dedicated to the practical session.
Functions and routines have to be completed, according to the subject provided by
 the standing guys.

By default, useful functions defined in local library (libtp) are imported,
 as many __future__ features that allows user to code in Python 3 style,
 even if dinopython is used.
 For all functions of libtp, don't hesitate to use the help() function for
 get the documentation about it.
  example: help(RkNN)
Moreover, example functions are defined. Maybe one of them will help you.

If the subject or the standing guys are not clear enough, please take a look
 to the following webpages, instead of throw rocks on them:
    - http://python-igraph.readthedocs.org/en/latest/tutorial.html
    - http://stackoverflow.com/questions/tagged/igraph
    - https://en.wikipedia.org/wiki/Centrality

"""
from __future__ import print_function
import igraph as ig
from libtp import phyper, RkNN, get_edges, plot_stats


# Centrality exemple function
def fonction_stat(g):
    """
    Return a liste of tuple, with each vertex name and its stat value.
    g: graph
    """
    result = []
    # for each vertex in graph
    for vertex in g.vs:
        pass # TODO
    return result


def vertices_name(graph):
    """
    Return list of names of vertices present in the given graph
    g: graph
    """
    name_list = []
    for vertex_name in graph.vs['name']:
        name_list.append(vertex_name)
    return name_list
    # other solution:
    name_list = []
    for vertex in graph.vs:
        vertex_attributes = vertex.attributes()
        name_list.append(vertex_attributes['name'])
    return name_list
    # other solution:
    return [vertex_name for vertex_name in graph.vs['name']]


def plot_dumb_stats(graph):
    """
    Show the special vertex proportion in the graph.
    A vertex is special if have an 'a' in its name.
    This is done for 'b' too, because its also special.
    """
    prot_count = len(graph.vs['name'])
    special_prot_count = []
    special_letters = ('a', 'b')
    for special_letter in special_letters:
        special_prot_count.append(0)
        for vertex_name in graph.vs['name']:
            try:
                if special_letter in vertex_name.lower():
                    special_prot_count[-1] += 1
            except (AttributeError, TypeError):
                pass
    plot_stats([prot_count] * 2, special_prot_count, special_letters)


# PIPELINE STATISTIQUE
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
