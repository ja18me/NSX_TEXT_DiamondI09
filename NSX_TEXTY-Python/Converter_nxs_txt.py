#import matplotlib.pyplot as plt
from nexusformat.nexus import *
from nexusformat.nexus.tree import NeXusError

directoryName="NxsToTxt"


def SaveToFile_XPS(Energy,Signal,RunName,ExpName):
    with open(directoryName+"/"+RunName[0:-4]+"_"+ExpName+".txt","w") as txt_file:
        txt_file.write("#"+RunName[0:-4]+" "+ExpName+"\n")
        txt_file.write("#Energy"+"\t"+"Spectrum\n")
        for i in range(len(Energy)):
            txt_file.write("".join(str(Energy[i]))+"\t"+"".join(str(Signal[0][i]))+"\n")

def SaveToFile_XAS(Energy,Ji0,Data,RunName):
    with open(directoryName+"/"+RunName[0:-4]+"_XAS.txt","w") as txt_file:
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
        try:
            a=nxload("./"+directoryName+"/"+str(x))
        except NeXusError:
            print("I am skipping {}. It is a dummy file".format(x))
            continue
        #Reading the lable of the main root of the data strcuture
        root=list(a.keys())[0]
        #Read the XAS/XPS/HAXPES identifier
        indentifier=a['/'+root+'/scan_command'].nxdata.decode('UTF-8')
        if indentifier.find('ew4000')>0: #Condition to deal with an XPS type file
            List_regions = a['/'+root+'/instrument/ew4000/region_list'].nxdata #Create a list with the XPS regions stored in the NSX file
            for region_name in List_regions:
                namestr=region_name.decode('UTF-8')
                excitation_energy=a['/'+root+'/instrument/'+namestr+'/excitation_energy'].nxdata
                energy=a['/'+root+'/instrument/'+namestr+'/energies'].nxdata
                signal=a['/'+root+'/instrument/'+namestr+'/spectrum_data'].nxdata
                try:
                    SaveToFile_XPS(energy,signal,x,namestr+'_'+str(excitation_energy[0][0]))
                except IndexError:
                    SaveToFile_XPS(energy,signal,x,namestr+'_'+str(excitation_energy[0]))       
            continue
        if indentifier.find('jenergy')>0: #Condition to deal with an XAS type file
            dataSDC=a['/'+root+'/sdc/data'].nxdata
            energy=a['/'+root+'/sdc/jenergy'].nxdata
            dataJI0=a['/'+root+'/jI0/data'].nxdata
            SaveToFile_XAS(energy,dataJI0,dataSDC,x)
            continue

