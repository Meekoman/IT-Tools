import sys

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