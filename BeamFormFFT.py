import os
import os.path
import math
import numpy as np
import pylab
from matplotlib import pyplot as plt
from numpy.fft import fft, fftshift
#from UdpRecv import ArrayData
#from UdpRecv import ArrayDataLock
import time
import multiprocessing

outData = 0.000

def GetTimeinMilliSec():
    milli_sec = int(round(time.time() * 1000));
    return milli_sec;
    
    
def Calc_Power_From_NetworkMP(QuPut, QuGet, QuDly, hanWin, DataSize, NumArr, SamplingRate):
    
    while True:
        Xsnr = np.zeros(DataSize, dtype = np.int16)
        d1 = GetTimeinMilliSec()
        
        inpDataAllArray = QuPut.get();
        delay = QuDly.get();

        i = inpDataAllArray[DataSize];

        
        #print("Data Length: ", len(inpDataAllArray), "Array Num : ", i)
        inpDatanp = inpDataAllArray[0:DataSize];
        HannedInp = np.multiply(hanWin, inpDatanp);
        yFft = fft(HannedInp, DataSize);
        
        fft_freqs = fftshift(np.linspace(-SamplingRate/2, SamplingRate/2 - (SamplingRate/DataSize), DataSize));
        
        phaseShift = np.exp(2 * 1j * np.pi * delay * (i) * fft_freqs);
        InvFFTDat = np.multiply(yFft, phaseShift);
        #InvFFTDat = np.fft.ifft(np.multiply(yFft, phaseShift))/DataSize;
        
        QuGet.put(np.real(InvFFTDat));    

def Calc_Power_From_Network(delay, inpDataAllArray, hanWin, DataSize, NumArr, SamplingRate, ArrayNum):
    
    global outData;
    Xsnr = np.zeros(DataSize, dtype = np.int16)
    
    #print("*************************")
    startVal = 0;
    endVal   = DataSize*2;
    d1 = GetTimeinMilliSec()
    
    #print("Array Num : ", ArrayNum, delay)
    i = ArrayNum
    #for i in range(0, NumArr):
            
    #inpData = inpDataAllArray[startVal:endVal];
    
    #print("************************* : ", i, startVal, endVal)
    
    #startVal = endVal;
    #endVal   = (i + 2) * (DataSize * 2);
    
    #print("Data Length: ", len(inpData))
    inpDatanp = inpDataAllArray;#np.frombuffer(inpDataAllArray[i], dtype=np.int16)
    #print("Length : ", len(inpDataAllArray))

    HannedInp = np.multiply(hanWin, inpDatanp);
    #nfft = DataSize;
    
    yFft = fft(HannedInp, DataSize);
    #plt.figure()

    fft_freqs = fftshift(np.linspace(-SamplingRate/2, SamplingRate/2 - (SamplingRate/DataSize), DataSize));
    

    phaseShift = np.exp(2 * 1j * np.pi * delay * (i) * fft_freqs);
    #phaseShift = np.multiply(fft_freqs, ExpVal);
    
    #InvFFTDat = np.fft.ifft(np.multiply(yFft, phaseShift))/DataSize;
    InvFFTDat = np.multiply(yFft, phaseShift);
    #TimeData = np.divide(InvFFTDat, DataSize);
    #plt.plot(np.real(InvFFTDat))
    #plt.show()
    #d1 = GetTimeinMilliSec()
    #Xsnr =   np.add(Xsnr, np.real(InvFFTDat));

    #print("FFT Len : ", np.real(InvFFTDat))
    
    #CalPwr = np.power(Xsnr, 2);
    #print("Pwr Time: ", GetTimeinMilliSec() - d1);
#    print("Xsnr : ", Xsnr[0], Xsnr[1], Xsnr[2]);
#    print("CalPwr : ", CalPwr[0], CalPwr[1], CalPwr[2]);
    return np.real(InvFFTDat);#np.sum(CalPwr)
    
def Calc_Power_From_File(delay, hanWin, DataSize, NumArr, SamplingRate):
    
    global outData;
    Xsnr = np.zeros(DataSize, dtype = np.int16)
    for i in range(1, 17):
        FileName = "Data\SensorData_45_"
        IndexNum = i
        FileExt  = ".wav"
        file = open((FileName + str(IndexNum) + FileExt), "rb")

        file.read(44)
        inpData = file.read(DataSize * 2)
        inpDatanp = np.frombuffer(inpData, dtype=np.int16)
        HannedInp = np.multiply(hanWin, inpDatanp);
        nfft = DataSize;
        yFft = fft(HannedInp, nfft);
        
        #plt.figure()
        fft_freqs = fftshift(np.linspace(-SamplingRate/2, SamplingRate/2 - (SamplingRate/nfft), nfft));
        
        phaseShift = np.exp(2 * 1j * np.pi * delay * (i - 1) * fft_freqs);
        #phaseShift = np.multiply(fft_freqs, ExpVal);
        
        InvFFTDat = np.fft.ifft(np.multiply(yFft, phaseShift))/nfft;
        #TimeData = np.divide(InvFFTDat, nfft);
        #plt.plot(np.real(InvFFTDat))
        #plt.show()
        Xsnr =   np.add(Xsnr, np.real(InvFFTDat));

    CalPwr = np.power(Xsnr, 2);
#    print("Xsnr : ", Xsnr[0], Xsnr[1], Xsnr[2]);
#    print("CalPwr : ", CalPwr[0], CalPwr[1], CalPwr[2]);
    return np.sum(CalPwr) 
   
