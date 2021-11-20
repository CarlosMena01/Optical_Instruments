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

""" Función de Difracción Discreta por Espectro Angular usando DFTs"""
def Angular_Spectrum_DFT(matrix,z,w_length,dx):
    # matrix es la representación discreta de la imagen o función 
    # z es la distancia de propagación (metros)
    # w_length es la longitud de onda (m)
    # dx es el intervalo de muestreo de la función en el plano de entrada

    #Se define la dimensión de la imagen (solo se utiliza N por ser cuadrada)
    N=np.shape(matrix)[0]

    #Se calcula el intervalo de muestreo en el dominio de las frecuancias
    df=1/(dx*N)

    #Se calcula la transformada de Fourier de la imagen o función
    A_0=DFT(matrix)
    A_0=(dx**2)*A_0

    #Se definen las coordenadas frecuenciales con el fin de aplicar la función de transferencia
    #adecuadamente
    x=np.arange(-int(N/2),int(N/2),1)
    y=np.arange(-int(N/2),int(N/2),1)
    X,Y=np.meshgrid(x,y)
    fX=X*(1/(N*dx))
    fY=Y*(1/(N*dx))

    #Se aplica la función de transferencia
    A_z=A_0*np.exp(1j*z*(2*np.pi/w_length)*np.sqrt(1-(w_length**2)*(fX**2+fY**2)))      

    #Se calcula la transformada inversa de Fourier de A_z y se retorna (U_z es la representación del
    # camp óptico difractado a una distancia z) 
    U_z=DFT(A_z,'i')
    U_z=(df**2)*U_z
    return U_z