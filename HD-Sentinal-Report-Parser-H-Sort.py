import sys
import re
import numpy as np
from operator import itemgetter
import pandas as pd

drives = []
report = []  
health_pct = []
split_idx = []

#Check if input file was entered
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    inputFile = input("Please enter input file: ")


#Open input file
with open (inputFile, encoding= "ISO-8859-1") as myfile:
    # For each line, read to a string
    for line in myfile:              
        report.append(line)

search_string = "  -- Physical Disk Information"
hddID = "Hard Disk Model ID"
sn = "Hard Disk Serial Number"
size = "Total Size"
poh = "Power On Time"
ltw = "Lifetime Writes"
health = "Health"
perf = "Performance"
sector = "sector"
firstDrive = True

for idx, s in enumerate(report):  
    if search_string in s:
        drives.append(report[idx])
        for i in range(28):
            if sn in report[idx + i]:
                drives.append(report[idx + i])
            if health in report[idx + i]:
                num = ''.join(filter(str.isdigit, report[idx + i]))
                if num == '':
                    num = 0
                num = int(num)
                drives.append(report[idx + i])
                health_pct.append(num)
            if sector in report[idx + i]:
                drives.append(report[idx + i])
            #print(report[idx + i])
            firstDrive = False
        drives.append("\n\n")
        split_idx.append(len(drives))


#Sort by health
dMatrix = np.array(drives)

#print(split_idx)


dMatrix = np.split(dMatrix, split_idx, axis=0)
drives_df = pd.DataFrame(dMatrix)

health_df = pd.DataFrame(health_pct)
df = pd.concat([drives_df, health_df], axis=1, join="inner")
df.columns = ['Model', 'SN', 'Health', 'Sectors', 'Blank', 'Hth']

df = df.sort_values('Hth')

#Cleanup dataframe
df = df.drop(['Blank', 'Hth'], axis=1)
print(df)

npArray = df.to_numpy()
print(npArray)
#Check if user entered an output file name
if len(sys.argv) > 2:
    outputFile = sys.argv[2]
else:
    outputFile = input("Please enter new output file name: ")


#Write to output file
#of = open(outputFile, 'w')
#of.writelines(df)
#of.close()
with open(outputFile, 'wb'):
    npArray.tofile(outputFile, sep=' ', format='%s')