#import matplotlib.pyplot as plt
from nexusformat.nexus import *

directoryName="NxsToTxt"


def SaveToFile(Energy,Ji0,Data,RunName,mode):
    with open(directoryName+"/"+RunName[0:-4]+mode+".txt","w") as txt_file:
        txt_file.write("#"+RunName[0:-4]+mode+"\t XAS\n")
        txt_file.write("#Energy"+"\t"+mode+"Data_Norm\n")
        if mode == "TEY":
            for i in range(len(Energy)):
                txt_file.write("".join(str(Energy[i]))+"\t"+"".join(str(Data[i]/Ji0[i]))+"\n")
        if mode == "TFY":            
            for i in range(len(Energy)):
                txt_file.write("".join(str(Energy[i]))+"\t"+"".join(str(Data[i]))+"\n")


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
        dataSDC=a['/entry1/ca16b/ca16b'].nxdata
        energy=a['/entry1/ca16b/pgm_energy'].nxdata
        dataJI0=a['/entry1/ca18b/ca18b'].nxdata
        SaveToFile(energy,dataJI0,dataSDC,x,"TEY")
        a=nxload("./"+directoryName+"/"+str(x))
        try:
            dataSDC=a['/entry1/xspress3Mini/total'].nxdata
            energy=a['/entry1/xspress3Mini/pgm_energy'].nxdata
            SaveToFile(energy,[],dataSDC,x,"TFY")
        except NeXusError:
            pass

