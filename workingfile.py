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
from libtp import phyper, plot_phyper, plot_stats, compute_biological_data


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
    return tuple(result)


def pipeline_degree(g, essential_proteins):
    levels = (1, 2)  # TODO
    protein_count_total     = []  # number of proteins with a degree >= level
    protein_count_essential = []  # same for essential proteins
    degrees = centrality_degree(g)
    for level in levels:
        protein_count_total.append(0)
        protein_count_essential.append(0)
        for vertex, degree in degrees:
            if degree >= level:
                if vertex.name in essential_proteins:
                    protein_count_essential[-1] += 1
                protein_all_total[-1] += 1
    # plotting proportions
    plot_stats(
        protein_count_total,
        protein_count_essential,
        levels,
    )
    # hypergeometric test
    pvalues = []
    for index, level in enumerate(levels):
        protein_count = len(g.vs)
        # total number of protein: protein_count,
        # subset of proteins: protein_count_total[index]
        # total number of essential proteins: len(essential_proteins)
        # number of essential proteins in subset: protein_count_essential[index]
        pvalues.append(phyper(
            protein_count, len(essential_proteins),
            protein_count_total[index],
            protein_count_essential[index])
        ))
    # plotting p-value evolution
    plot_phyper(pvalues, levels)


if __name__ == '__main__':
    five_vertices()

    graph = compute_biological_data()
    essential_proteins = []  #TODO: load the essential proteins set
    centrality_degree(graph, essential_proteins)
