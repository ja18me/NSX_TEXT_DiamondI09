#import matplotlib.pyplot as plt
from nexusformat.nexus import *

directoryName="NxsToTxt"


def SaveToFile(Energy,Ji0,Data,RunName):
    with open(directoryName+"/"+RunName[0:-4]+".txt","w") as txt_file:
        txt_file.write("#"+RunName[0:-4]+"\t XAS\n")
        txt_file.write("#Energy"+"\t"+"Ji0"+"\t"+"Spectrum"+"\t"+"Data_Norm\n")
        for i in range(len(Energy)):
            txt_file.write("".join(str(Energy[i]))+"\t"+"".join(str(Ji0[i]))+"\t"+"".join(str(Data[i]))+"\t"+"".join(str(Data[i]/Ji0[i]))+"\n")

import os
import sys
ifExistDirectory = os.path.exists("./"+directoryName)
if not(ifExistDirectory):
    print("Directory "+directoryName+" does not exist")
    os.mkdir("./"+directoryName)
    print("Directory "+directoryName+" has been created")
    print("Please move the nxs files you want to transform into txt files in this directory")
    sys.exit()
  
files=os.listdir("./"+directoryName)
if len(files)==0:
    print(directoryName+" is empty")
    print("Please move the nxs files you want to transform into txt files in this directory")
    sys.exit()
    
for x in files:
    if x[-3:]!='nxs':
        next
    else:
        a=nxload("./"+directoryName+"/"+str(x))
        dataSDC=a['/entry/sdc/data'].nxdata
        energy=a['/entry/sdc/jenergy'].nxdata
        dataJI0=a['/entry/jI0/data'].nxdata
        SaveToFile(energy,dataJI0,dataSDC,x)

