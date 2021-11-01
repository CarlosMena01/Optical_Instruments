#Importamos todas las librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Función para calcular la formación de imgenes de una lente en el plano focal si el objeto está en el otro plano focal
def Lenses2F(image,landa,f):
  result = (-1j/(landa*f))*np.fft.fftshift(np.fft.fftn(image))
  return result
