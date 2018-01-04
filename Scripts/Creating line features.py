#Importing package and modules 
import arcpy, os, sys

#Setting envrionment
arcpy.env.overwriteOutput = True

#Path to text file
gpsFile = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\TextFiles\track.txt"

#Setting path for output file
outFC = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\gpstrack.shp"

#Path for the desired coordinate file
coordsys = r"c:\Geo\geo465\Aawaj_Joshi\lab10\Data\WGS 1984 UTM ZONE 15N.prj"

arcpy.env.workspace = os.path.dirname(outFC)
featClass = os.path.basename(outFC)

#If featClass already exists, then deleting it 
if arcpy.Exists(featClass):
    arcpy.Delete_management(featClass)

arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POLYLINE", "", "", "", coordsys)

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

#Creating an array lineArray
lineArray = arcpy.Array()
lid = 1
pid = 1

#Creating a list fieldList
fieldList = ["ID", "SHAPE@"]

#Creating insert cursor 
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:
    for gpsPnt in Lines:
        lstValue = gpsPnt.split(",")
        yCoord = float(lstValue[yCoordIndex])
        xCoord = float(lstValue[xCoordIndex])

        #Adding the coordinates to the array 
        lineArray.add(arcpy.Point(xCoord, yCoord))

        #Printing message saying each point was added to the array
        print("Add point {0} into line array".format(pid))
        pid = pid + 1

    #Inserting new row 
    isCursor.insertRow([lid, arcpy.Polyline(lineArray)])
    print("Add line {0} into line feature class".format(lid))

    #Removing all values
    lineArray.removeAll()

