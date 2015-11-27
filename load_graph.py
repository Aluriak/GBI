# Anti dinosaur import
import __future__
# Standard imports
import csv
import itertools as it

# Custom imports & Awsome lib (...)
import igraph as ig


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

        print("Loaded: {} nodes, {} edges.".format(len(all_nodes), 
                                                   len(weights_for_edges)))

        return all_nodes, weights_for_edges

def make_a_graph(all_nodes, weights_for_edges):
    """This function creates a weighted graph according to given parameters.

    :param arg1: LIST of nodes.
    :param arg2: dict of edges with weights.
    :type arg1: <list>
    :type arg2: <dict (node1, node2):weight>

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


if __name__ == "__main__":

    # Parse csv file
    all_nodes, weights_for_edges = parse_ugly_tab()

    # Load a graph
    make_a_graph(all_nodes, weights_for_edges)


