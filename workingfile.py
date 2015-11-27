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
from __future__ import print_function, division_operator
from libtp import phyper, RkNN, get_edges


# FONCTION EXEMPLE DE CENTRALITÉ
def fonction_stat(g):
    """
    Retourne une liste de tuple, avec le nom de chaque vertex et sa valeur statistique.
    g: un graphe
    """
    result = []
    # on regarde chaque vertex dans le graph
    for vertex in g.vs:
        # A FAIRE :)
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

# PIPELINE STATISTIQUE
def analyse_degree_graph(g, threshold):
    """
    Renvoie, pour un graph donné, le nombre de sommets d'un degré >= 
    threshold, et parmi ceux-ci, le nombre de graphs essentiels.
    g: un graphe
    threshold: un int
    """
    graph_degree         = function_degree(g)
    nb_vertex            = 0
    nb_essentials_vertex = 0
    for vertex_stat in graph_degree:
        # A FAIRE
    return (nb_vertex, nb_essentials_vertex)
