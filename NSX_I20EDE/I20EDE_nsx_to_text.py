from nexusformat.nexus import *

file=nxload('50602_B19_industrial_SCNMC811_scan3.nxs')
data=file['/entry1/lnI0It/data'].nxdata
#print(data)
energy_scale=file['/entry1/lnI0It/energy'].nxdata
#print(energy_scale)

#Choose idexes for Ni K-edge
ilower=0 #define new integer
ihigher=0
for i in range(len(energy_scale)):
    if energy_scale[i] > 8200 and energy_scale[i] < 8201.5:
        ilower=i
        #print(ilower)
    if energy_scale[i] > 8530 and energy_scale[i] < 8531.5:
        ihigher=i
        #print(ihigher)
        
#Cropping the matrix for the Ni K-edge
index=0
for scan in data: #one scan contains 1024 points
    if max(scan) > 10:
        next
        index=index+1
    else:
        with open("data"+str(index)+".txt","w") as txt_file:
            for i in range(ilower,ihigher):
                txt_file.write("".join(str(energy_scale[i]))+"\t"+"".join(str(scan[i]))+"\n")
        index=index+1

#Erasing unwanted scans
#scans=[] #define a new list or array or slice
#

