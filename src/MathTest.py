import numpy as np
import matplotlib.pyplot as plt

point=10000
x0,y0=0,0
r=1
count=0

plt.figure()
plt.title('Monte Carlo Simulation of Pi')
plt.xlabel('x')
plt.ylabel('y')

for i in range(point):
    x=np.random.uniform(x0-r,x0+r)
    y=np.random.uniform(y0-r,y0+r)
    if (x-x0)**2+(y-y0)**2<=r**2:
        count+=1
        plt.plot(x,y,'ro',markersize=0.5)  # Point inside the circle
    else:
        plt.plot(x,y,'bo',markersize=0.5)  # Point outside the circle

plt.axis('equal')
plt.show()

pi_estimate=4*count/point
print(f'Estimated value of Pi: {pi_estimate}')