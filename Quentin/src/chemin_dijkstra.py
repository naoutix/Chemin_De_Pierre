import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1 as axes_grid1
from gen_graph import gen_graph
from utils import *
from networkx.algorithms.shortest_paths.weighted import dijkstra_path

points = np.loadtxt("../data/terrain2_3dpoints.txt")
G = gen_graph(points)

shape = int(np.sqrt(points.shape[0]))

cvt_nodes = np.reshape(np.arange(points.shape[0]), (shape,shape))

depart = np.random.randint(shape,size=2)
fin = np.random.randint(shape,size=2)

node_depart = cvt_nodes[depart[0],depart[1]]
node_fin = cvt_nodes[fin[0],fin[1]]

print("POINT DE DEPART : ",depart)
print("POINT DE FIN : ",fin)

node_list = dijkstra_path(G,node_depart,node_fin)

x_list, y_list = [], []

for node in node_list:
    u = np.where(cvt_nodes == node)
    x_list.append(u[0][0])
    y_list.append(u[1][0])

np.save("../data/chemin.npy",np.array([x_list,y_list]))

plt.figure()
plt.imshow(np.reshape(points[:,2], (shape,shape)),cmap='terrain')
plt.plot(depart[0],depart[1],'g*')
plt.plot(fin[0],fin[1],'r*')
plt.plot(x_list,y_list,'b-')
plt.savefig("../data/chemin.png", dpi=150)
plt.show()

