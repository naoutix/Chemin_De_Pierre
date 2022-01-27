import numpy as np
import cv2
from utils import *

x, y, z = read_file('../data/terrain2_3dpoints.txt')
shape = x.shape
taille_image = 50

chemin = np.load("../data/chemin.npy")
coord_chemin = [(chemin[0][k], chemin[1][k]) for k in range(chemin.shape[1])]

xnew = chemin[0]
ynew = chemin[1]

dist_min = 12000

""" Carte de segmentation """
with open('../data/textures/labels/seg11.npy', 'rb') as f:
    markers = np.load(f)

nb_classes = np.max(markers) - 1  # Classe background et contour en plus des pierres

im = np.zeros((shape[0] * taille_image, shape[1] * taille_image, 3))

t1 = cv2.imread('../data/textures/real_textures/water_texture.jpg')
t1 = cv2.resize(t1, (taille_image, taille_image)) / 255

t2 = cv2.imread('../data/textures/real_textures/sand_texture.jpg')
t2 = cv2.resize(t2, (taille_image, taille_image)) / 255

t3 = cv2.imread('../data/textures/real_textures/grass_texture.jpg')
t3 = cv2.resize(t3, (taille_image, taille_image)) / 255

t4 = cv2.imread('../data/textures/real_textures/ground_texture.jpg')
t4 = cv2.resize(t4, (taille_image, taille_image)) / 255

t5 = cv2.imread('../data/textures/real_textures/ice_texture.jpg')
t5 = cv2.resize(t5, (taille_image, taille_image)) / 255

t_chemin = cv2.imread('../data/textures/freeTexture11.png')
t_chemin = cv2.resize(t_chemin, (taille_image, taille_image)) / 255

""" Image segmentée par watershed """
seg_img = cv2.imread('../data/textures/segmentation11.jpg',cv2.IMREAD_UNCHANGED)

""" Attention downsample segmentation -> downsample markers ? effectuer la segmentation sur l'image déjà downsample ? """
seg_img = np.int8(cv2.resize(seg_img, (taille_image, taille_image)) / 255)

seg_img = np.repeat(np.expand_dims(seg_img, axis=2), 3, axis=2)
print(seg_img[0][0])

seuils = [-3, 0, 1, 3]

print("CREATION TEXTURE MAP\n")
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        """ CREER IMAGE """
        val_z = z[i, j]
        if val_z < seuils[0]:
            if (j,i) in coord_chemin:
                tmp = np.where(seg_img == [1,1,1],t_chemin,t1)
            else:
                tmp = t1
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = tmp
        elif val_z < seuils[1]:
            if (j,i) in coord_chemin:
                tmp = np.where(seg_img == [1,1,1],t_chemin,t2)
            else:
                tmp = t2
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = tmp
        elif val_z < seuils[2]:
            if (j,i) in coord_chemin:
                tmp = np.where(seg_img == [1,1,1],t_chemin,t3)
            else:
                tmp = t3
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = tmp
        elif val_z < seuils[3]:
            if (j,i) in coord_chemin:
                tmp = np.where(seg_img == [1,1,1],t_chemin,t4)
            else:
                tmp = t4
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = tmp
        else:
            if (j,i) in coord_chemin:
                tmp = np.where(seg_img == [1,1,1],t_chemin,t5)
            else:
                tmp = t5
            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = tmp
"""
print("APPLICATION CHEMIN")
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        if (j, i) in coord_chemin:
            seg_tmp = np.zeros(seg_img.shape)

            for k in range(2, nb_classes + 1):  # Pour chaque classe i.e. pierre
                coord = np.argwhere(markers == k)  # Récupérer les coordonnées
                proj_coord = np.transpose(np.array([coord[:, 0] + i * taille_image, coord[:,
                                                                                    1] + j * taille_image]))  # Projection de repère case à repère image
                for q in range(coord.shape[0]):
                    seg_tmp[coord[q, 0], coord[q, 1]] = 1

            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = np.where(
                seg_tmp == 1,
                t_chemin, im[i * taille_image:(i + 1) * taille_image,
                          j * taille_image:(j + 1) * taille_image, :])

            im[i * taille_image:(i + 1) * taille_image, j * taille_image:(j + 1) * taille_image, :] = t_chemin
"""
cv2.imwrite('../data/texture_map_chemin_test.png', im * 255)

cv2.imshow('Texture map', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
