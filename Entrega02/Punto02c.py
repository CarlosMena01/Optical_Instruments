#Se imortan las librerías relevantes y las unidades
from resources.functions import *

#Parámetros del sistema
N = 300 #Tamaño de la imagen
dx = 10*um #Tamaño de pixel
w_length = 650*nm #Longitud de onda
r = 80*dx
N_F = 25 #Número de zonas de Fresnel
z1 = (r**2)/(N_F*w_length)
z2 = (r**2)/((N_F +1)*w_length)

print(z1,z2)


#Calculamos la transmitancia
image = Mask_Circle(N, int(r/dx), kind= "O")

#Gráficamos
fig, axs = plt.subplots(1,3)

Complex_Plot(image,"A",0,axs[0], fig ,colbar= False)
Complex_Plot(Diffraction(image,z1,w_length,dx),"A",0,axs[1],fig, colbar= False)
Complex_Plot(Diffraction(image,z2,w_length,dx),"A",0,axs[2],fig, colbar= False)
axs[0].set_title("Rejilla circular")
axs[1].set_title("Difracción con " +str(N_F)+ "zonas de Fresnel")
axs[2].set_title("Difracción con"+str(N_F+1)+"zonas de Fresnel")

plt.show()