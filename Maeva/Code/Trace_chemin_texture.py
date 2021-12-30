import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.image import imread
import matplotlib.patches as patches
import cv2
import os
import skimage
from skimage import morphology

if __name__ == '__main__':

    exec(open("Interpolation.py").read())

    bool_segmentation = input("Texture a segmenter ? (O/N)")
    
    if (bool_segmentation == 'O') or (bool_segmentation == 'o'):
        exec(open("Segmentation.py").read())
    else:
        chemin_texture_non_seg = input("Entrez le chemin vers la texture souhaitee sur le chemin (.jpg):")

    # Rayon du chemin
    r = 80

    chemin_fond = input("Entrez le chemin vers la texture souhaitee pour le fond (.jpg):")


    ###### Elargissement du chemin
    chemin = Image.open("Images_intermediaires/Trace_chemin.jpg")
    image_file = chemin.convert('1')
    pixels_chemin = image_file.load()
    for i in range(chemin.size[0]):
        for j in range(chemin.size[1]):
            if (pixels_chemin[i,j] == 0):
                for i_change in range(i-r,i,1):
                    for j_change in range(j-r,j,1):
                        pixels_chemin[i_change,j_change] = 0
    image_file.save("Images_intermediaires/chemin_large.jpg")
    chemin_large = ImageOps.invert(Image.open("Images_intermediaires/chemin_large.jpg"))


    ###### Répétition de la texture de fond
    # Pour une texture réelle, exécuter d'abord ces commandes pour rendre la texture répétable:
    # pip3 install img2texture
    # img2texture /path/to/source.jpg /path/to/seamless.jpg 
    bg = Image.open(chemin_fond)
    bg_w, bg_h = bg.size
    new_im = Image.new('RGB', (3000,3000))
    w, h = new_im.size
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            new_im.paste(bg, (i, j))
    new_im.save("Images_intermediaires/Tile_fond.jpg")

    fond = new_im.resize((590,590))


    ###### Collage de la texture sur le chemin

    ###### 1er cas: texture non segmentée de type freeTexture15
    if (bool_segmentation == 'N') or (bool_segmentation == 'n'):
        texture_non_segmentee = Image.open(chemin_texture_non_seg)
        texture_non_segmentee = texture_non_segmentee.resize((590,590))

        mask_im = chemin_large
        mask_im = mask_im.resize((590,590))
        mask_im = mask_im.filter(ImageFilter.GaussianBlur(10))

        back_im = fond.copy()
        back_im.paste(texture_non_segmentee, (0,0), mask_im)
        back_im = back_im.crop((0,50,590,400))
        back_im.save('result.jpg', quality=100, subsampling=0)


    ###### 2ème cas: texture segmentée
    else:
        texture_segmentee = cv2.imread("Images_intermediaires/texture_segmentee_tile.jpg")
        grayImage = cv2.cvtColor(texture_segmentee, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite("Images_intermediaires/blackwhite_texture.jpg", blackAndWhiteImage)
        inverse = cv2.bitwise_not(blackAndWhiteImage)
        cv2.imwrite("Images_intermediaires/blackwhite_texture_inverse.jpg", inverse)

        # Copiage de la texture de fond dans le fond des pierres répétées
        # Cas 1: 
        # mask_im = Image.open('Images_intermediaires/blackwhite_texture_inverse.jpg')
        # Cas 2:
        mask_im = Image.open('Images_intermediaires/blackwhite_texture.jpg')
        mask_im = mask_im.resize((590,590))
        fond = fond.resize((590,590))
        texture_pierres_bis = Image.open('Images_intermediaires/Tile_pierres.jpg')
        texture_pierres_bis = texture_pierres_bis.resize((590,590))
        texture_pierres_bis.paste(fond, (0,0), mask_im)

        # Même étape que précédement (comme avec la texture non segmentée)
        texture_segmentee = texture_pierres_bis
        mask_im = chemin_large
        mask_im = mask_im.resize((590,590))
        back_im = fond.copy()
        back_im.paste(texture_segmentee, (0,0), mask_im)
        back_im = back_im.crop((0,50,590,590))

        ###### Correction des pierres coupées:

        # Répétition de la texture en noir et blanc:
        # Cas 1:
        # bg = Image.open("Images_intermediaires/blackwhite_texture_inverse.jpg")
        # Cas 2:
        bg = Image.open("Images_intermediaires/blackwhite_texture.jpg")
        bg_w, bg_h = bg.size
        new_im = Image.new('RGB', (3000,3000))
        w, h = new_im.size
        for i in range(0, w, bg_w):
            for j in range(0, h, bg_h):
                new_im.paste(bg, (i, j))

        # Suppression des pierres loin du chemin avec un masque:
        texture_segmentee_bw = new_im.resize((590,590))
        mask_im = chemin_large
        mask_im = mask_im.resize((590,590))
        back_im = Image.new('RGB', (590,590), (255,255,255))
        back_im.paste(texture_segmentee_bw, (0,0), mask_im)
        back_im.save('Images_intermediaires/collage_mask_pierres_chemin_bw.jpg', quality=100, subsampling=0)

        # Suppression des pierres au bord du chemin:
        mask_im.save('Images_intermediaires/mask_im.jpg', quality=100, subsampling=0)
        chemin_large = cv2.imread('Images_intermediaires/mask_im.jpg',0)
        (thresh, chemin_large) = cv2.threshold(chemin_large, 127, 255, cv2.THRESH_BINARY)
        test_supp_large = chemin_large
        pixels_chemin_large = test_supp_large
        test_supp_gray = cv2.imread('Images_intermediaires/collage_mask_pierres_chemin_bw.jpg',0)
        (thresh, test_supp) = cv2.threshold(test_supp_gray, 127, 255, cv2.THRESH_BINARY)
        pixels_supp = test_supp
        first = True
        new_pixels_supp = pixels_supp
        grid_labeled, num_labels = morphology.label(new_pixels_supp, background=255, connectivity=1, return_num=True)
        grid_labeled = grid_labeled.reshape((590,590))
        label_ij = []

        for i in range(590):
            for j in range(590):
                # Si on est sur un pixel-chemin large, à la frontière du chemin et qu'on se trouve sur une pierre
                if (pixels_chemin_large[i,j-1] == 0) and (pixels_chemin_large[i,j] != 0) and (first) and (new_pixels_supp[i,j] == 0):
                    new_pixels_supp[i,j] = 255
                    label_ij.append(grid_labeled[i,j])
                    first = False
            first = True
        # Suppression de toutes les traces des pierres au bord:
        unique_label = []
        for label in label_ij:
            if label not in unique_label:
                unique_label.append(label)
        for label in unique_label:
            for y in range(590):
                for x in range(590):
                    if (grid_labeled[y,x] == label):
                        new_pixels_supp[y,x] = 255

        img_flip = cv2.flip(new_pixels_supp, 1)
        pixels_chemin_large_flip = cv2.flip(pixels_chemin_large, 1)
        grid_labeled, num_labels = morphology.label(img_flip, background=255, connectivity=1, return_num=True)
        grid_labeled = grid_labeled.reshape((590,590))
        label_ij = []
        first = True
        for i in range(590):
            for j in range(590):
                # Si on est sur un pixel-chemin large, à la frontière du chemin et qu'on se trouve sur une pierre
                if (pixels_chemin_large_flip[i,j-1] == 0) and (pixels_chemin_large_flip[i,j] != 0) and (first) and (img_flip[i,j] == 0):
                    img_flip[i,j] = 255
                    label_ij.append(grid_labeled[i,j])
                    first = False
            first = True
        # Suppression de toutes les pierres au bord:
        unique_label = []
        for label in label_ij:
            if label not in unique_label:
                unique_label.append(label)
        for label in unique_label:
            for y in range(590):
                for x in range(590):
                    if (grid_labeled[y,x] == label):
                        img_flip[y,x] = 255
        
        img_flip_2 = cv2.flip(img_flip, 1)

        inverse = cv2.bitwise_not(img_flip_2)
        cv2.imwrite("Images_intermediaires/blackwhite_texture_cut_inverse.jpg", inverse)

        back_im = fond.copy()
        mask_im = Image.open('Images_intermediaires/blackwhite_texture_cut_inverse.jpg')
        back_im.paste(texture_segmentee, (0,0), mask_im)
        back_im = back_im.crop((0,50,590,450))
        back_im.save('result.jpg', quality=100, subsampling=0)
