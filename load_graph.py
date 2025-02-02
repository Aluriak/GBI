# -*- coding: utf-8 -*-
# Anti dinosaur import
import __future__
# Standard imports
import csv
import itertools as it
import re

# Custom imports & Awsome lib (...)
import igraph as ig


def parse_nodes(path="./data/yeast_biogrid_3.4.129_nodes.csv"):
    """Read informations about nodes from a file 
    exported from biogrid & cytoscape.

    :param arg1: Optional. Path of csv file.
    :type arg1: <str>

    :return: dict of entrez_id with the mapping of yeast_id
    :rtype: <dict yeast_id:entrez_id>

    """

    # 5ième champ:
    # 851136|31676|CDC73|YLR418C|L000002792
    # group(1): entrez_id
    # group(2): yeast_id
    expr_reg = re.compile('^([\d]+)\|.*\|(Y[\d\w\-]+)\|?.*$')
    with open(path) as file:
        # Skip headers
        next(file)

        yeast_id_entrez_id = dict()
        # Yolo !
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            try:
                gprs = expr_reg.match(row[4])
                yeast_id_entrez_id[gprs.group(2)] = gprs.group(1)
            except AttributeError:
                pass

        print("Mapping of {} yeast_id/{} nodes.".format(len(yeast_id_entrez_id), i))

    return yeast_id_entrez_id


def get_go_sub(path="./data/gene_association_R64-2-1_20150113.sgd"):
    """Return lists of proteins for each GO term.
    File was taken from yeastgenome.org

    SGD	S000001855	ACT1	contributes_to	GO:0004402	SGD_REF:S000046619|PMID:10911987	IDA		F	Actin	YFL039C|ABY1|END7|actin	gene	taxon:559292	20131015	SGD		

    :return: Go term: list of proteins
    :rtype: <defaultdict <str>:<list> >

    """

    from collections import defaultdict

    go_sub = defaultdict(list)
    #expr_reg = re.compile('^(Y[\d\w\-]+)$')
    expr_reg = re.compile('^(Y[\d\w\-]+)\|?.*$')

    with open(path) as file:
        # Skip 8 headers
        [next(file) for _ in range(8)]

        # Yolo !
        reader = csv.reader(file, delimiter='\t')

        for row in reader:
            try:
                go_sub[row[4]].append(expr_reg.match(row[10]).group(1))
            except AttributeError:
                pass

#        {go_sub[row[4]].append(row[9]) for row in reader
#            if expr_reg.match(row[9])}

#        print(go_sub)
        print("{} Gene ontology numbers".format(len(go_sub)))

    print({go:len(go_sub[go]) for go in go_sub if len(go_sub[go]) >= 100})
    # GO:0008380 RNA splicing
    # GO:0016787 hydrolase activity
    # GO:0005524 ATP binding
    return go_sub


def read_essentials(path="./data/Essential_ORFs.txt"):
    """his function loads all yeast_id of essential genes.

    The file was taken from stanford :
    http://www-sequence.stanford.edu/group/yeast_deletion_project/Essential_ORFs.txt

    ..Note: Return of 1122/1156 references in file.

    :param arg1: Path of txt file.
    :type arg1: <str>
    :return: set of yeast_id of essential genes
    :rtype: <set>

    """

    with open(path) as file:
        # Skip headers
        next(file)

        # Yolo !
        reader = csv.reader(file, delimiter='\t')
        essentials_prots = {row[1] for row in reader \
                            if (len(row) >= 2) and (row[1] != '')}

        print("{} essential genes from stanford.".format(len(essentials_prots)))

        return essentials_prots


