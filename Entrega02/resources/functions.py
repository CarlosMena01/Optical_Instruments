import numpy as np
import matplotlib.pyplot as plt
import cv2

#Definimos unidades
nm = 1e-9
um = 1e-6
mm = 1e-3
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
    U_z=U_2prima*(np.exp(1j*k*z)/(1j*w_length*z))*np.exp((1j*k/(2*z))*((dx*n)**2+(dx*m)**2))
    return U_z

""" Función de Difracción Discreta por Espectro Angular usando FFTs"""
def Angular_Spectrum_FFT(T, z, wave_length, dx):
    #T := Transmitancia que entra al sistema
    #dx := Dimención del espació discreto
    #z := Distancia a propagar
    #wave_length := longitud de onda
    
    A_0 = (dx**2)*(np.fft.fftshift(np.fft.fftn(T)))
    
    N,M = np.shape(T)

    x = np.arange(-int(M/2),int(M/2),1)
    y = np.arange(-int(N/2),int(N/2),1)
    X,Y = np.meshgrid(x,y)
    
    fx = X*(1/(M*dx))
    fy = Y*(1/(N*dx))
    
    k = 2*np.pi/wave_length
    
    trans = np.exp(1j*k*z*np.sqrt(1-(wave_length**2)*(fx**2 + fy**2)))
    
    A_z = A_0*trans
    df=1/(N*dx)
    U_end = (df**2)*np.fft.ifftn(A_z)
    return U_end

""" Función de Difracción Discreta por Transformada de Fresnel usando FFTs"""
def Fresnel_Transform_FFT(matrix,z,w_length,dx0):
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
    U_2prima= np.fft.fftshift(np.fft.fftn(U_prima))
    U_2prima=(dx**2)*U_2prima

    #Se definen las coordenadas del plano de salida con el fin de aplicar las fases esféricas de salida
    x=np.arange(-int(N/2),int(N/2),1)
    y=np.arange(-int(N/2),int(N/2),1)
    n,m=np.meshgrid(x,y)

    #Se aplican las fases esféricas de salida y se obtiene el campo difractado a un distancia z
    U_z=U_2prima*(np.exp(1j*k*z)/(1j*w_length*z))*np.exp((1j*k/(2*z))*((dx*n)**2+(dx*m)**2))
    return U_z

#funcion general para calculo de la difraccion
def Diffraction(image, z, w_length, dx,type = "FFT"):
  N = np.shape(image)[0] 
  param = N*(dx**2)/w_length
  if z >= param:
    print("Tipo: Fresnel, parámetro: ", param)
    if type == "FFT":
      result = Fresnel_Transform_FFT(image,z,w_length,dx)
    elif type == "DFT": 
      result = Fresnel_Transform_DFT(image,z,w_length,dx)
    else:
      result = "ERROR, tipo equívocado"
  elif z < param:
    print("Tipo: Espectro Angular, parámetro: ", param)
    if type == "FFT":
      result = Angular_Spectrum_FFT(image,z,w_length,dx)
    elif type == "DFT": 
      result = Angular_Spectrum_DFT(image,z,w_length,dx)
    else:
      result = "ERROR, tipo equívocado"
  return result

