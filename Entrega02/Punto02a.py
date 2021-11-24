#Se imortan las librerías relevantes y las unidades
from resources.functions import *

""" A continuación se presenta el analisis a los casos de difracción planteados """

#Parámetros del sistema
L = 0.2*mm
m = 30
N = 500 #Tamaño de la imagen
dx = 10*um #Tamaño de pixel
w_length = 650*nm #Longitud de onda
z = (L**2)/w_length

#Creamos nuestra cuadrícula 
x = np.arange(-N/2,N/2,1)
y = np.arange(-N/2,N/2,1)
X,Y = np.meshgrid(x,y)

X = X*dx
Y = Y*dx

#Calculamos la transmitancia
image = (1/2)*(1 + m* np.cos(2*np.pi * X/L))

#Gráficamos
fig, axs = plt.subplots(1, 3, sharey=True)

Complex_Plot(image,"A",0,axs[0])
Complex_Plot(Diffraction(image,z,w_length,dx),"A",0,axs[1])
Complex_Plot(Diffraction(image,z*1.3,w_length,dx),"A",0,axs[2])
print("Z: ",z,"L: ",L, "WL: ", w_length )
plt.show()