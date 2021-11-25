#Se imortan las librerías relevantes y las unidades
from resources.functions import *

""" A continuación se presenta el analisis a los casos de difracción planteados """

#Parámetros del sistema
L = 100*um
m = 1
N = 600 #Tamaño de la imagen
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
fig, axs = plt.subplots(1, 3)

Complex_Plot(image,"A",0,axs[0], fig ,colbar= False)
Complex_Plot(Diffraction(image,z*4,w_length,dx),"A",0,axs[1],fig, colbar= False)
Complex_Plot(Diffraction(image,z*5,w_length,dx),"A",0,axs[2], fig,colbar= False)

axs[0].set_title("Imagen original")
axs[1].set_title("Difracción con N=4")
axs[2].set_title("Difracción con N=5")
plt.show()