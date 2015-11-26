import itertools
import operator
import igraph as ig


# TO BE USED IN TP
def get_edges(graph, vertex):
    "Return iterable of edges of the given graph that are linked to given vertex"
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


# TO BE USED IN TP
def RkNN(graph, k=1):
    "Return RkNN of given graph"
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


def exercice4():
    g = ig.Graph()
    for source, target, weight in get_graph_from(''):
        # pass
        g.add_edge(source, target, weight=weight)



def figure1Ning():
    g = ig.Graph(directed=False)
    # i.plot(g)
    # print(help(g.add_vertex))
    for i in range(1, 6):
        g.add_vertex(i, label='node ' + str(i))
    # print(help(g.add_edge))
    g.es["weight"] = 1.0  # make the graph a weighed one
    g[0, 1] = 2.5
    g[0, 1] = 2.5
    g[1, 2] = 2.0  # equivalent to g.add_edge(1, 2, weight=2.0)
    g[2, 3] = 1.0
    g[3, 4] = 4.0
    g[0, 4] = 5.0
    g[0, 3] = 1.5
    g[1, 3] = 2.5

    print('WEIGHED:', g.is_weighted())
    visual_style = {
        'vertex_label': g.vs['label'],
        'edge_label'  : g.es['weight'],
        'layout'      : g.layout_circle(),
        'margin'      : 150,
    }
    ig.plot(g, **visual_style)

    rnn = RkNN(g, k=2)
    rnn_visual_style = {
        'vertex_label': rnn.vs['label'],
        'edge_label'  : rnn.es['weight'],
        'layout'      : rnn.layout_kamada_kawai(),
        'margin'      : 150,
        'autocurve'  : False,
    }
    ig.plot(rnn, **rnn_visual_style)


if __name__ == '__main__':
    figure1Ning()
