from resources.functions import *

w_length=633*nm

bob=cv2.imread('bob.jpg',0)
Complex_Plot(bob,'A',0)
shape=np.shape(bob)
dx=5*um #tamaño de imagen al rededor de los 0.5cm

r1=Random_Phase_Plate(shape)
r2=Random_Phase_Plate(shape)

def Object_Arm(image,r1,r2,z1,z2,w_length,dx,C1):
    U1,dx1=Fresnel_Transform(C1*image*r1,z1,w_length,dx)
    UCCD,dx2=Fresnel_Transform(U1*r2,z2,w_length,dx)
    
    return UCCD,dx1,dx2

UCCD,dx1,dx2=Object_Arm(bob,r1,r2,0.1,0.2,w_length,dx,1)
Complex_Plot(UCCD,'I',0)