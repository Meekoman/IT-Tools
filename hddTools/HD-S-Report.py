import sys
import re
import numpy as np
from operator import itemgetter
import pandas as pd

#Report vars
drives = []
report = []  
health_pct = []
split_idx = []
#Search String vars
search_string = "  -- Physical Disk Information"
hddID = "Hard Disk Model ID"
sn = "Hard Disk Serial Number"
size = "Total Size"
poh = "Power On Time"
ltw = "Lifetime Writes"
health = "Health"
perf = "Performance"
sector = "sectors"
fw = "Firmware"
firstDrive = True
#List of 1 to 4, excluding 5
array = list(range(1, 5))

def printOptions():
    print("\nAvailable Output Formats:")
    print("1 - Health Sort")
    print("2 - SN, Health, Sector")
    print("3 - Simplified All")
    print("4 - All\n")
    print("0 - See an example\n")
#End of printOptions()

#Takes in an integer as input
def printExampleOutput(num):
    if num == 1:
        print("\n   -- Physical Disk Information - Disk: #1: INTEL SSDSC2KB038T8 --\n" + 
            "Hard Disk Serial Number  . . . . . . . . . . . . : PHYF112300Y83P8EGN\n" + 
            "Health . . . . . . . . . . . . . . . . . . . . . : ################---- 81 % (Good)\n" + 
            "The status of the solid state disk is PERFECT. Problematic or weak sectors were not found.\n")
    elif num == 2:
        print("\n  -- Physical Disk Information - Disk: #0: INTEL SSDSC2KB038T8 --\n" + 
            "Hard Disk Serial Number  . . . . . . . . . . . . : PHYF112300QG3P8EGN\n" + 
            "Lifetime Writes  . . . . . . . . . . . . . . . . : 991.13 TB\n" + 
            "Health . . . . . . . . . . . . . . . . . . . . . : ##########---------- 52 % (Fair)\n" + 
            "There are 8 bad sectors on the disk surface. The contents of these sectors were moved to the spare area.\n")
    elif num == 3:
        print("\n  -- Physical Disk Information - Disk: #0: INTEL SSDSC2KB038T8 --\n" + 
            "Hard Disk Model ID . . . . . . . . . . . . . . . : INTEL SSDSC2KB038T8\n" + 
            "Firmware Revision  . . . . . . . . . . . . . . . : XCV10132\n" + 
            "Hard Disk Serial Number  . . . . . . . . . . . . : PHYF112300QG3P8EGN\n" + 
            "Total Size . . . . . . . . . . . . . . . . . . . : 3662827 MB\n" + 
            "Power On Time  . . . . . . . . . . . . . . . . . : 1258 days, 13 hours\n" + 
            "Power On Hours . . . . . . . . . . . . . . . . . : 30205 hours\n" + 
            "Lifetime Writes  . . . . . . . . . . . . . . . . : 991.13 TB\n" + 
            "Health . . . . . . . . . . . . . . . . . . . . . : ##########---------- 52 % (Fair)\n" + 
            "Performance  . . . . . . . . . . . . . . . . . . : #################### 100 % (Excellent)\n" + 
            "There are 8 bad sectors on the disk surface. The contents of these sectors were moved to the spare area.\n")
    elif num == 4:
        print("\n  -- Physical Disk Information - Disk: #0: INTEL SSDSC2KB038T8 --\n\n" + 
            "Hard Disk Summary\n" + 
            "-------------------\n" + 
            "Hard Disk Number . . . . . . . . . . . . . . . . : 0\n" + 
            "Interface  . . . . . . . . . . . . . . . . . . . : S-ATA Gen3\n" + 
            "Disk Controller  . . . . . . . . . . . . . . . . : Avago Adapter, SAS3 3008 Fury -StorPort (PCI\CC_010700&DT_0) [VEN: 1000, DEV: 0097] Version: 2.51.25.1, 8-30-2018\n" + 
            "Disk Location  . . . . . . . . . . . . . . . . . : Bus Number 0, Target Id 0, LUN 0, Device: 1\n" + 
            "Hard Disk Model ID . . . . . . . . . . . . . . . : INTEL SSDSC2KB038T8\n" + 
            "Firmware Revision  . . . . . . . . . . . . . . . : XCV10132\n" + 
            "Hard Disk Serial Number  . . . . . . . . . . . . : PHYF112300QG3P8EGN\n" + 
            "Total Size . . . . . . . . . . . . . . . . . . . : 3662827 \n" + 
            "Power State  . . . . . . . . . . . . . . . . . . : Active\n" + 
            "Device Type  . . . . . . . . . . . . . . . . . . : Fixed Disk\n" + 
            "Current Temperature  . . . . . . . . . . . . . . : 22 Â°C\n" + 
            "Maximum Temperature (Ever Measured)  . . . . . . : 25 Â°C, 3/31/2025 7:31:42 PM\n" + 
            "Minimum Temperature (Ever Measured)  . . . . . . : 21 Â°C, 3/31/2025 6:15:46 PM\n" + 
            "Power On Time  . . . . . . . . . . . . . . . . . : 1258 days, 13 hours\n" + 
            "Estimated Remaining Lifetime . . . . . . . . . . : 153 days\n" + 
            "Lifetime Writes  . . . . . . . . . . . . . . . . : 991.13 TB\n" + 
            "Health . . . . . . . . . . . . . . . . . . . . . : ##########---------- 52 % (Fair)\n" + 
            "Performance  . . . . . . . . . . . . . . . . . . : #################### 100 % (Excellent)\n\n" + 
            "There are 8 bad sectors on the disk surface. The contents of these sectors were moved to the spare area.\n" + 
            "At this point, warranty replacement of the disk is not yet possible, only if the health drops further.\n" + 
            "It is recommended to examine the log of the disk regularly. All new problems found will be logged there.\n" + 
            "The TRIM feature of the SSD is supported and enabled for optimal performance.\n" + 
            "It is recommended to continuously monitor the hard disk status.\n")
    else:
        print("Invalid number")
