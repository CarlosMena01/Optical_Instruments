from resources.functions import *

w_length=633*nm

bob=cv2.imread('resources/bob.jpg',0)
Complex_Plot(bob,'A',0, plt)
beso=cv2.imread('resources/beso.jpg',0)
Complex_Plot(beso,'A',0, plt)
shape=np.shape(bob)
dx=5*um #tamaño de imagen al rededor de los 0.5cm

r1=Random_Phase_Plate(shape)
r2=Random_Phase_Plate(shape)

def Object_Arm(image,r1,r2,z1,z2,w_length,dx,C1):
    U1,dx1=Fresnel_Transform(C1*image*r1,z1,w_length,dx)
    UCCDo,dx2=Fresnel_Transform(U1*r2,z2,w_length,dx)
    
    return UCCDo,dx1,dx2

UCCDo,dx1,dx2=Object_Arm(beso,r1,r2,0.1,0.2,w_length,dx,1)

fig2, axs = plt.subplots( sharey=False)
Complex_Plot(UCCDo,'I',0,axs,fig2)

def Host_Arm(host, phase, NDF2, z3, w_length, dx0):
    imageh = NDF2*host*(np.sin(phase) + 1j*np.cos(phase))
    UCCD_host, dxf = Fresnel_Transform(imageh,z3,w_length,dx0)

    return UCCD_host, dxf

UCCD,dx1,dx2=Object_Arm(bob,r1,r2,0.1,0.2,w_length,dx,1)

UCCD_host, dx3 = Host_Arm(bob, np.pi, 1, 0.3, w_length, dx)

Complex_Plot(UCCD,'I',0, plt)
