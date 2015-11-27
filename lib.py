from __future__ import print_function
import itertools
import igraph as ig
from libtp import get_edges, RkNN, plot_stats, plot_phyper
from examples import plot_dumb_stats




# EXAMPLE OF EXERCISE IN THE TP
def exercice4():
    g = ig.Graph()
    for source, target, weight in get_graph_from(''):
        # pass
        g.add_edge(source, target, weight=weight)




def figure1Ning():
    # plot_stats(
        # [3000, 2000, 1000],
        # [ 300,  200,  100],
        # [  10,   20,   30],
    # )
    plot_phyper(
        (0.23, 0.42, 0.2),
        (3, 4, 8),
    )
    exit()
    plot_dumb_stats()

    g = ig.Graph(directed=False)
    # i.plot(g)
    # print(help(g.add_vertex))
    for i in range(1, 6):
        g.add_vertex(i, label='node ' + str(i))
    # print(help(g.add_edge))
    g.es["weight"] = 1.0  # make the graph a weighed one
    g[0, 1] = 2.5
    g[0, 1] = 2.5
    # g[1, 2] = 2.0  # equivalent to g.add_edge(1, 2, weight=2.0)
    g.add_edge(1, 2, weight=2.0, color='green')
    g[2, 3] = 1.0
    g[3, 4] = 4.0
    g[0, 4] = 5.0
    g[0, 3] = 1.5
    g[1, 3] = 2.5


    # CENTRALITY
    for vertex in g.vs:
        print('VERTEX:', vertex)
        print('\tdegree:', vertex.degree())
        print('\tbetweenness:', vertex.betweenness())
        print('\tcloseness:', vertex.closeness())

    # PLOT
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
