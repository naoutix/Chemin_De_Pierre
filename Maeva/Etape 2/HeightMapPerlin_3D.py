# https://jackmckew.dev/3d-terrain-in-python.html

# #%matplotlib inline
import noise
import numpy as np
import matplotlib
from matplotlib import pyplot
from mpl_toolkits.mplot3d import axes3d

shape = (50,50)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=42)

# C'est la variable 'terrain' qui donne l'impression de mer, montagne...
matplotlib.pyplot.imshow(world,cmap='terrain')
#plot_surface facecolors
pyplot.show()

#############################################

lin_x = np.linspace(0,1,shape[0],endpoint=False)
lin_y = np.linspace(0,1,shape[1],endpoint=False)
x,y = np.meshgrid(lin_x,lin_y)

fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(111, projection="3d")

# Changer la texture avec l'argument facecolors ?
ax.plot_surface(x,y,world,cmap='terrain')
pyplot.show()

# #############################################

# terrain_cmap = matplotlib.cm.get_cmap('terrain')
# def matplotlib_to_plotly(cmap, pl_entries):
#     h = 1.0/(pl_entries-1)
#     pl_colorscale = []

#     for k in range(pl_entries):
#         C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
#         pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

#     return pl_colorscale

# terrain = matplotlib_to_plotly(terrain_cmap, 255)

# import plotly
# import plotly.graph_objects as go
# plotly.offline.init_notebook_mode(connected=True)

# fig = go.Figure(data=[go.Surface(colorscale=terrain,z=world)])

# fig.update_layout(title='Random 3D Terrain')

# # Note that include_plotlyjs is used as cdn so that the static site generator can read it and present it on the browser. This is not typically required.
# html = plotly.offline.plot(fig, filename='3d-terrain-plotly.html',include_plotlyjs='cdn')



