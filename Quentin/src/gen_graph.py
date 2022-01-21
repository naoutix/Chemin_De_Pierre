import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot

def gen_graph(points, delta_max=.15):
    shape = int(np.sqrt(points.shape[0]))
    sup = 10

    Zx = points[:,2]
    Zy = np.reshape(Zx,(shape,shape)).T.flatten()

    edge_x = np.zeros((shape,shape-1))
    edge_y = np.zeros((shape,shape-1))

    for i in range(shape):
        for j in range(shape-1):
            dx = abs(Zx[i*shape+j] - Zx[i*shape+j+1])
            if dx > delta_max:
                edge_x[i, j] = sup
            else:
                edge_x[i, j] = dx

            dy = abs(Zy[i*shape+j] - Zy[i*shape+j+1])
            if dy > delta_max:
                edge_y[i, j] = sup
            else:
                edge_y[i, j] = dy

    G = nx.Graph()

    for i in range(shape):
        nodes = np.arange(i*shape,(i+1)*shape)
        G.add_nodes_from(nodes)

        edges_x = [(nodes[k], nodes[k+1], edge_x[i,k]) for k in range(shape-1)]
        edges_y = [(k*shape+i, (k+1)*shape+i, edge_y[i,k]) for k in range(shape-1)]
        
        G.add_weighted_edges_from(edges_x)
        G.add_weighted_edges_from(edges_y)

    return G

#nx.write_gexf(G, "graph_grad.gexf")
#write_dot(G, 'graph_grad.dot')