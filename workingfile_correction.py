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
# Anti dinosaur import
from __future__ import print_function
import igraph as ig
from libtp import (phyper, plot_phyper, plot_stats,
                   compute_biological_data, read_essentials)


def five_vertices():
    """
    Function for the section 1.
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
        # result.append((vertex, ?))  # TODO
        result.append((vertex, vertex.degree()))  # TODO
    return tuple(result)


def pipeline_degree(g, essential_proteins, centrality, thresholds):
    # thresholds = (1, 2, 5, 8, 12, 20)  # TODO
    # thresholds = range(1, 20)  # TODO
    protein_count_total     = []  # number of proteins with a degree >= threshold
    protein_count_essential = []  # same for essential proteins
    # degrees = centrality_degree(g)
    degrees = [(v, centrality(v)) for v in g.vs]
    for threshold in thresholds:
        protein_count_total.append(0)
        protein_count_essential.append(0)
        for vertex, degree in degrees:
            if degree >= threshold:
                if vertex.attributes()['name'] in essential_proteins:
                    protein_count_essential[-1] += 1
                protein_count_total[-1] += 1
    # plotting proportions
    plot_stats(
        protein_count_total,
        protein_count_essential,
        thresholds,
    )
    # hypergeometric test
    pvalues = []
    for index, threshold in enumerate(thresholds):
        protein_count = len(g.vs)
        # total number of protein: protein_count,
        # subset of proteins: protein_count_total[index]
        # total number of essential proteins: len(essential_proteins)
        # number of essential proteins in subset: protein_count_essential[index]
        pvalues.append(phyper(
            protein_count, len(essential_proteins),
            protein_count_total[index],
            protein_count_essential[index]
        ))
    # plotting p-value evolution
    plot_phyper(pvalues, thresholds)


if __name__ == '__main__':
    # five_vertices()  # comment that when section 2 is reached

    # SECTION 2
    # TODO: create a graph with the igraph API, and test centrality measures on it.
    # TODO: read graph from the gml file
    # TODO: read the essential proteins
    # TODO: call the pipeline
    import glob
    for filename in reversed(glob.glob('*.gml')):
    # for filename in ('biological_data_0005730.gml',):
        print('FILENAME:', filename)
        g = ig.Graph.Read(filename, format='gml')
        try:
            print('degree...')
            pipeline_degree(g, read_essentials(g), lambda v: v.degree(), range(1, 45))
        except KeyboardInterrupt, e:
            print('INTERRUPT:DEGREE:', filename)
        try:
            print('between...')
            pipeline_degree(g, read_essentials(g), lambda v: v.betweenness(), range(1, 55))
        except KeyboardInterrupt, e:
            print('INTERRUPT:BETWEEN:', filename)
        try:
            print('close...')
            pipeline_degree(g, read_essentials(g), lambda v: v.closeness(), tuple(x/100. for x in range(100)))
        except KeyboardInterrupt, e:
            print('INTERRUPT:CLOSE:', filename)