#End of printExampleOutput

#Have user decide how he/she want the report formatted
def outputPicker():
    functionOption = None
    example = None

    while functionOption not in array:
        try:
            functionOption = int(input("Please enter an output format (Press 'Enter' to reprint menu): "))
            if functionOption == 0:
                while example not in array:
                    try:
                        example = int(input("Which example output would you like to see? Press 'Enter' to see options: "))
                        printExampleOutput(example)
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
                        printOptions()
                #End of example help menu
                example = None
            
            elif functionOption not in array:
                print("Invalid input. Please try again. Press 'Enter' to reprint menu.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            printOptions()
    #End of while loop
#End of outputPicker()

#Check if input file name was entered
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    inputFile = input("Please enter input file: ")

#Open input file
with open (inputFile, encoding= "ISO-8859-1") as myfile:
    # For each line, read to a string
    for line in myfile:              
        report.append(line)

#Option 1
def healthSort(): 
    #Build list of information containing each drive
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

                firstDrive = False
            drives.append("\n\n")
            #Mark split point
            split_idx.append(len(drives))


    #Sort by drive health
    dMatrix = np.array(drives)
    dMatrix = np.split(dMatrix, split_idx, axis=0)

    drives_df = pd.DataFrame(dMatrix)
    health_df = pd.DataFrame(health_pct)
    df = pd.concat([drives_df, health_df], axis=1, join="inner")

    df.columns = ['Model', 'SN', 'Health', 'Sectors', 'Blank', 'Hth']

    df = df.sort_values('Hth')

    print(df)

    #Cleanup dataframe
    df = df.drop(['Hth'], axis=1)
    npArray = df.to_numpy()

    #Check if user entered an output file name
    if len(sys.argv) > 2:
        outputFile = sys.argv[2]
    else:
        outputFile = input("Please enter new output file name: ")


    #Write to output file
    with open(outputFile, 'wb'):
        npArray.tofile(outputFile, sep=' ', format='%s')
#End of healthSort()

#Option 2
def sn_health_sector():
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
#End of sn_health_sector()

#Option 3
def simplified_full():
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
#End of simplified_full()

#Option 4
def full():
    firstDrive = True
    #Add Drive info to 'drives' list
    for idx, s in enumerate(report):  
        if search_string in s:
            for i in range(28):
                if i == 0:
                    if firstDrive == False:
                        drives.append("\n\n\n\n")
                drives.append(report[idx + i])
                #print(report[idx + i])
                firstDrive = False

    #Check if user entered an output file name
    if len(sys.argv) > 2:
        outputFile = sys.argv[2]
    else:
        outputFile = input("Please enter new output file name: ")

    #Write to output file
    of = open(outputFile, 'w')
    of.writelines(drives)
    of.close()
#End of full()


#Check if function was entered
if len(sys.argv) > 3:
    functionOption = int(sys.argv[3])
else:
    printOptions()

    outputPicker()
#End of if-else statement

if functionOption == 0:
    printOptions()
    outputPicker()
elif functionOption == 1:
    healthSort()
elif functionOption == 2:
    sn_health_sector()
elif functionOption == 3:
    simplified_full()
elif functionOption == 4:
    full()
else:
    print("Error. Exiting. Try running the program again.")