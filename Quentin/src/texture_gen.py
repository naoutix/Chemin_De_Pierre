import numpy as np
import cv2
from utils import *

x, y, z = read_file('terrain_3dpoints.txt')
shape = x.shape

im = np.zeros((shape[0]*50,shape[1]*50,3))

t1 = cv2.imread('textures/freeTexture4.png')
t1 = cv2.resize(t1,shape)/255

t2 = cv2.imread('textures/freeTexture1.png')
t2 = cv2.resize(t2,shape)/255

t3 = cv2.imread('textures/freeTexture2.png')
t3 = cv2.resize(t3,shape)/255

t4 = cv2.imread('textures/freeTexture14.png')
t4 = cv2.resize(t4,shape)/255

t5 = cv2.imread('textures/freeTexture15.png')
t5 = cv2.resize(t5,shape)/255

n = shape[0]
seuils = [-0.05, 0, 0.05, 0.1]

for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        """ CREER IMAGE """
        val_z = z[i,j]
        if val_z < seuils[0]:
            im[i*n:(i+1)*n,j*n:(j+1)*n,:] = t1
        elif val_z < seuils[1]:
            im[i*n:(i+1)*n,j*n:(j+1)*n,:] = t2
        elif val_z < seuils[2]:
            im[i*n:(i+1)*n,j*n:(j+1)*n,:] = t3
        elif val_z < seuils[3]:
            im[i*n:(i+1)*n,j*n:(j+1)*n,:] = t4
        else:
            im[i*n:(i+1)*n,j*n:(j+1)*n,:] = t5

cv2.imwrite('texture_map.png',im*255)

cv2.imshow('Texture map',im)
cv2.waitKey(0)
cv2.destroyAllWindows()