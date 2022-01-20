import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

points = np.loadtxt('terrain2_3dpoints.txt')

tri = Delaunay(points[:,:2])

"""f = open('terrain2_3dpoints.obj', 'w')
for p in range(points.shape[0]):
    f.write('v '+str(points[p,0])+' '+str(points[p,1])+' '+str(points[p,2])+'\n')

for t in tri.simplices:
    f.write('f '+str(t[0]+1)+' '+str(t[1]+1)+' '+str(t[2]+1)+'\n')
f.close()
"""
fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')
ax.plot_trisurf(points[:,0], points[:,1], points[:,2], triangles=tri.simplices, cmap=plt.cm.Spectral)

plt.show()