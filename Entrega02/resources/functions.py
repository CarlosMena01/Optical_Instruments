import numpy as np
import matplotlib.pyplot as plt
import cv2

#Definimos unidades
um = 10**(-6)
mm = 10**(-3)
m = 1

#Función para gráficar matrices complejas 
def Complex_Plot(matrix,kind,log,axs,fig = 0, colbar = False):
  #matrix: matriz a gráficar
  #kind: I=Intensidad, A=Amplitud, P=Fase
  #log: 1 si se desea escala logarítmica 0 en caso contrario
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

#Definimos el sistema 4F a partir de las funciones que ya teniamos definidas.
def Lenses4F(image,landa,f):
    Half01=Lenses2F(image,landa,f,1) #Usamos el método de dividir el sistema 4f en dos mitades.
    Half02=Lenses2F(Half01,landa,f,0)
    return Half02