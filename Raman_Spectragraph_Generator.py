import matplotlib.pyplot as plt
import numpy as np
import Raw_data_input as rdi
import pybaselines.whittaker as whit
from scipy.signal import savgol_filter



#File inputs
FileBackground = r"C:\Users\overh\OneDrive\Documents\Raman 4-29-25\baslinw25s.dat" #Input file path for background reading
FileRaman = r"C:\Users\overh\OneDrive\Documents\Raman 4-29-25\coal 25s.dat"  #Input file path for Raman reading

#Creating lists from file inputs
BackgroundRaw = np.transpose(np.loadtxt(FileBackground, skiprows = 4, dtype = int)[:,1:])[0].tolist()
RamanRaw = np.transpose(np.loadtxt(FileRaman, skiprows = 4, dtype = int)[:,1:])[0].tolist()

#Formatting the data
Raman = rdi.createList(RamanRaw)[33:3678]
Background = rdi.createList(BackgroundRaw)[33:3678]



def BaslineSubtration(Signal, BackgroundSignal):
    #Obtain baseline for background noise
    Baseline, Params = whit.arpls(BackgroundSignal) 
    for i in range(len(Signal)):
        Signal[i] = Signal[i] - Baseline[i]
    return Signal 

def ScaleSignal(Signal, Scale):
    newSignal=[]
    for i in range(len(Signal)):
        newSignal.append(Scale * Signal[i])
    return newSignal

def RemoveFlourescence(Signal):
    newSignal = []
    savSignal = savgol_filter(Signal, len(Signal), 1)
    for i in range(len(savSignal)):
        newSignal.append(Signal[i]-savSignal[i])
    return newSignal


if __name__ == "__main__":

    subSignal = BaslineSubtration(Raman, Background)
    scaledSubSignal = ScaleSignal(subSignal, 10)
    scaledSubSignalFiltered = savgol_filter(ScaleSignal(subSignal, 10), len(subSignal), 16, deriv = 0)

    smoothedSignal = savgol_filter(RemoveFlourescence(subSignal), len(subSignal), 15)
    noFlour = RemoveFlourescence(subSignal)
    
    x_axis = np.linspace(1, len(Raman), len(Raman))


    plt.plot(x_axis, subSignal, label = 'Raman w/ baseline subtraction')
    plt.plot(x_axis, scaledSubSignal, label = 'Scaled Raman')
    plt.plot(x_axis, RemoveFlourescence(subSignal))
    plt.plot(x_axis, ScaleSignal(smoothedSignal, 30), label = 'test')
    plt.plot(x_axis, savgol_filter(scaledSubSignal, len(scaledSubSignal), 32))
    # plt.ylim(ymin = 0)
    plt.xlim(xmin = 0)
    plt.legend()
    plt.show()