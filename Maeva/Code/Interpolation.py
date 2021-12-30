import time

import numpy as np
import matplotlib.pyplot as plt

def InterpolationChemin():
    X = []
    Y = []
    P2DRAW = []
    pas = 1/100

    x2draw = []
    y2draw = []

    nbpointsutilisateur = input("Entrez le nombre de points souhaites sur le chemin:")

    ############# Sélection des points par l'utilisateur #############

    def tellme(s):
        print(s)
        plt.title(s, fontsize=16)
        plt.draw()

    plt.figure()
    plt.xlim(0, 10)
    plt.ylim(0, 10)

    tellme('Cliquez pour selectionner les points du chemin')

    plt.waitforbuttonpress()

    while True:
        pts = []
        while len(pts) < 3:
            tellme('Selectionnez vos points')
            pts = np.asarray(plt.ginput(int(nbpointsutilisateur), timeout=-1))
            X.append(pts[:,0])
            Y.append(pts[:,1])
            if len(pts) < 3:
                tellme('Encore un point')
                time.sleep(1)

        tellme('Clavier pour valider, souris pour recommencer')

        if plt.waitforbuttonpress():
            break


    ############# Interpolation de Lagrange #############

    def buildParametrisationReguliere(nbElem, pas):
            #Vecteur des pas temporels
            T = []
            #Echantillonage des pas temporels
            tToEval = []

            #Construction des pas temporels
            for i in range(nbElem):
                T.append(i)
            #Construction des échantillons
            cpt = 1
            tToEval.append(min(T))
            while tToEval[-1] < max(T):
                tToEval.append(min(T) + cpt*pas)
                cpt = cpt + 1

            return (T, tToEval)

    def lagrange(x, X, Y):
        Li = 1.0
        Pn = 0.0
        for i in range(len(X)):
            for j in range(len(X)):
                if j != i:
                    Li = Li*((x - X[j]) / (X[i] - X[j]))
            Pn = Pn + Li*Y[i]
            Li = 1.0
        return Pn

    def applyLagrangeParametrisation(X, Y, T, tToEval):
        for i in range(len(tToEval)):
            # Calcul de xpoint et ypoint
            xpoint = lagrange(tToEval[i], T, X)
            ypoint = lagrange(tToEval[i], T, Y)
            x2draw.append(xpoint)
            y2draw.append(ypoint)

    plt.close()

    (T, tToEval) = buildParametrisationReguliere(len(X[0]), pas)
    applyLagrangeParametrisation(X[0], Y[0], T, tToEval)

    plt.plot(np.array(x2draw), np.array(y2draw))
    plt.axis("off")
    plt.savefig("Images_intermediaires/Trace_chemin.jpg")
    plt.show()

if __name__ == '__main__':
    InterpolationChemin()