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
fw = "Firmware"
firstDrive = True

#Add Drive info to 'drives' list
# for idx, s in enumerate(report):  
#     if search_string in s:
#         if firstDrive == False:
#             drives.append("\n\n\n\n")
#         drives.append(report[idx])
#         drives.append(report[idx + 10])
#         drives.append(report[idx + 20])
#         drives.append(report[idx + 21])
#         drives.append(report[idx + 23])
#         #print(report[idx + i])
#         firstDrive = False

for idx, s in enumerate(report):  
    if search_string in s:
        drives.append(report[idx])
        for i in range(28):
 #           if i == 0:
 #               if firstDrive == False:
 #                   drives.append("\n\n\n\n")
            if hddID in report[idx + i]:
                drives.append(report[idx + i])
            if fw in report[idx + i]:
                drives.append(report[idx + i])
            if sn in report[idx + i]:
                drives.append(report[idx + i])
            if size in report[idx + i]:
                drives.append(report[idx + i])
            if poh in report[idx + i]:
                drives.append(report[idx + i])
                pattern = r'\d+'
                match = re.findall(pattern, report[idx + i])
                if match:
                    hours = int(match[0]) * 24 + int(match[1])
                    drives.append(f"    Power On Hours . . . . . . . . . . . . . . . . . : {hours} hours\n")
            if ltw in report[idx + i]:
                drives.append(report[idx + i])
            if health in report[idx + i]:
                drives.append(report[idx + i])
            if perf in report[idx + i]:
                drives.append(report[idx + i])
            if sector in report[idx + i]:
                drives.append(report[idx + i])
            #print(report[idx + i])
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