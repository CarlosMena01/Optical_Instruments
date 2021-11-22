#Se imortan las librerías relevantes y las unidades
from resources.functions import *

""" A continuación se presenta un ejemplo del funcionamiento de la función de Espectro Angular via DFT
    para la difracción de una apertura circular de diametro 3mm a una distancia de 250mm, iluminando
    con luz de 650nm (ir al documento donde se compara el resultado con el resultado real) """

#Se crea computacionalmente la apertura circular (el diámetro se acomoda con las dimensiones de muestreo)
circ_aperture=np.zeros((500,500),dtype="uint8")
coordy=int(np.shape(circ_aperture)[0]/2)
coordx=int(np.shape(circ_aperture)[1]/2)
cv2.circle(circ_aperture,(coordx,coordy),150,1,-1)

#Se calcula el patrón de difracción por Espectro Angular
U_circ=Diffraction(circ_aperture,60*mm,650*nm,1e-5, type = "DFT")
fig, axs = plt.subplots(1, 1, figsize=(10, 10))
Complex_Plot(U_circ,'A',0,axs)
plt.show()
