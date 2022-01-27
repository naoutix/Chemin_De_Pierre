from mayavi import mlab
import numpy as np
from tvtk.api import tvtk
from PIL import Image

points = np.loadtxt("../data/terrain2_3dpoints.txt")
shape = int(np.sqrt(points.shape[0]))

x = np.reshape(points[:,0], (shape,shape))
y = np.reshape(points[:,1], (shape,shape))
z = np.reshape(points[:,2], (shape,shape))

im = Image.open("../data/texture_map_chemin_test-merge.pngcd Doc    ")
im2 = im.rotate(90)
im2.save("../data/texture_map_90.png")

img = tvtk.PNGReader()
img.file_name = "../data/texture_map_90.png"

texture = tvtk.Texture(input_connection=img.output_port, interpolate=0)

s = mlab.surf(z,color=(1,1,1),warp_scale="auto")
s.actor.enable_texture = True
s.actor.tcoord_generator_mode = 'plane'
s.actor.actor.texture = texture
mlab.show()
