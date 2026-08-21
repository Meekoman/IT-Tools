import sys
import re
import numpy as np
from operator import itemgetter
import pandas as pd
from itertools import chain

#Report vars
drives4 = []
report = []  
health_pct = []
poh_sort = []
split_idx = []
sectorArray = []
#Search String vars
search_string = "  -- Physical Disk Information"
hddID = "Hard Disk Model ID"
sn = "Hard Disk Serial Number"
size = "Total Size"
poh = "Power On Time"
pod = "Power On Days"
ltw = "Lifetime Writes"
health = "Health"
perf = "Performance"
sector = "sector"
fw = "Firmware"
error = "error"
se = ["sector", "error"]
http = "http"
unknown = "unknown"
end = ["ATA Information", "Properties"]
linux = False

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
    return functionOption
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
        if "Linux" in line:
            linux = True

# Function to add a value to a specified column
def add_value(df, column_name, value, index):
    if column_name in df.columns:
        df.loc[index, column_name] = value
        return df
    else:
        print(f"Column '{column_name}' does not exist in the DataFrame.")

def add_pod_column(df):
    if pod not in df.columns:
        # Add the new column with NaN values (or any default value)
        df[pod] = pd.NA
        # Find the index of the 'Poh' column
        poh_index = df.columns.get_loc(poh)
        # Reorder columns to place the new column at the index of 'Poh'
        cols = list(df.columns)
        cols.insert(poh_index + 1, cols.pop(-1))  # Move the new column to the index after 'Poh'
        df = df[cols]  # Reindex the DataFrame with the new order
        return df
    else:
        print(f"The column '{pod}' exists in the DataFrame.")
        return df

def dataframeCleanup(df):
    first_colon = 1
    for columnName in df:
        if 'Health' in columnName or 'Performance' in columnName:
            df[columnName] = df[columnName].str.replace(r'\D', '', regex=True)
            df[columnName] = df[columnName].str.strip()
        elif ":" in df.iloc[0][columnName] or ":" in df.iloc[len(df) - 1][columnName]:
            df[columnName] = df[columnName].str.split(': ', expand=True, n=first_colon)[first_colon]
            df[columnName] = df[columnName].str.strip()

    return df


#Option 5
def refactor(option):
    driveIndex = 0
    selection = []

 ### Variable to change if you want to sort by a different value ###
 # Valid values (Output dependent):
 # - health
 # - size
 # - poh 
 # - ltw
 # - fw
 # - sn

    sortBy = health

### ###

    if linux:
        maxLines = 23
    else:
        maxLines = 28

    Sectors = "Sectors"
    nl = "Newline"
    #Build list of information containing each drive
    if option == 1:
        selection = [sn, health]
        sort = True
    elif option == 2:
        selection = [sn, health, ltw]
        sort = True
    elif option == 3:
        selection = [fw, sn, size, poh, ltw, health, perf]
        sort = True
    else:
        sort = False

    selection.insert(0, 'Model')
    selection.insert(0, search_string)
    selection.append(Sectors)
    selection.append(nl)
    drives = pd.DataFrame(columns=selection)

    for idx, s in enumerate(report):  
        if search_string in s:
            if option < 4:
                add_value(drives, search_string, s, driveIndex)
            subset = selection.copy()

            for i in range(maxLines):
                target_line = report[idx + i]
                for word in subset:
                    if word in target_line:
                        if poh in target_line:
                            add_value(drives, poh, target_line, driveIndex)
                            pattern = r'\d+'
                            match = re.findall(pattern, target_line)
                            if pod not in drives.columns:
                                drives = add_pod_column(drives)
                            if match:
                                hours = int(match[0]) * 24 + int(match[1])
                                h = f"    Power On Hours . . . . . . . . . . . . . . . . . : {hours} hours\n"
                                add_value(drives, pod, h, driveIndex)
                            break
                        else:
                            add_value(drives, word, target_line, driveIndex)
                            subset.remove(word)
                            break

                #Search for Sectors/Errors
                if option != 4:
                    if (any(w in target_line for w in se) and 
                    http not in target_line):
                        sectorArray.append(target_line)
                else:
                    if any(w in target_line for w in end):
                        drives4.append("\n")
                        break
                    elif i == (maxLines - 1):
                        drives4.append("\n\n")
                    else: 
                        drives4.append(target_line)      
            #End of loop that collects individual drive info

            #Add list of sectors to drives dataframe
            if len(sectorArray) > 0:
                s = " ".join(sectorArray)
                add_value(drives, Sectors, s, driveIndex)
            add_value(drives, nl, "\n\n", driveIndex)

            sectorArray.clear()            
            driveIndex += 1
    #End of loop that records all drive info


    #Replace NaN values
    for column in drives.columns:
        drives[column] = drives[column].fillna(f"    {column}\n")

    #Convert 'drives' list into numpy array
    dMatrix = np.array(drives)

    #Sort by drive health
    if sort:
        if sortBy != sn:
            drives['Sorted'] = drives[sortBy].apply(lambda x: int(re.search(r'(\d+)', x).group()) 
                                                    if re.search(r'(\d+)', x) else float('inf'))
        else:
            drives['Sorted'] = drives[sortBy].apply(lambda x: re.search(r':\s*([A-Za-z0-9]+)', x).group(1) 
                                                    if re.search(r':\s*([A-Za-z0-9]+)', x) else "")


        #Debugging
        pd.set_option('display.max_rows', len(drives))
        print(drives.sort_values(by='Sorted', ascending=True))

        # Sort the DataFrame by the new column, then drop the column if not needed
        if sortBy == health:
            sorted_df = drives.sort_values(by='Sorted', ascending=True).drop(columns=['Sorted'])
        #elif sortBy == sn:
        #    sorted_df = drives.sort_values("Hard Disk Serial Number", key=lambda col: col.map(nat_key), ascending=True)
        else:
            sorted_df = drives.sort_values(by='Sorted', ascending=True).drop(columns=['Sorted'])
        
        npArray = sorted_df.to_numpy()
        #print(sorted_df)
    else:
        if option != 4:
            npArray = dMatrix


    #Cleanup sorted_df
    if sort:
        sorted_df.rename(columns={'  -- Physical Disk Information':'Disk #'}, inplace=True)
        sorted_df.rename(columns={'Hard Disk Serial Number':'Serial Number'}, inplace=True)
        sorted_df = dataframeCleanup(sorted_df)
        sorted_df = sorted_df.drop('Newline', axis=1)
        sorted_df = sorted_df.drop('Disk #', axis=1)


    #Check if user entered an output file name
    if len(sys.argv) > 2:
        outputFile = sys.argv[2]
    else:
        outputFile = input("Please enter new output file name: ")

    if option != 4:
        #Write to output file
        summaryFile = "Summary-" + outputFile
        with open(outputFile, 'wb'):
            npArray.tofile(outputFile, sep=' ', format='%s')
        if sort:
            with open(summaryFile, 'w') as f:
                f.write(sorted_df.to_string())
    else:
        #Write to output file
        of = open(outputFile, 'w')
        of.writelines(drives4)
        of.close()
#End of refactor()


#Check if function was entered
if len(sys.argv) > 3:
    functionOption = int(sys.argv[3])
else:
    #functionOption = 0
    printOptions()
    functionOption = outputPicker()
#End of if-else statement


if functionOption == 0:
    printOptions()
    outputPicker()
elif functionOption >= 0 and functionOption <= 4:
    refactor(functionOption)
else:
    print("Error. Exiting. Try running the program again.")