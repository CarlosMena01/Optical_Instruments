#Importamos todas las librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Función para calcular la formación de imgenes de una lente en el plano focal si el objeto está en el otro plano focal
def Lenses2F(image,landa,f,shift):
  #shift=1 Se hace el shift
  #shift=0 No se hace el shift
  #Como vimos, para la segunda parte del sistema el shift no es necesario
  if (shift==1):
    result = (-1j/(landa*f))*(np.fft.fftshift(np.fft.fftn(image)))
  elif (shift==0):
    result = (-1j/(landa*f))*(np.fft.fftn(image))
  return result

