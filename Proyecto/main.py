from resources.functions import *

w_length=633*nm

bob=cv2.imread('bob.jpg',0)
fig1, axs = plt.subplots( sharey=False)
Complex_Plot(bob,'A',0,axs,fig1)
shape=np.shape(bob)
dx=5*um #tamaño de imagen al rededor de los 0.5cm

r1=Random_Phase_Plate(shape)
r2=Random_Phase_Plate(shape)

def Object_Arm(image,r1,r2,z1,z2,w_length,dx,C1):
    U1,dx1=Fresnel_Transform(C1*image*r1,z1,w_length,dx)
    UCCDo,dx2=Fresnel_Transform(U1*r2,z2,w_length,dx)
    
    return UCCDo,dx1,dx2

UCCDo,dx1,dx2=Object_Arm(bob,r1,r2,0.1,0.2,w_length,dx,1)

fig2, axs = plt.subplots( sharey=False)
Complex_Plot(UCCDo,'I',0,axs,fig2)