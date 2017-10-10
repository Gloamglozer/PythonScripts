# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:58:21 2016

@author: Eric
"""
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math

### Setting Constants 
side = 6 
delta = .1
gridsize = int(side/delta)
A = "Reflection based fall off" # fall off rate when exponential term is active
B = 2*np.pi/(3/((2*0 + 1)/2)) #frequency (wavelength in denominator)
ExpFallOff = False

### Choosing between reflection based and distance based wave falloff
if(ExpFallOff == True):
    def falloff(m,n,x,y):
        return np.exp(A*math.sqrt((x+m)**2 + (y+n)**2))
elif(ExpFallOff == False):
    def falloff(m,n,x,y):
        return (1/(.1*(abs(m)+abs(n))+1))
        
### Function that takes nth values of X and Y matrices and gives corresponding height
def chladniplate(x,y):
    zdeltlist = []
    oldz = 0 
    z = 0
    
    for t in np.arange(0,1.3,.2):
        oldz = z
        z = 0 
        for m in range (-9,10,3):
            for n in range(-9,10,3): #Exponent fall off factor: np.exp(A*math.sqrt((x+m)**2 + (y+n)**2))*
                    z += falloff(m,n,x,y)*np.cos(B*math.sqrt((x+m)**2 + (y+n)**2)+2*np.pi*t)
        if t > 0:
            zdeltlist.append(abs(z-oldz))
            
    return np.average(zdeltlist)

x = y = np.arange(float(-side/2), float(side/2), delta)
X, Y = np.meshgrid(x, y)
Z = np.empty([gridsize,gridsize])
for i in range(0,gridsize):
    for j in range(0,gridsize):
        Z[i][j] = chladniplate(X[i][j],Y[i][j])

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111, projection='3d')

#wireframe
"""ax.plot_wireframe(X,Y,Z, rstride=1, cstride=1)

plt.show()"""

### Setting up Surface Plot 
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.title("A={}\n Wavelength={}".format(A,(2*np.pi/B)))
ax.view_init(elev=90.,azim=0)

plt.show()

