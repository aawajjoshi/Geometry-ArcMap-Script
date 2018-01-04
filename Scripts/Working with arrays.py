#Importing package and modules 
import arcpy, os, sys

#Setting envrionment
arcpy.env.overwriteOutput = True

#Path to text file
gpsFile = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\TextFiles\track.txt"

#Setting path for output file
outFC = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\multitrack.shp"

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

#Creating a new index
newIndex = lstHeader.index("new_seg")

#Creating an array lineArray
lineArray = arcpy.Array()
lid = 1

#Creating a list fieldList
fieldList = ["ID", "SHAPE@"]

#Creating insert cursor 
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:
    for gpsPnt in Lines:
        lstValue = gpsPnt.split(",")
        isNew = str(lstValue[newIndex].upper())
                    
        #Checking if value of isNew is True 
        if isNew == "TRUE":
            #Checking if the number of lines in the Array is less than 0
            if lineArray.count>0:
                #Inserting new row if conditions are met 
                isCursor.insertRow([lid, arcpy.Polyline(lineArray)])
                print("Insert track line {0}".format(lid))
                #Removing all values
                lineArray.removeAll()
                lid = lid + 1

                yCoord = float(lstValue[yCoordIndex])
                xCoord = float(lstValue[xCoordIndex])

                #Adding the coordinates to the array 
                lineArray.add(arcpy.Point(xCoord, yCoord))

        yCoord = float(lstValue[yCoordIndex])
        xCoord = float(lstValue[xCoordIndex])

        #Adding the coordinates to the array 
        lineArray.add(arcpy.Point(xCoord, yCoord))

    #Inserting new row 
    isCursor.insertRow([lid, arcpy.Polyline(lineArray)])
    print("Add line {0} into line feature class".format(lid))

    #Removing all values
    lineArray.removeAll()


