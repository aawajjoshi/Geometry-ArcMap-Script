#Importing package and modules 
import arcpy, os, sys

#Setting envrionment
arcpy.env.overwriteOutput = True

#Setting path for output file
outFC = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\gpsWaypoint.shp"

#Path for the desired coordinate file
coordsys = r"c:\Geo\geo465\Aawaj_Joshi\lab10\lab10\Data\WGS 1984 UTM ZONE 15N.prj"

#Setting workspace
arcpy.env.workspace = os.path.dirname(outFC)
featClass = os.path.basename(outFC)

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

#Printing complete to signify end of task
print("Complete")
