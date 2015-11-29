"""
Some igraph and libtp usage examples are grouped here.

"""
from libtp import plot_stats

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


def plot_dumb_stats():
    """Show statistics about proteins awesomness"""
    plot_stats(
        (40, 23, 12),  # all proteins
        (20, 11,  7),  # essential proteins
        ( 1,  5, 10),  # awesomness levels
        stat_name='awesomness',  #xlabels
        all_color='magenta',
        essential_color='yellow'
    )


def add_property(graph, property_name, value):
    """Add given property with given value to all vertices of the graph"""
    properties = {property_name: value}
    for vertex in graph.vs:
        vertex.update_attributes(properties)
