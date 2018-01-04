#Importing package and modules 
import arcpy, os, csv

#Setting envrionment
arcpy.env.overwriteOutput = True

#Path to text file
crimeFile = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\TextFiles\crime_incidents_2011_CSV.csv"

#Setting path for output file
outFC = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\Homicide.shp"

#Path for the desired coordinate file
coordsys = r"c:\Geo\geo465\Aawaj_Joshi\lab10\Data\NAD 1983.prj"

arcpy.env.workspace = os.path.dirname(outFC)
featClass = os.path.basename(outFC)

#If featClass already exists, then deleting it 
if arcpy.Exists(featClass):
    arcpy.Delete_management(featClass)

arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POINT", "", "", "", coordsys)

#Adding fields
arcpy.AddField_management(featClass, "Offense", "TEXT", "", "", 50)
arcpy.AddField_management(featClass, "District", "TEXT", "", "", 50)

#Reading data from the text file 
crimeLocations = open(crimeFile, 'r')

#Reads the entire file 
csvReader = csv.reader(crimeLocations)

#Placing cursor in next line
headerLine = csvReader.next()

yCoordIndex = headerLine.index("LATITUDE")
xCoordIndex = headerLine.index("LONGITUDE")
offenseIndex = headerLine.index("OFFENSE")
districtIndex = headerLine.index("DISTRICT")

pid = 1

#Creating a list fieldList
fieldList = ["ID", "OFFENSE", "DISTRICT", "SHAPE@"]

#Creating insert cursor 
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:

#Iterating through csvReader:
    for crimePnt in csvReader:
        
        xCoord = float(crimePnt[xCoordIndex])
        yCoord = float(crimePnt[yCoordIndex])
        
        offense = str(crimePnt[offenseIndex])
        district = str(crimePnt[districtIndex])

        #Checking to see if the coordinates are 0
        if xCoord == 0 or yCoord == 0:
            #Continue if they are 0
            continue

        #Inserting new row 
        isCursor.insertRow([pid, offense, district, arcpy.Point(xCoord, yCoord)])

        pid = pid + 1

#Closing file
crimeLocations.close()
       
