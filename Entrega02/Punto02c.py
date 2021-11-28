#Se imortan las librerías relevantes y las unidades
from resources.functions import *

#Parámetros del sistema
N = 600 #Tamaño de la imagen
dx = 10*um #Tamaño de pixel
w_length = 633*nm #Longitud de onda
r = 100 #píxeles

#Calculamos la transmitancia
image = Mask_Circle(N, r, kind= "O")

center = []
zs = []
#Hacemos el barrido de la intensidad del campo en el eje óptico para diferentes posiciones axiales
for z in range(1500,4000,1):
    zs.append(z*dx)
    mat = Diffraction(image,z*dx,w_length,dx)
    center.append(np.abs(mat[int(N/2)][int(N/2)]))
#Gráficamos
fig1, axs = plt.subplots()
plt.plot(zs,center)


fig2, axs = plt.subplots(2,5,sharey=True,sharex=True)
patterns=[]
for j in range(2500,3500,100):
    patterns.append(Diffraction(image,j*dx,w_length,dx))
axs[0][0].plot(range(0,600),np.abs(patterns[0][300]))
axs[0][1].plot(range(0,600),np.abs(patterns[1][300]))
axs[0][2].plot(range(0,600),np.abs(patterns[2][300]))
axs[0][3].plot(range(0,600),np.abs(patterns[3][300]))
axs[0][4].plot(range(0,600),np.abs(patterns[4][300]))
axs[1][0].plot(range(0,600),np.abs(patterns[5][300]))
axs[1][1].plot(range(0,600),np.abs(patterns[6][300]))
axs[1][2].plot(range(0,600),np.abs(patterns[7][300]))
axs[1][3].plot(range(0,600),np.abs(patterns[8][300]))
axs[1][4].plot(range(0,600),np.abs(patterns[9][300]))

axs[0][0].set_title('z=25mm')
axs[0][1].set_title('z=26mm')
axs[0][2].set_title('z=27mm')
axs[0][3].set_title('z=28mm')
axs[0][4].set_title('z=29mm')
axs[1][0].set_title('z=30mm')
axs[1][1].set_title('z=31mm')
axs[1][2].set_title('z=32mm')
axs[1][3].set_title('z=33mm')
axs[1][4].set_title('z=34mm')


fig3, axs = plt.subplots(1,1)
Complex_Plot(Diffraction(image,33*mm,w_length,dx),'A',0,axs[0],fig3)

plt.show()