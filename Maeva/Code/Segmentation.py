import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from skimage import morphology

import sys
from PIL import Image
import cv2

def SegmentationTexture():
    # /!\ Ne fonctionne que sur des formats jpg
    chemin_texture = input("Entrez le chemin vers la texture souhaitee sur le chemin (.jpg):")

    # Dans le cas d'une segmentation de pierres: classification fond/forme
    n_classes = 2

    # On charge l'image et on la répète
    bg = Image.open(chemin_texture)
    bg_w, bg_h = bg.size
    new_im = Image.new('RGB', (3000,3000))
    w, h = new_im.size
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            new_im.paste(bg, (i, j))
    new_im.save("Images_intermediaires/Tile_pierres.jpg")

    # Segmentation avec k-means

    texture = np.array(new_im, dtype=np.float64) / 255

    w, h, d = original_shape = tuple(texture.shape)
    assert d == 3
    image_array = np.reshape(texture, (w * h, d))

    image_array_sample = shuffle(image_array, random_state=0, n_samples=1_000)
    kmeans = KMeans(n_clusters=n_classes, random_state=0).fit(image_array_sample)
    labels = kmeans.predict(image_array)

    for i in range(labels.shape[0]):
        if (labels[i] == 1):
            labels[i] = 255

    image = labels.reshape(w,h)

    plt.imsave("Images_intermediaires/texture_segmentee_tile.jpg", image)


    if (chemin_texture == "Textures/freeTexture3.jpg") or (chemin_texture == "Textures/freeTexture8.jpg") or (chemin_texture == "Textures/freeTexture11.jpg"):

        texture_segmentee = cv2.imread("Images_intermediaires/texture_segmentee_tile.jpg")
        grayImage = cv2.cvtColor(texture_segmentee, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite("Images_intermediaires/blackwhite_texture.jpg", blackAndWhiteImage)
        inverse = cv2.bitwise_not(blackAndWhiteImage)
        cv2.imwrite("Images_intermediaires/blackwhite_texture_inverse.jpg", inverse)
        if (chemin_texture == "Textures/freeTexture3.jpg"):
            mask_im = inverse
        if (chemin_texture == "Textures/freeTexture8.jpg"):
            mask_im = inverse
        if (chemin_texture == "Textures/freeTexture11.jpg"):
            mask_im = inverse
        mask_im = np.asarray(mask_im, dtype='uint8' )

        if (chemin_texture == "Textures/freeTexture3.jpg"):
            bg = Image.open("Textures/masque_freeTexture3.jpg")
        if (chemin_texture == "Textures/freeTexture8.jpg"):
            bg = Image.open("Textures/masque_freeTexture8.jpg")
        if (chemin_texture == "Textures/freeTexture11.jpg"):
            bg = Image.open("Textures/masque_freeTexture11.jpg")
        
        bg_w, bg_h = bg.size
        new_im = Image.new('RGB', (3000,3000))
        w, h = new_im.size
        for i in range(0, w, bg_w):
            for j in range(0, h, bg_h):
                new_im.paste(bg, (i, j))
        new_im.save("Images_intermediaires/Tile_pierres_bw.jpg")
        image_ref = np.asarray(new_im, dtype='uint8' )
        image_ref_np = np.zeros((w,h))
        for i in range(w):
            for j in range(h):
                image_ref_np[i,j] = image_ref[i,j,0]
        image_ref_np = np.asarray(image_ref_np, dtype='uint8' )

        image_ref_np = image_ref_np.reshape(w*h)
        mask_im = mask_im.reshape(w*h)
        print(accuracy_score(mask_im,image_ref_np))

        # Dans le cas d'une classification binaire: calcul des TP, FP...
        if (n_classes == 2):
            TP, FP, TN, FN = 0, 0, 0, 0
            for i in range(w*h):
                if (mask_im[i] == 255):
                    if (image_ref_np[i] == 255):
                        TP = TP + 1
                    else:
                        FP = FP + 1
                else:
                    if (image_ref_np[i] == 255):
                        FN = FN + 1
                    else:
                        TN = TN + 1

            # Calcul du pourcentage de TP, FP, TN, FN
            taille_labels = w*h
            TP = 100.0*(TP/taille_labels)
            FP = 100.0*(FP/taille_labels)
            TN = 100.0*(TN/taille_labels)
            FN = 100.0*(FN/taille_labels)

            # Calcul de la précision
            precision = TP / (TP + FP)

            # Calcul de la sensibilité
            sensibilite = TP / (TP + FN)

            # Calcul de la similarité
            similarite = 2*TP / (2*TP + FP + FN)

            print(precision)
            print(sensibilite)
            print(similarite)

if __name__ == '__main__':
    SegmentationTexture()