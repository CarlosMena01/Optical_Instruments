#Importamos todas las librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Función para calcular la formación de imgenes de una lente en el plano focal si el objeto está en el otro plano focal
def Lenses2F(image,landa=1,f=1,shift=0):
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

#Importamos la imagen a corregir
b=cv2.imread('puntob.png',0)

#Hacemos pasar la imagen por la primera parte del sistema
fft_b=Lenses2F(b,landa=1,f=1,shift=1)

#Se hace la máscara con la cual se filtrarán las frecuencias en el plano de Fourier
mask=np.ones(np.shape(b),dtype="uint8")
cv2.circle(mask,(396,367),5,0,-1)
cv2.circle(mask,(372,401),5,0,-1)

#Se hace pasar la información del plano de Fourier por la segunda parte del sistema, aplicando el filtro
b_filt=Lenses2F(fft_b*mask,landa=1,f=1,shift=0)

#Se muestra la imagen original, La información de Frecuencias con el filtro y la imagen corregida
fig, axs = plt.subplots(1, 3, figsize=(10, 5), sharey=True)
Complex_Plot(b ,'A',0,axs[0])
axs[0].set_title("Imagen con Ruido")
Complex_Plot(fft_b ,'A',1,axs[1])
axs[1].set_title("Plano Fourier con Filtro")
Complex_Plot(b_filt,'A',0,axs[2])
axs[2].set_title("Imagen Corregida")