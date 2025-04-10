import sys
import re

drives = []
report = []  

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
            if ltw in report[idx + i]:
                drives.append(report[idx + i])
            if health in report[idx + i]:
                drives.append(report[idx + i])
            if sector in report[idx + i]:
                drives.append(report[idx + i])
            firstDrive = False
        drives.append("\n\n")

#Check if user entered an output file name
if len(sys.argv) > 2:
    outputFile = sys.argv[2]
else:
    outputFile = input("Please enter new output file name: ")

#Write to output file
of = open(outputFile, 'w')
of.writelines(drives)
of.close()