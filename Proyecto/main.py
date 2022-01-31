from resources.functions import *

w_length=633*nm

bob=cv2.imread('Proyecto/resources/bob.jpg',0)
Complex_Plot(bob,'A',0, plt)
plt.show()
beso=cv2.imread('Proyecto/resources/beso.jpg',0)[28:928,200:1100]
Complex_Plot(beso,'A',0, plt)
plt.show()
shape=np.shape(bob)
dx=5*um #tamaño de imagen al rededor de los 0.5cm

r1=Random_Phase_Plate(shape)
r2=Random_Phase_Plate(shape)

def Object_Arm(image,r1,r2,z1,z2,w_length,dx,C1):
    U1,dx1=Fresnel_Transform(C1*image*r1,z1,w_length,dx)
    UCCDo,dx2=Fresnel_Transform(U1*r2,z2,w_length,dx)
    
    return UCCDo,dx1,dx2

def Host_Arm(host, phase, NDF2, z3, w_length, dx0):
    imageh = NDF2*host*np.exp(1j*phase)
    UCCD_host, dxf = Fresnel_Transform(imageh,z3,w_length,dx0)

    return UCCD_host, dxf

UCCD,dx1,dx2=Object_Arm(beso,r1,r2,0.1,0.2,w_length,dx,0.00001)

UCCD_host, dx3 = Host_Arm(bob, np.pi, 1, 0.3, w_length, dx)

Complex_Plot(UCCD+UCCD_host,'I',0, plt)
plt.show()

host=Inverse_Fresnel_Transform(UCCD+UCCD_host,0.3,w_length,dx3)
Complex_Plot(host,'I',0,plt)
plt.show()


##################### PHASE SHIFTING ###########################

U_host0,dx_h0= Host_Arm(bob, 0, 1, 0.3, w_length, dx)
U_host90,dx_h90= Host_Arm(bob, np.pi/2, 1, 0.3, w_length, dx)
U_host180,dx_h180= Host_Arm(bob, np.pi, 1, 0.3, w_length, dx)

PW=PlaneWave(900,900,np.pi/2,np.pi/2,dx,dx,w_length)
Complex_Plot(PW,'P',0,plt)
plt.show()

I0=np.abs(U_host0+PW)**2
I90=np.abs(U_host90+PW)**2
I180=np.abs(U_host180+PW)**2

host_phase=np.angle(PW)+np.arctan2((2*I90-I0-I180),(I180-I0))
host_amplitude=np.sqrt((1/2)*(I0+I180)-np.abs(PW)**2)


Complex_Plot(U_host0,'P',0,plt)
plt.show()

U_host_rec=host_amplitude*np.exp(1j*host_phase)
Complex_Plot(U_host_rec,'P',0,plt)
plt.show()

bob_rec=Inverse_Fresnel_Transform(U_host_rec,0.3,w_length,dx_h0)
Complex_Plot(bob_rec,'A',0,plt)
plt.show()

############################# DECRYPTION ###########################################3

U_host0,dx_h0= Host_Arm(bob, 0, 1, 0.3, w_length, dx)
U_host90,dx_h90= Host_Arm(bob, np.pi/2, 1, 0.3, w_length, dx)
U_host180,dx_h180= Host_Arm(bob, np.pi, 1, 0.3, w_length, dx)

UCCD,dx1,dx2=Object_Arm(beso,r1,r2,0.1,0.2,w_length,dx,1)

I0=np.abs(UCCD+U_host0)**2
I90=np.abs(UCCD+U_host90)**2
I180=np.abs(UCCD+U_host180)**2

obj_phase=np.angle(U_host0)-np.arctan2((2*I90-I0-I180),(I180-I0))
obj_amplitude=np.sqrt(1/2*(I0+I180)-np.abs(U_host0)**2)

object_rec=obj_amplitude*np.exp(1j*obj_phase)

o1=Inverse_Fresnel_Transform(object_rec,0.2,w_length,dx2)
o1=o1*np.conjugate(r2)
object_dec=Inverse_Fresnel_Transform(o1,0.1,w_length,dx1)
object_dec=object_dec*np.conjugate(r1)

Complex_Plot(np.fft.fftshift(object_dec),'A',0,plt)
plt.show()