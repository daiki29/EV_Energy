#%%
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import pandas as pd
from tkinter import messagebox


def gastoEenergetico(V):
    pAire=1.1682
    aF = 7.182
    masaEv=3500
    masaBat=1700
    mCarga=2200
    mVeh = masaEv+masaBat+mCarga
    
    g = 9.81
    alfa = 0
    Cd = 0.6
    Cr = 0.01 #caucho alfato seco 
    nc = 0.95 #eta_conversion electrica
    Pe = np.zeros([len(V),1]) 
    a = np.gradient(V)    #a=dV/dt
    
    for i in range(len(V)):
        Fa = (pAire*aF*Cd*(V[i]*V[i]))/2 #m/s
        Fr = mVeh*Cr*g*np.cos(alfa)
        Fg = mVeh*g*np.sin(alfa)
        Ft = (mVeh*a[i])+Fa+Fr+Fg
        Pm = V[i]*Ft
        Pe[i] = (Pm/nc)*(1/1000)
        
        if (Pe[i]<0):
            Pe[i]=Pe[i]*0.6
    Cenergy=(np.cumsum(Pe))*(1/1000)  #integral Pelectrica
    return (Pe,Cenergy)

data=genfromtxt('CBDDrivingCycle.csv',delimiter=',', skip_header=1)
plt.style.use('_mpl-gallery')

t=data[:,0]
vel=data[:,1]
dist=np.trapz(vel*(1000/3600))
(Pele,Energy)=gastoEenergetico(vel*(1000/3600))
messagebox.showinfo(message=" %0.2f km" % (dist/1000), title="Recorrido Relizado")
messagebox.showinfo(message=" %0.2f kWH" % Energy[-1], title="Energia Consumida")

plt.rcParams["figure.autolayout"] = True
plt.subplot(311)
plt.plot(t ,vel, linewidth=2.0)
plt.xlabel("time[s]")
plt.ylabel("Velocity[km/h]")
plt.subplot(312)
plt.plot(t ,Pele, linewidth=2.0)
plt.xlabel("time[s]")
plt.ylabel("Power[kW]")
plt.subplot(313)
plt.plot(t ,Energy, linewidth=2.0)
plt.xlabel("time[s]")
plt.ylabel("Energy[kWh]")
plt.show()