def parse_ugly_tab(path="./data/yeast_biogrid_3.4.129_export.csv"):
    """This function reads a csv file from BIOGRID, and returns all nodes and 
    edges with weights.

    ..Note: You must return a list of nodes. Why ?
        When you create a graph, a set (an iterable) will not be accepted ! 
        This tool doesn't respect the pythonic way of thinking !
        It's coded in java python. Deal with that.

    :param arg1: Optional. Path of csv file.
    :type arg1: <str>

    :return: LIST of nodes, dict of edges with weights.
    :rtype: <list>, <dict (node1, node2):weight>

    """

    with open(path) as file:
        # Skip headers
        next(file)

        # Yolo !
        reader = csv.reader(file, delimiter=',')

        # Ex of line:
        # ['822613', '855264 (822613) 855267', '6', 'synthetic genetic interaction defined by inequality', '23390603']
        g = ((edge.split(' '), weight) for r_name, edge, weight, _, _ in reader)

        weights_for_edges = {(edge[0], edge[2]):weight for edge, weight in g}

        g = (key for key in weights_for_edges)

        # The set ensures the uniqueness of the nodes
        # list(set()) is ugly ? Yes it's igraph.
        all_nodes = list(set(it.chain(*g)))

        print("Loaded from BIOGRID: {} nodes, {} edges.".format(len(all_nodes), 
                                                                len(weights_for_edges)))

        return all_nodes, weights_for_edges


def get_common_yeast_id(yeast_id_entrez_id, essentials_prots):
    """This function returns yeast_id which are common in nodes used in the graph
    and the essential genes.

    :rtype: <set>

    """

    common_yeast_id = set(yeast_id_entrez_id.keys()) & essentials_prots
    entrez_ids = {yeast_id_entrez_id[yeast_id] for yeast_id in common_yeast_id}

    print("{} common essential proteins (BIOGRID/stanford).".format(len(common_yeast_id)))
    return entrez_ids


def color_graph_with_essential(graph, entrez_ids):
    """This function colors all essential nodes in the given graph
    """

    seq = graph.vs.select(name_in=entrez_ids)

    for vertex in seq:
        vertex['color'] = 'green'

    print("Color essential nodes [Ok]")


def make_a_graph(all_nodes, weights_for_edges):
    """This function creates a weighted graph according to given parameters.

    :param arg1: LIST of nodes.
    :param arg2: dict of edges with weights.
    :type arg1: <list>
    :type arg2: <dict (node1, node2):weight>

    :return: Return the igraph object.
    :rtype: <igraph.Graph>

    """

    # Intialization of empty graph having the size of the number of nodes
    g = ig.Graph(len(all_nodes))

    # Import of nodes with their names
    # PS: YOU MUST PASS A LIST !! 
    # For example, a set is an iterable but it will not be accepted! 
    # This tool doesn't respect the pythonic way of thinking !
    g.vs["name"] = all_nodes

    # Import of edges (dont forget the structure: {(node1, node2):weight})
    print("Please wait during the graph creation...")
    for edge in weights_for_edges:
        try:
            g[edge[0], edge[1]] = weights_for_edges[edge]
        except:
            print("An exception occurs on {} with weight {}.".format(
                  edge,
                  weights_for_edges[edge]))
            raise

    print("Edge count: {}".format(g.ecount()))

    return g


def make_plot_save_graph_with_networkx(weights_for_edges, entrez_ids):
    """Return graph by networkx

    :param arg1: dict of edges with weights.
    :param arg2: essential proteins in entrez_ids. Used to color essential nodes.
    :type arg1: <dict (node1, node2):weight>
    :type arg2: <set>
    :return: graph by networkx.
    :rtype: <?>

    """

    import networkx as nx
    import matplotlib.pyplot as plt

    print("NetworkX...")

    G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc

    # Add edges
    G.add_weighted_edges_from([(n1, n2, weights_for_edges[(n1, n2)])
                                for n1, n2 in weights_for_edges])

    # Colors for essential proteins
    def get_colors(node):
        return 'g' if node in entrez_ids else 'r'

    nodes_colors = [get_colors(node) for node in G.nodes_iter()]

    #https://networkx.github.io/documentation/latest/reference/generated/
    #networkx.drawing.nx_pylab.draw_networkx.html#networkx.drawing.nx_pylab.draw_networkx
    print('Color for nodes [Ok]')
    print('Drawing...')

    # positions for all nodes
    # pos = nx.spring_layout(G) # default => UGLY !
    # apt-get install graphviz graphviz-dev (python-pygraphviz)
    # pip-3.2 install pygraphviz
    # sudo pip3 install nxpydot + pydot2
    #pos = nx.graphviz_layout(G, prog='neato')
    nx.draw_networkx(G,
                     #pos=pos,
                     node_color=nodes_colors, 
                     node_size=20, 
                     with_labels=False)

    print('Drawing [Ok]')
    print('Saving...')

    # Save GML & png
    nx.write_gml(G, "full_biological_data_networkx.gml")
    plt.savefig("full_biological_data_networkx.png", 
                format='png')
    # Release memory
    plt.close()

    return G


