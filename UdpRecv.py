import socket
import sys
import threading
import errno
import time
import numpy as np

NUM_ARRAYS = 16
MTU_SIZE   = 1500
SLEEP_TIME = (10/1000)

#ArrayDataLock = threading.Lock();

rows, cols = (NUM_ARRAYS, 0) 
# method 2b 
ArrayData = [[0 for i in range(cols)] for j in range(rows)]

def Recv_Data(UDPIpAddress, UDPPortNum):
    print("I come here", UDPIpAddress, UDPPortNum)
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.bind((UDPIpAddress, UDPPortNum))
    sock.setblocking(0)
    
    #for ii in range(0, NUM_ARRAYS):
    #ArrayFileName = "ArrayData_" + str(ii) + ".wav";
        #Files[ii] = open(ArrayFileName, "wb");
    #Files = [open("ArrayData_" + str(ii) + ".wav", 'wb') for ii in range(NUM_ARRAYS)]
        
    while True:
        try:
            data, addr = sock.recvfrom(MTU_SIZE) # buffer size is 1024 bytes
            #print("Received %d bytes: '%s'" % (len(data), data.decode('utf-16')))
            #print("Received %d" % (len(data), ))
            #DataFile.write(data);
            ByteData = data;#bytearray(data)
            #SplitArrayData = np.split(ByteData, NUM_ARRAYS)
            sizeOfData = int(len(data) / NUM_ARRAYS);
            #print("Data Size : ", sizeOfData)
            startValue = 0
            endValue   = sizeOfData;
            #ArrayDataLock.acquire();
            #try:
            for i in range(0, NUM_ARRAYS):
                #print("startValue: ", startValue, ", endValue: ", endValue, "Len: ", len(ArrayData[i]))
                #Files[i].write(ByteData[startValue:endValue]);
                ArrayData[i].append(ByteData[startValue:endValue])
                startValue = (sizeOfData * (i+1))
                endValue = (sizeOfData * (i+2))
                if len(ArrayData[i]) <= 0:
                    print("SIZE IS ZERO");
            #finally:
            #    ArrayDataLock.release()
        
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK: 
                #print('EWOULDBLOCK')
                time.sleep(SLEEP_TIME)           # short delay, no tight loops
            else:
                print(e)
                break