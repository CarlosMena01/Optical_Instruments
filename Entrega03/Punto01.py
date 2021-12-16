#Se imortan las librerías relevantes y las unidades
from resources.functions import *

#Se importa la imagen del lienzo
gala = cv2.imread('gala.jpg', 0)
print(gala)
#Se grafica el lienzo para determinar el tamaño de los macropixeles
fig1, axs = plt.subplots(1, 2, sharey=True)
Complex_Plot(gala,'A',0,axs[0],fig1)
axs[0].set_title('(a)')
axs[0].set_xlabel('1.48mm/píxel')
Complex_Plot(gala,'A',0,axs[1],fig1)
axs[1].set_title('(b)')
axs[1].set_xlabel('1.48mm/píxel')
