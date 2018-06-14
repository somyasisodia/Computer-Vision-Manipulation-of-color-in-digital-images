import cv2
import numpy as np
import sys

if(len(sys.argv) != 7) :
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

cv2.imshow("input image: " + name_input, inputImage)

rows, cols, bands = inputImage.shape # bands == 3
W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))

# The transformation should be based on the
# historgram of the pixels in the W1,W2,H1,H2 range.
# The following code goes over these pixels

tmp = np.copy(inputImage)
#cv2.imshow('tmp', tmp)

# end of example of going over window

Lmax=0
Lmin=999

for i in range(H1, H2) :
	for j in range(W1, W2) :
		b, g, r = inputImage[i, j]
		nlb=b/255
		nlg=g/255
		nlr=r/255
		
		if (nlb<0.03928):
			lb=nlb/12.92
		else:
			lb=pow(((nlb+0.055)/1.055),2.4)
			
			
		if (nlg<0.03928):
			lg=nlg/12.92
		else:
			lg=pow(((nlg+0.055)/1.055),2.4)
		
		if (nlr<0.03928):
			lr=nlr/12.92
		else:
			lr=pow(((nlr+0.055)/1.055),2.4)
			
			
		x=((0.412453*lr) + (0.35758*lg) + (0.180423*lb))
		y=((0.212671*lr) + (0.71516*lg) + (0.072169*lb))
		z=((0.019334*lr) + (0.119193*lg) + (0.950227*lb))
		
		uw=(4*0.95)/(0.95+(15*1.0)+(3*1.09))
		vw=(9*1.0)/(0.95+(15*1.0)+(3*1.09))
		
		#t=y/Yw=1.0, (Xw, Yw, Zw)=(0.95, 1.0, 1.09)
		t=y/1.0
		if (t>0.008856):
			L=(116*(pow(t,(1/3))))-16.0
		else:
			L=903.3*t
		L=round(L)	
		if(L>Lmax):
			Lmax=L
			
		if(L<Lmin):
			Lmin=L
			
		d=x+(15*y)+(3*z)
		if (d==0.0):
			u_dash=0.0
			v_dash=0.0
		else:
			u_dash=(4*x)/d
			v_dash=(9*y)/d
		
		
		u=13*L*(u_dash-uw)
		v=13*L*(v_dash-vw)
		
		#if (L>100.0):
		#	print(L)
			
#print("Lmin : "+str(Lmin)+" Lmax : "+str(Lmax))
#Complete till BGR to Luv
#Now we have got the Lmax and Lmin values to be used for the entire image
#To display the image back, we need to convert it back to BGR



outputImage = np.zeros([rows, cols, bands], dtype=np.uint8)


for i in range(0, rows) :
	for j in range(0, cols) :
		b, g, r = inputImage[i, j]
		#print(str(b)+" :"+str(g)+" : "+str(r))
		nlb=b/255
		nlg=g/255
		nlr=r/255
		#print(str(nlb)+" :"+str(nlg)+" : "+str(nlr))
		
		if (nlb<0.03928):
			lb=nlb/12.92
		else:
			lb=pow(((nlb+0.055)/1.055),2.4)
		
		if (nlg<0.03928):
			lg=nlg/12.92
		else:
			lg=pow(((nlg+0.055)/1.055),2.4)
		
		if (nlr<0.03928):
			lr=nlr/12.92
		else:
			lr=pow(((nlr+0.055)/1.055),2.4)
		
		#print(str(lb)+" :"+str(lg)+" : "+str(lr))		
			
		x=((0.412453*lr) + (0.35758*lg) + (0.180423*lb))
		y=((0.212671*lr) + (0.71516*lg) + (0.072169*lb))
		z=((0.019334*lr) + (0.119193*lg) + (0.950227*lb))
		
		#print(str(x)+" :"+str(y)+" : "+str(z))
		
		uw=(4*0.95)/(0.95+(15*1.0)+(3*1.09))
		vw=(9*1.0)/(0.95+(15*1.0)+(3*1.09))
		
		#t=y/Yw=1.0, (Xw, Yw, Zw)=(0.95, 1.0, 1.09)
		t=y/1.0
		#print(str(uw)+" :"+str(vw)+" : "+str(t))
		if (t>0.008856):
			L=(116*(pow(t,(1/3))))-16.0
		else:
			L=903.3*t
		L=round(L)
			
		if(L>=Lmax):
			L=100.0
			
		if(L<=Lmin):
			L=0.0
			
		d=x+(15*y)+(3*z)
		if (d==0.0):
			u_dash=0.0
			v_dash=0.0
		else:
			u_dash=(4*x)/d
			v_dash=(9*y)/d
		u=13*L*(u_dash-uw)
		v=13*L*(v_dash-vw)
		
		
		#if (L<0 or u<0 or v<0):
		#	print(str(L)+" :"+str(u)+" : "+str(v))
		
		#if (L>100 or L<0):
		#	print(L)
#Complete till BGR to Luv
#Now we have got the Lmax and Lmin values to be used for the entire image
#To display the image back, we need to convert it back to BGR
		den=13*L
		nom1=u+(13*uw*L)
		nom2=v+(13*vw*L)
		if(den==0.0):
			u_star=nom1
			v_star=nom2
		else:
			u_star=nom1/den
			v_star=nom2/den
		#print(str(u_star)+" :"+str(v_star))
#Need to find out what Yw is
#t=y/Yw=1.0, (Xw, Yw, Zw)=(0.95, 1.0, 1.09)
		if (L>7.9996):
			Y=(pow(((L+16)/116), 3))*1.0
		else:
			Y=(L/903.3)*1.0
			
		if (v_star==0.0):
			X=0
			Z=0
		else:
			X=(Y*2.25*u_star)/v_star
			Z=(Y*(3-0.75*u_star-5*v_star))/v_star
			
		#if (X<0 or Y<0 or Z<0):
		#	print(str(X)+" :"+str(Y)+" : "+str(Z))
			
		Rs=(3.240479*X)+((-1.53715)*Y)+((-0.498535)*Z)
		Gs=((-0.969256)*X)+(1.875991*Y)+(0.041556*Z)
		Bs=(0.055648*X)+((-0.204043)*Y)+(1.057311*Z)
		
		#if (Rs<0 or Gs<0 or Bs<0):
		#	print(str(Rs)+" :"+str(Gs)+" : "+str(Bs))
		#print(str(Rs)+" :"+str(Gs)+" : "+str(Bs))
		
		if (Rs<0.00304):
			Rl=12.92*Rs
		else:
			Rl=(1.055*pow(Rs,(1/2.4)))-0.055
			
		if (Gs<0.00304):
			Gl=12.92*Gs
		else:
			Gl=(1.055*pow(Gs,(1/2.4)))-0.055
			
		if (Bs<0.00304):
			Bl=12.92*Bs
		else:
			Bl=(1.055*pow(Bs,(1/2.4)))-0.055
			
		#if (Rl<0 or Gl<0 or Bl<0):
		#	print(str(Rl)+" :"+str(Gl)+" : "+str(Bl))
		#print(str(Rl)+" :"+str(Bl)+" : "+str(Gl))
			
		r=Rl*255.0
		g=Gl*255.0
		b=Bl*255.0
		#if (r<0 or g<0 or r<0):
		#	print(str(b)+" :"+str(g)+" : "+str(r))
		outputImage[i,j] = [b, g, r]
		
cv2.imshow("output:", outputImage)
cv2.imwrite(name_output, outputImage);


# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()