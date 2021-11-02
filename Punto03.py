#Importamos todas las librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Función para calcular la formación de imgenes de una lente en el plano focal si el objeto está en el otro plano focal
def Lenses2F(image,landa,f,shift):
  #image: Imagen que se ubica en el foco del plano objeto y pasará por la lente 
  #landa: Longitud de onda de la luente de luz que ingresa al sistema
  #f: distancia focal de la lente
  #shift: 0 si no se desea realizar un fftshit a la matriz y 1 en caso contrario
  if (shift==1):
    result = (-1j/(landa*f))*(np.fft.fftshift(np.fft.fftn(image)))
  elif (shift==0):
    result = (-1j/(landa*f))*(np.fft.fftn(image))
  return result

#Función para gráficar matrices complejas 
def Complex_Plot(matrix,kind,log,axs):
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
    axs.imshow(np.log(matrix_to_plot + 0.0000001))
  elif (log==0):
    axs.imshow(matrix_to_plot)
  return 

#Función para gráficar todo el sistema 4F
def All_system(image,landa,f,kind):
  #image: Imagen que se ubica en el foco del plano objeto y pasará por la lente 
  #landa: Longitud de onda de la luente de luz que ingresa al sistema
  #f: distancia focal de la lente
  #kind: I=Intensidad, A=Amplitud, P=Fase
  fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
  Complex_Plot(image ,kind,0,axs[0])
  axs[0].set_title("Imagen inicial")
  Complex_Plot(Lenses2F(image,landa,f,1) ,kind,1,axs[1])
  axs[1].set_title("Primera lente escala log")
  Complex_Plot(Lenses2F(Lenses2F(image,landa,f,1),landa,f,0) ,kind,0,axs[2])
  axs[2].set_title("Imagen final")
  return

#Definimos unidades
um = 10**(-6)
mm = 10**(-3)
m = 1

#Definimos los parametros y la imagen 
root = ""
filename = "red_heart.jpg"
image = cv2.imread(root + filename, 0)
landa = 0.66*um
f = 2*m

All_system(image, landa, f, "A")
