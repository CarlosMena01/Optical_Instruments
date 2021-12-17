#Se imortan las librerías relevantes y las unidades
from matplotlib.pyplot import show
from resources.functions import *

#Importamos el holograma
root = "resources/" 
file_name = "Hologram.tiff"
Hologram = cv2.imread(root + file_name, 0)
shape = np.shape(Hologram) #Dimensión del arreglo

#Espectro de fourier
Hologram_Fourier = np.fft.fftshift(np.fft.fftn(Hologram))
#Definimos las condiciones para la primer gráfica
fig, axs = plt.subplots(1, 2, sharey=True)
Complex_Plot(Hologram,'I',0,axs[0], fig)
Complex_Plot(Hologram_Fourier,'I',1,axs[1], fig)
axs[0].set_title("Holograma")
axs[1].set_title("Espectro de frecuencias \n en escala logaritmica")
plt.show()

#Creamos un filtro para guardar la información de interés
r = 400 #Radio de los circulos 
coor1=[1726,576] #Coordenadas donde se encuentra la información de interes 
Filter = Mask_Circle(shape, r, "A", coor1[0],coor1[1])

#Obtenemos la imagen filtrada
obj = np.fft.ifftn(Hologram_Fourier*Filter)

#Propagamos la imagen
z = 73*mm
landa = 633*nm
dx = (6513/2048)*um
obj_final = Diffraction(obj,z,landa,dx)
#Definimos las condiciones para la primer gráfica
fig, axs = plt.subplots( sharey=True)
Complex_Plot(obj_final, "A",0,axs)
axs.set_title("Imagen reconstruida")
axs.set_xlabel("{} um/pixel".format(round(dx/um,2)))
plt.show()
