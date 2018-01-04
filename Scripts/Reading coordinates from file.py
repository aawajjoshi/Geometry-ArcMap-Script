#Importing package and modules 
import arcpy, os, sys

#Setting envrionment
arcpy.env.overwriteOutput = True

#Path to text file
gpsFile = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\TextFiles\waypoint.txt"

#Reading data from the text file 
fileRead = open(gpsFile, 'r')

#Reading one line at a time into headerLine variable
headerLine = fileRead.readline()

#Reading entire file into a list variable Lines
Lines = fileRead.readlines()

#Closing the file after reading the necessary data
fileRead.close()

#Splittng the read data 
lstHeader = headerLine.split(",")
yCoordIndex = lstHeader.index("y_proj")
xCoordIndex = lstHeader.index("x_proj")
pid = 1

#Iterating through list Lines
for gpsPnt in Lines:
    lstValue = gpsPnt.split(",")
    xCoord = float(lstValue[xCoordIndex])
    yCoord = float(lstValue[yCoordIndex])

    #Prinring the coordinates and it's x and y coordinates
    print("The point {0} coordinate is ({1}, {2})".format(pid, xCoord, yCoord))
    pid = pid + 1

#Printing complete to signify end of text file
print("Complete")