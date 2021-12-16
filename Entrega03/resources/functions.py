import numpy as np
import matplotlib.pyplot as plt
import cv2

#Definimos unidades
nm = 1e-9
um = 1e-6
mm = 1e-3
m = 1

#Función para crear rejillas circulares con diferentes coordenadas y tamaños
def Mask_Circle(shape,r,kind='A',coordx=0,coordy=0):

    #N dimensión de la matriz
    #r es el radio del circulo (en píxeles)
    #kind: 'A' si es una apertura, 'O' si es un obstáculo
    if (coordx==0):
        coordx=int(shape[1]/2)
    elif (coordy=0):
        coordy=int(shape[0]/2)

    if (kind=='A'):
        circ_aperture=np.zeros(shape,dtype="uint8")
        
        coordx=int(np.shape(circ_aperture)[1]/2)
        cv2.circle(circ_aperture,(coordx,coordy),r,1,-1)
        return circ_aperture
    elif (kind=='O'):
        circ_obstacle=np.ones((N,N),dtype="uint8")
        coordy=int(np.shape(circ_obstacle)[0]/2)
        coordx=int(np.shape(circ_obstacle)[1]/2)
        cv2.circle(circ_obstacle,(coordx,coordy),r,0,-1)
        return circ_obstacle