def prune_my_graph(graph, wanted_go_term, go_sub, yeast_id_entrez_id):
    """Return a subgraph of proteins from a GO set.

    # GO:0008380 RNA splicing
    # GO:0016787 hydrolase activity
    # GO:0005524 ATP binding
    # PS: run get_go_sub() to see if there are useful GO terms

    """

    mapping = {yeast_id_entrez_id[id] for id in go_sub[wanted_go_term] if id in yeast_id_entrez_id}
    print("{} nodes in GO set.".format(len(mapping)))

    pruned_vs = graph.vs.select([node.index for node in graph.vs.select(name_in=mapping)])
    graph = graph.subgraph(pruned_vs)

    # Delete nodes with degree = 0
    pruned_vs = graph.vs.select([node.index for node in graph.vs.select(_degree_gt=0)])
    graph = graph.subgraph(pruned_vs)

    print("{} nodes, {} edges in cleaned (without 0 degree) GO subnetwork."\
          .format(graph.vcount(), graph.ecount()))

    return graph


if __name__ == "__main__":

    # GO mapping
    go_sub = get_go_sub()

    # Get all existing yeast_id & entrez_id (nodes in graph) from biogrid
    yeast_id_entrez_id = parse_nodes()

    # Get all essential proteins (yeast_ids)
    essentials_prots = read_essentials()

    # Get common essential proteins between biogrid & stanford (yeast_id => entrez_ids)
    entrez_ids = get_common_yeast_id(yeast_id_entrez_id, essentials_prots)

    with open("essentials.txt", 'w') as file:
        for id in entrez_ids:
            file.write(id + '\n')

    # Parse csv file (nodes involved in a weighted edge)
    all_nodes, weights_for_edges = parse_ugly_tab()

    # Make graph with networkx
#    make_plot_save_graph_with_networkx(weights_for_edges, entrez_ids)


    # Reload big graph
    import os.path
    import pickle

    if os.path.isfile('graph.pkl'):
        # Reload
        with open('graph.pkl', 'rb') as pklFile:
            graph = pickle.load(pklFile)

        print("Loaded from pickle: {} nodes, {} edges.".format(graph.vcount(), graph.ecount()))
    else:
        # Load a graph
        graph = make_a_graph(all_nodes, weights_for_edges)

        # Save
        with open('graph.pkl', 'wb') as output:
            pickle.dump(graph, output)


    go_set = {go for go in go_sub if len(go_sub[go]) >= 100}

    for go in go_set:
        print('---')
        print(go)
        # Subgraph of proteins from a GO set.
        subgraph = prune_my_graph(graph, go, go_sub, yeast_id_entrez_id)

        # Save the sub graph
        subgraph.save("biological_data_" + go.split(':')[1] + ".gml", format="gml")

        # Color the essential proteins in the graph
        color_graph_with_essential(subgraph, entrez_ids)

        # save the colored png
        ig.plot(subgraph, "biological_data_" + go.split(':')[1] + "_colored.png", vertex_size=10)

    exit()

    # Subgraph of proteins from a GO set.
    # GO:0008380 RNA splicing
    # GO:0016787 hydrolase activity
    # GO:0005524 ATP binding
    # PS: run get_go_sub() to see if there are useful GO terms
    subgraph = prune_my_graph(graph, 'GO:0004674', go_sub, yeast_id_entrez_id)

    # Color the essential proteins in the graph
    #color_graph_with_essential(subgraph, entrez_ids)

    # Plot the graph
    # avoid trace problems:
    # raise TypeError("plotting not available")
    # TypeError: plotting not available
    # pip install cairocffi
#    ig.plot(subgraph,
#            #vertex_label=graph.vs['name'],
#            #layout=graph.layout_kamada_kawai(),
#            vertex_size=10)

    # Save the sub graph
    subgraph.save("biological_data.gml", format="gml")
    # Or (marche pas lolilol)
    # subgraph.write_gml()


