#Se imortan las librerías relevantes y las unidades
from resources.functions import *
"""Función que implementa la transformada discreta de Fourier bidimensional de forma matricial
(para imágenes cuadradas)"""
def DFT(matrix, inverse=False):
    # matrix es la representación discreta de la imagen o función 
    # inverse = True (transformada inversa de fourier) ; inverse = False (transformada de Fourier)

    #Se define la dimensión de la imagen (solo se utiliza N por ser cuadrada)
    N=np.shape(matrix)[0]

    #Se define el signo del kernel de la transformada, dependiendo si es inversa o no
    if (inverse):
        w=np.exp(1j*2*np.pi/N)
    else:
        w=np.exp(-1j*2*np.pi/N)
    
    # Se calcula la matriz W (cuyo origen se especifica en el informe)
    W=np.zeros(np.shape(matrix),dtype="complex_")
    for p in range(N):
        for q in range(N):
            W[p][q]=(w)**(p*q)
    
    #Se calcula la transformada de Fourier discreta en su forma matricial (F=W.matrix.W)
    F=np.matmul(W,matrix)
    F=np.matmul(F,W)

    #Se retorna F sin shift si es la transformada inversa (teniendo en cuenta que la matriz viene de un
    #proceso previo de trnasformada de Fourier en el cual se ha aplicado el shift)
    if (inverse):
        return F
    else:
        return np.fft.fftshift(F)