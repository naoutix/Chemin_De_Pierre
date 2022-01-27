import noise
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import plotly
import plotly.graph_objects as go

""" Conversion color map matplotlib vers plotly """
terrain_cmap = matplotlib.cm.get_cmap('terrain')
def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

    return pl_colorscale

terrain = matplotlib_to_plotly(terrain_cmap, 255)

""" Paramètres bruit """
shape = (100,100)
scale = 25.0
octaves = 3
persistence = 0.2
lacunarity = 2.0

""" Génération height map """
world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = 10*noise.pnoise2(i/scale,
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=42)

""" Plot height map 2D """
"""
plt.figure()
plt.imshow(world,cmap='terrain')
plt.show()"""

""" Générer coordonées (x,y) """
lin_x = np.linspace(0,1,shape[0],endpoint=False)
lin_y = np.linspace(0,1,shape[1],endpoint=False)
x,y = np.meshgrid(lin_x,lin_y)

f = open('terrain2_3dpoints.txt', 'w')
for i in range(shape[0]):
    for j in range(shape[1]):
        f.write(str(x[i,j])+" "+str(y[i,j])+" "+str(world[i,j])+"\n")
f.close()

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(x,y,world,cmap='terrain')
plt.show()"""


fig = go.Figure(data=[go.Surface(colorscale=terrain,z=world)])

"""fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=world,
                   opacity=0.20,
                   color='green')])"""

fig.update_layout(title='Random 3D Terrain')

# Note that include_plotlyjs is used as cdn so that the static site generator can read it and present it on the browser. This is not typically required.
html = plotly.offline.plot(fig, filename='3d-mesh-flat-plotly.html',include_plotlyjs='cdn')