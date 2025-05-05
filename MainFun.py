import sys
import math
import time
import threading
import numpy as np
import matplotlib
import pyqtgraph as pg
import multiprocessing

from multiprocessing.pool import ThreadPool
from matplotlib           import pyplot as plt
from BeamFormFFT          import Calc_Power_From_NetworkMP
from UdpRecv              import Recv_Data
from UdpRecv              import ArrayData
from UpdateGUI            import GUIProcess

from datetime             import datetime



UDP_IP     = "127.0.0.1"
UDP_PORT   = 5015

Dist   = 0.09;
cSound = 1500;
#enrg   = zeros(1, 18);
NumArr = 16;

MinAngle  = 0;
MaxAngle  = 180;
AngleJump = 5;

LISTSIZE  = 205;
DataSize     = LISTSIZE * 40;   # size in samples
SamplingRate = 16000;


def ReadArrayDataAndProcess():
    print("Enter-0")
    
    TimeVal = 0;
    
    hanWin = np.hanning(DataSize)        
    EnergyVal = np.zeros(int(MaxAngle/AngleJump) + 1)
    
    inpData1 = np.arange((DataSize + 1)*NumArr, dtype=np.int16);
    
    inpData = inpData1.reshape(NumArr, (DataSize+1))
    
    QuPut   = multiprocessing.Queue()
    QuGet   = multiprocessing.Queue()
    QuDly   = multiprocessing.Queue()

    jobs = []
    
    cpuCount = multiprocessing.cpu_count()
    
    for i in range(cpuCount):
        p = multiprocessing.Process(target=Calc_Power_From_NetworkMP, args=(QuPut, QuGet, QuDly, hanWin, DataSize, NumArr, SamplingRate))
        jobs.append(p)
        p.start()    

    print(inpData.shape)
    print(len(inpData[0]))
    
    while True:
        #print("Run in A Loop")
        
        #ArrayDataLock.acquire();
        #try:
        DataArrayLen = 1;
        
        dt = datetime.now()
        dtMicS = dt.microsecond;
        
        for i in range(0, NumArr):
            ListLen = len(ArrayData[i]);
            if ListLen < LISTSIZE:
                DataArrayLen = 0;
            elif ListLen >= LISTSIZE:
                startVal = 0;
                endVal   = 0;
                for ii in range(0, LISTSIZE):
                    a = ArrayData[i].pop(0);                        
                    bb = np.frombuffer(a, dtype=np.int16)
                    endVal = len(bb) * (ii + 1);
                    #print(len(bb), startVal, endVal);
                    inpData[i, startVal:endVal] = bb;
                    #np.insert(inpData[i], np.frombuffer(a, dtype=np.int16, count=40));
                    startVal = endVal;
                    #endVal   = (i + 2) * (DataSize*2);                        
       # finally:
      #      ArrayDataLock.release();
        dt1 = datetime.now();
        dtMicS1 = dt1.microsecond;
                
        if DataArrayLen == 0:
            time.sleep(10/1000)
            continue;
            
        FFTData0 = np.arange(DataSize*NumArr, dtype=np.int16)
                
        FFTData = FFTData0.reshape(NumArr, DataSize)            
              
        #print("FFt Data Len: ", FFTData.shape)
        print(inpData.shape, DataArrayLen, dtMicS1 - dtMicS);
        
        #print(hanWin.size)
        jj = 1
        #EnergyVal[0] = 0;
        #EnergyVal[int(MaxAngle/AngleJump)] = 0;
        #EnergyVal = np.zeros(int(MaxAngle/AngleJump))
        EnergyVal = np.zeros(int(MaxAngle/AngleJump) + 1)
        dt2 = GetTimeinMilliSec()
        #dtMicS2 = dt2.microsecond;
        
        for deg in range(MinAngle, MaxAngle-2, AngleJump):
            
            FFTData1 = np.zeros(DataSize, dtype = np.int16)
            #dt3 = GetTimeinMilliSec()
            delay = Dist * math.cos(deg/180 * np.pi)/cSound;
            #print("BeamFromTimeTaken-0 : ", GetTimeinMilliSec() - dt3);
            for i in range(0, NumArr):
                inpData[i, DataSize] = i;
                QuDly.put(delay);
                QuPut.put(inpData[i]);
            for i in range(0, NumArr):
                    FFTData11 = QuGet.get();
                    FFTData1 = np.add(FFTData1, FFTData11)
                    
            CalPwr = np.power(FFTData1, 2);
            EnergyVal[jj] = np.sum(CalPwr);
            jj = jj + 1;
        
        print("BeamFromTimeTaken : ", GetTimeinMilliSec() - dt2,   np.argmax(EnergyVal));
        
        EnergyVal_1 = np.trim_zeros(EnergyVal);
        
        #ydata = EnergyVal_1;
        #xdata = np.linspace(0, MaxAngle, len(EnergyVal_1))
        
        #ydata = ydata + np.argmax(EnergyVal);
        #xdata = xdata + np.max(EnergyVal);
        
        print("Index and Value", np.argmax(EnergyVal) * AngleJump, np.max(EnergyVal));
        
        TimeVal = TimeVal + 1;
        
        #update_plot();
        

    
def GetTimeinMilliSec():
    milli_sec = int(round(time.time() * 1000));
    return milli_sec; 
            
if __name__ == '__main__':
   
    UDPRecvDataThread = threading.Thread(target=Recv_Data, args=(UDP_IP, UDP_PORT));
    UDPRecvDataThread.daemon = True
    UDPRecvDataThread.start();
    
    QuGUIData   = multiprocessing.Queue()
    
    p = multiprocessing.Process(target=GUIProcess, args=(QuGUIData, ))
    p.start()    
       
    print("After UDP RECV processsing");
    
    ReadArrayDataAndProcess();
    
