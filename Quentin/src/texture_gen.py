import numpy as np
import cv2
from utils import *

x, y, z = read_file('../data/terrain2_3dpoints.txt')
shape = x.shape
taille_image = 50;

chemin = np.load("../data/chemin.npy")
coord = [(chemin[0][k],chemin[1][k]) for k in range(chemin.shape[1])]

im = np.zeros((shape[0]*taille_image,shape[1]*taille_image,3))

t1 = cv2.imread('../data/textures/freeTexture4.png')
t1 = cv2.resize(t1,(taille_image,taille_image))/255

t2 = cv2.imread('../data/textures/freeTexture1.png')
t2 = cv2.resize(t2,(taille_image,taille_image))/255

t3 = cv2.imread('../data/textures/freeTexture2.png')
t3 = cv2.resize(t3,(taille_image,taille_image))/255

t4 = cv2.imread('../data/textures/freeTexture14.png')
t4 = cv2.resize(t4,(taille_image,taille_image))/255

t5 = cv2.imread('../data/textures/freeTexture15.png')
t5 = cv2.resize(t5,(taille_image,taille_image))/255

t_chemin = cv2.imread('../data/textures/freeTexture8.png')
t_chemin = cv2.resize(t_chemin,(taille_image,taille_image))/255

seuils = [-3, 0, 1, 3]

for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        """ CREER IMAGE """
        if (j,i) in coord:
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t_chemin
        else:
            val_z = z[i,j]
            if val_z < seuils[0]:
                im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t1
            elif val_z < seuils[1]:
                im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t2
            elif val_z < seuils[2]:
                im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t3
            elif val_z < seuils[3]:
                im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t4
            else:
                im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t5

cv2.imwrite('../data/texture_map_chemin.png',im*255)

cv2.imshow('Texture map',im)
cv2.waitKey(0)
cv2.destroyAllWindows()