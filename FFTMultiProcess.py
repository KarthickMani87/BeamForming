import sys
import math
import time
import threading
import numpy as np
import matplotlib
import pyqtgraph as pg
import multiprocessing

from multiprocessing.pool import ThreadPool
from matplotlib import pyplot as plt
from BeamFormFFT import Calc_Power_From_Network
from UdpRecv import Recv_Data
from UdpRecv import ArrayData

 
NumArr = 16
LISTSIZE  = 205;
DataSize     = LISTSIZE * 40;   # size in samples
SamplingRate = 16000;
SLEEP_TIME = (1/1000) 
  
def square(x, x2, x3): 
    print(x)
    

    
    while True:

        time.sleep(SLEEP_TIME)           # short delay, no tight loops


def GetTimeinMilliSec():
    milli_sec = int(round(time.time() * 1000));
    return milli_sec;

def Calc_Power_From_Network1(delay, QuPut, QuGet, hanWin, DataSize, NumArr, SamplingRate, ArrayNum):
    #print("Array Id : ", ArrayNum);
    while True:
        inpDataArray = QuPut.get();
        print("Array Num  : ", ArrayNum, "Size : ", len(inpDataArray));
        QuGet.put(inpDataArray)
        #time.sleep(SLEEP_TIME)           # short delay, no tight loops
   
if __name__ == '__main__':

    inpData1 = np.arange(DataSize*NumArr, dtype=np.int16);
      
    inpData = inpData1.reshape(NumArr, DataSize) 
    
    hanWin = np.hanning(DataSize)

    QuPut = multiprocessing.Queue()
    QuGet = multiprocessing.Queue()

    inputArgs = [(0.5, hanWin, DataSize, NumArr, SamplingRate, kk) for kk in range(NumArr)]
    
    print("Start Process")
    StartTime = GetTimeinMilliSec();
    jobs = []
    for i in range(NumArr):
        p = multiprocessing.Process(target=Calc_Power_From_Network1, args=(0.5, QuPut, QuGet, hanWin, DataSize, NumArr, SamplingRate, i))
        jobs.append(p)
        p.start()
    
    print("Process Done : ", GetTimeinMilliSec() -  StartTime);
    
    while True:
        for i in range(0, NumArr):
            QuPut.put(inpData[i]);
        
        StartTime = GetTimeinMilliSec();
        for i in range(0, NumArr):
            inpDataArray = QuGet.get();
        print("Len : ", len(inpDataArray), "Read Done : ", GetTimeinMilliSec() -  StartTime);    
            
        time.sleep(3)
        
    
    