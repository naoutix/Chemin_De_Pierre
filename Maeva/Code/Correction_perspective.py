import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import copy
from PIL import Image

pts1 = np.zeros(4)

def click_event(event, x, y, flags, params):

    if (event == cv2.EVENT_LBUTTONDOWN):
        print(x, ' ', y)

#### Code utile pour connaître les coordonnées à utiliser pour pts1:
#texture = input("Chemin vers la texture dont la perspective doit etre corrigee: ")
#cv2.imshow('image', texture)
#cv2.setMouseCallback('image', click_event)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Si correction de la perspective d'une autre texture que Texture5, remplacer le chemin suivant ainsi que pts1:
texture = cv2.imread('Textures_reelles/Texture5.jpg')
rows,cols,ch = texture.shape

pts1 = np.float32([[62,17],[324,121],[2,209],[189,320]])
pts2 = np.float32([[0,0],[rows,0],[0,cols],[rows,cols]])

h, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC,5.0)
texture_persp = cv2.warpPerspective(texture, h, (cols*2, rows*2))

cv2.imwrite("Images_intermediaires/Correction_perspective.jpg", texture_persp)

# Tous les pixels au dessus de 3 sont considérés comme blancs
gray = cv2.imread("Images_intermediaires/Correction_perspective.jpg",0)
_, thresh_original = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY)

# Recherche des contours:
thresh = copy.copy(thresh_original)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

lst_contours = []
for cnt in contours:
    ctr = cv2.boundingRect(cnt)
    lst_contours.append(ctr)
x,y,w,h = sorted(lst_contours, key=lambda coef: coef[3])[-1]

# On retire les bords noires de l'image avec la nouvelle perspective:
texture_persp_crop = Image.open("Images_intermediaires/Correction_perspective.jpg")
persp_crop = texture_persp_crop.crop((0,0,w//2,h//2))
persp_crop.save("Textures_reelles/Correction_perspective_crop.jpg")