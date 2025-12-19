import sys
import re
import numpy as np
from operator import itemgetter
import pandas as pd

drives = []
report = []  
health_pct = []
split_idx = []
functionOption = None


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


#Search Strings
search_string = "  -- Physical Disk Information"
hddID = "Hard Disk Model ID"
sn = "Hard Disk Serial Number"
size = "Total Size"
poh = "Power On Time"
ltw = "Lifetime Writes"
health = "Health"
perf = "Performance"
sector = "sectors"
status = "status"
firstDrive = True

#Check if input file was entered
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    inputFile = input("Please enter input file: ")

#Check if function was entered
if len(sys.argv) > 3:
    functionOption = int(sys.argv[3])
else:
    print("\nAvailable Output Formats:")
    print("1 - Health Sort")
    print("2 - All\n")

    #List of 1 to 2, excluding 3
    array = list(range(1, 3))

    while functionOption not in array:
        try:
            functionOption = int(input("Please enter an output format: "))
            if functionOption not in array:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    #End of while loop
#End of if-else statement

#Option 1
def healthSort():
    #Build list of information containing each drive
    for idx, s in enumerate(report):  
        if search_string in s:              
            drives.append(report[idx])
            for i in range(21):
                if sn in report[idx + i]:
                    drives.append(report[idx + i])

                if health in report[idx + i]:
                    num = ''.join(filter(str.isdigit, report[idx + i]))
                    if num == '':
                        num = 0
                    num = int(num)
                    drives.append(report[idx + i])
                    health_pct.append(num)

                ### BUGGY: Input file formatting dependent ###
                if sector in report[idx + i]:
                    drives.append(report[idx + i])
                
                elif status in report[idx + i]:
                    drives.append("No Sector report available")

                #For output formatting. Handles inconsistant newlines:
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
def full():
    #Build list of information containing each drive
    for idx, s in enumerate(report):  
        if search_string in s:              
            drives.append(report[idx])
            for i in range(21):
                if sn in report[idx + i]:
                    drives.append(report[idx + i])

                if poh in report[idx + i]:
                    drives.append(report[idx + i])

                if ltw in report[idx + i]:
                    drives.append(report[idx + i])
                
                if health in report[idx + i]:
                    num = ''.join(filter(str.isdigit, report[idx + i]))
                    if num == '':
                        num = 0
                    num = int(num)
                    drives.append(report[idx + i])
                    health_pct.append(num)

                ### BUGGY: Input file formatting dependent ###
                if sector in report[idx + i]:
                    drives.append(report[idx + i])
                
                elif status in report[idx + i]:
                    drives.append("No Sector report available")

                #For output formatting. Handles inconsistant newlines:
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
    df.columns = ['Model', 'SN', 'PowerOnHours', 'LifetimeWrites', 'Health', 'Sectors', 'Blank', 'Hth']
    df = df.sort_values('Hth')

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
#End of full()

if functionOption == 1:
    healthSort()
elif functionOption == 2:
    full()
else:
    print("Error. Exiting. Try Again.")