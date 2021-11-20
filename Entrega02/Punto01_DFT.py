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

""" A continuación se presenta un ejemplo del funcionamiento de la función de Espectro Angular via DFT
    para la difracción de una apertura circular de diametro 3mm a una distancia de 250mm, iluminando
    con luz de 650nm (ir al documento donde se compara el resultado con el resultado real) """

#Se crea computacionalmente la apertura circular (el diámetro se acomoda con las dimensiones de muestreo)
circ_aperture=np.zeros((500,500),dtype="uint8")
coordy=int(np.shape(circ_aperture)[0]/2)
coordx=int(np.shape(circ_aperture)[1]/2)
cv2.circle(circ_aperture,(coordx,coordy),150,1,-1)

#Se calcula el patrón de difracción por Espectro Angular
U_circ=Angular_Spectrum_DFT(circ_aperture,250*mm,650*nm,1e-5)
fig, axs = plt.subplots(1, 1, figsize=(10, 10))
Complex_Plot(U_circ,'A',0,axs)

""" Función de Difracción Discreta por Transformada de Fresnel usando DFTs"""
def Fresnel_Transform_DFT(matrix,z,w_length,dx0):
    # matrix es la representación discreta de la imagen o función 
    # z es la distancia de propagación (metros)
    # w_length es la longitud de onda (m)
    # dx0 es el intervalo de muestreo de la función en el plano de entrada

    #Se define la dimensión de la imagen (solo se utiliza N por ser cuadrada)
    N=np.shape(matrix)[0]

    #Se calcula dx, el intervalo de muestreo en el plano de salida
    dx=(w_length*z)/(dx0*N)

    #Se definen las coordenadas del plano de entrada con el fin de aplicar las fases esféricas de entrada
    k=(2*np.pi)/w_length
    x0=np.arange(-int(N/2),int(N/2),1)
    y0=np.arange(-int(N/2),int(N/2),1)
    n0,m0=np.meshgrid(x0,y0)

    #Se aplican las fases esféricas de entrada
    U_prima=matrix*np.exp((1j*k/(2*z))*((dx0*n0)**2+(dx0*m0)**2))

    #Se calcula la transformada de Fourier de la función imediatamente anterior
    U_2prima=DFT(U_prima)
    U_2prima=(dx**2)*U_2prima

    #Se definen las coordenadas del plano de salida con el fin de aplicar las fases esféricas de salida
    x=np.arange(-int(N/2),int(N/2),1)
    y=np.arange(-int(N/2),int(N/2),1)
    n,m=np.meshgrid(x,y)

    #Se aplican las fases esféricas de salida y se obtiene el campo difractado a un distancia z
    U_z=U_2prima*(1)*np.exp((1j*k/(2*z))*((dx*n)**2+(dx*m)**2))
    return U_z