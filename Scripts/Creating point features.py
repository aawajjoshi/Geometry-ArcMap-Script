#Importing package and modules 
import arcpy, os, sys

#Setting envrionment
arcpy.env.overwriteOutput = True

#Path to text file
gpsFile = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\TextFiles\waypoint.txt"

#Setting path for output file
outFC = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\gpsWaypoint.shp"

#Path for the desired coordinate file
coordsys = r"c:\Geo\geo465\Aawaj_Joshi\lab10\Data\WGS 1984 UTM ZONE 15N.prj"

#If featClass already exists, then deleting it 
if arcpy.Exists(featClass):
    arcypy.Delete_management(featClass)

#Creating shapefile 
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POINT", "", "", "", coordsys)

#Adding fields
arcpy.AddField_management(featClass, "Ident", "TEXT", "", "", 20)
arcpy.AddField_management(featClass, "Comment", "TEXT", "", "", 20)
arcpy.AddField_management(featClass, "Latitude", "DOUBLE")
arcpy.AddField_management(featClass, "Longitude", "DOUBLE")

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
idIndex = lstHeader.index("ident")
comIndex = lstHeader.index("comment")
latIndex = lstHeader.index("lat")
longIndex = lstHeader.index("long")

pid = 1

#Creating a list fieldList that will be populated with new attributes
fieldList = ["ID", "Ident", "Comment", "Latitude", "Longitude", "SHAPE@"]

#Creating insert cursor 
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:

#Iterating through list Lines
    for gpsPnt in Lines:
        lstValue = gpsPnt.split(",")
        xCoord = float(lstValue[xCoordIndex])
        yCoord = float(lstValue[yCoordIndex])
        
        idValue = str(lstValue[idIndex])
        comValue = str(lstValue[comIndex])
        latValue = float(lstValue[latIndex])
        longValue = float(lstValue[longIndex])

        #Creating a new list newPoint with the necessary attributes
        newPoint = [pid, idValue, comValue, latValue, longValue, arcpy.Point(xCoord, yCoord)]

        #Inserting new row
        isCursor.insertRow(newPoint)

        #Printing the new records that got added
        print("Record number {0} written to feature class".format(pid))

        pid = pid + 1

#Signifies end of task
print("Point Shapefile complete")

