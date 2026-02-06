#import matplotlib.pyplot as plt
from nexusformat.nexus import *

directoryName="NxsToTxt"


def SaveToFile(Energy,Signal,RunName,ExpName):
    with open(directoryName+"/"+RunName[0:-4]+"_"+ExpName+".txt","w") as txt_file:
        txt_file.write("#"+RunName[0:-4]+" "+ExpName+"\n")
        txt_file.write("#Energy"+"\t"+"Spectrum\n")
        for i in range(len(Energy[0])):
            txt_file.write("".join(str(Energy[0][i]))+"\t"+"".join(str(Signal[0][i]))+"\n")

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
        FileNameTracker=0
        while (list(a.entry1.instrument.keys())[FileNameTracker]!='ew4000'):
            nameExperiment=list(a.entry1.instrument.keys())[FileNameTracker]
            energy=a['/entry1/instrument/'+str(nameExperiment)+'/energies'].nxdata
            signal=a['/entry1/instrument/'+str(nameExperiment)+'/spectrum_data'].nxdata
            SaveToFile(energy,signal,x,nameExperiment)
            FileNameTracker=FileNameTracker+1

