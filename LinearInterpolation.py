import numpy as np
import scipy
from scipy import interpolate
import matplotlib.pyplot as plt

def search(x,y,z):
	r = open("a" + str((5 * 10**x)) + "e" + str((5 * 10**y)) + "p" + str((5 * 10**z)) + ".txt","r")
	return r.read().strip('][').split(', ')[9]
	#kld_t[str(x) + ', ' + str(y) + ' p' + '50']

ran = 3
numvals = 7

ex,ey = np.mgrid[-ran:ran:7j,-ran:ran:7j]


#print(ex,ey)

cx = []
cy = []

for j,k in enumerate(ex):
	for a,b in enumerate(ex[j]):
		cx.append(ex[j][a])
		cy.append(ey[j][a])



c = list(zip(*(cx,cy)))

#print(c)

coor = []

for i in range(numvals):
	for j in c:
		coor.append(j)


for j,k in enumerate(ey[0]):
	for i in range(numvals ** 2):
		coor[i+((numvals ** 2) * j)] = coor[i+((numvals ** 2) * j)] + (k,)




#print(coor)
count = 0
for i in coor:
	count += 1

print (count)


fvals = []

for i in coor:
	r = search(i[0],i[1],i[2])
	fvals.append(float(r))

cx.clear()
cy.clear()

interp = scipy.interpolate.LinearNDInterpolator(coor, fvals)
print('y interpolation')
coor.clear()

R = []

for i in range(numvals):
	R.append(c[i][1])

print (R)

X = np.linspace(min(R), max(R))
Y = np.linspace(min(R), max(R))
Z = np.linspace(min(R), max(R))
X, Y, Z = np.meshgrid(X, Y, Z)
print('y grid')

#print (X, Y, Z)
plotvals = []


		
plotvals = interp(X, Y, Z)
#plotvals.append(fvals[j])
print('y grid interpolation')

X, Y = np.meshgrid(X, Y)

plt.figure()
plt.pcolormesh(X, Y, plotvals)
plt.colorbar()
plt.savefig('interptest.png')
plt.show()





