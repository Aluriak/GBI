"""
This file is dedicated to the practical session.
Functions and routines have to be completed, according to the subject provided by
 the standing guys.

By default, useful functions defined in local library (libtp) are imported,
 as many __future__ features that allows user to code in Python 3 style,
 even if the Pydinosaur is used.
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


# FONCTION EXEMPLE DE CENTRALITE
def fonction_stat(g):
    """
    Retourne une liste de tuple, avec le nom de chaque vertex et sa valeur statistique.
    g: un graphe
    """
    result = []
    # on regarde chaque vertex dans le graph
    for vertex in g.vs:
        pass # TODO
    return result


def vertices_name(graph):
    """Return list of names of vertices present in the given graph"""
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
    """Show the special vertex proportion in the graph.
    A vertex is special if have an 'a' in its name.
    This is done for 'b' too, because its also special."""
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

