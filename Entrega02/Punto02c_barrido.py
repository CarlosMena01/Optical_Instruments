#Se imortan las librerías relevantes y las unidades
from resources.functions import *

#Parámetros del sistema
N = 300 #Tamaño de la imagen
dx = 10*um #Tamaño de pixel
w_length = 650*nm #Longitud de onda
r = 80*dx

#Calculamos la transmitancia
image = Mask_Circle(N, int(r/dx), kind= "O")

center = []
zs = []
#Hacemos el barrido
for z in range(0,3000,1):
    zs.append(z)
    mat = Diffraction(image,z*dx,w_length,dx)
    center.append(np.abs(mat[int(N/2)][int(N/2)]))
#Gráficamos
fig, axs = plt.subplots()

plt.plot(zs,center)

plt.show()