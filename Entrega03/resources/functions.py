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
    #shape dimensiones de la matriz (2-tupla)
    #r es el radio del circulo (en píxeles)
    #kind: 'A' si es una apertura, 'O' si es un obstáculo
    #coordx y coordy son las coordenadas del centro en el eje x y y respectivamente. Definidas en el centro de la imagen por defecto
    if (coordx==0):
        coordx=int(shape[1]/2)
    if (coordy==0):
        coordy=int(shape[0]/2)

    if (kind=='A'):
        circ_aperture=np.zeros(shape,dtype="uint8")
        cv2.circle(circ_aperture,(coordx,coordy),r,1,-1)
        return circ_aperture
    elif (kind=='O'):
        circ_obstacle=np.ones((N,N),dtype="uint8")
        cv2.circle(circ_obstacle,(coordx,coordy),r,0,-1)
        return circ_obstacle

#Función para gráficar matrices complejas 
def Complex_Plot(matrix,kind,log,axs,fig = 0, colbar = False):
  #matrix: matriz a gráficar
  #kind: I=Intensidad, A=Amplitud, P=Fase
  #log: 1 si se desea escala logarítmica 0 en caso contrario
  fig.set_cmap('gist_gray') #hacer la imagen en blanco y negro
  if (kind=='I'):
    matrix_to_plot=np.abs(matrix)**2
  elif (kind=='A'):
    matrix_to_plot=np.abs(matrix)
  elif (kind=='P'):
     matrix_to_plot=np.angle(matrix)
  if (log==1):
    image = axs.imshow(np.log(matrix_to_plot + 0.0000001))
  elif (log==0):
    image = axs.imshow(matrix_to_plot)
  if (colbar):
    fig.colorbar(image, ax = axs)
  return 