import numpy as np
import cv2


def merge_smooth(t1,t2):
    """ Fusion de textures smooth par moyenne """
    if not t1.shape == t2.shape:
        t2 = cv2.resize(t2,(t1.shape[0],t1.shape[1]))

    shape = (t1.shape[0],t1.shape[1])
    a = np.linspace(1,0,shape[0])
    b = np.linspace(0,1,shape[0])

    vm1 = np.repeat(np.expand_dims(a,axis=1),shape[1],axis=1)
    vm2 = np.repeat(np.expand_dims(b,axis=1),shape[1],axis=1)

    im = np.zeros(t1.shape)
    for i in range(t1.shape[2]):
        im[:,:,i] = np.multiply(vm1,t1[:,:,i]) + np.multiply(vm2,t2[:,:,i])

    return im
