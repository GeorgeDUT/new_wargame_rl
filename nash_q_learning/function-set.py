from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy


def move(P,steps,sets):
    x,y=P
    a,b,c,d=sets
    dx=a*x+b*x
    dy=c*x+d*x
    return [x+dx*steps,y+dy*steps]

sets=[0,0,0,1]
t=np.arange(-30,30,0.01)
P0=[0.5,0.5]
P=P0
d=[]
for v in t:
    P=move(P,0.001,sets)
    d.append(P)

dnp=np.array(d)


fig=plt.figure()
plt.plot(d)
plt.show()