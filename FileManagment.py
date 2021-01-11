import arcpy
import os


def makeNewGDBIfDoesntExist(folder, GDBName):
    '''Makes a new file geodatabase if the
    GDB does not already exist. Returns the the path
    of the GDB
    '''
    if arcpy.Exists(os.path.join(folder, GDBName)):
        pass
    else:
        arcpy.CreateFileGDB_management(folder, GDBName)

    GDBPath = os.path.join(folder, GDBName)
    return GDBPath


def findAllGeospatialFiles(folder, searchWord='', fileType="FeatureClass"):
    '''Returns a list of all the feature classes
    that are within and the provided folder and any
    addtionaly subfolders
    '''
    geoSpatialFiles = []
    walk = arcpy.da.Walk(folder, datatype=fileType)

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if searchWord in os.path.join(dirpath, filename):
                geoSpatialFiles.append(os.path.join(dirpath, filename))
    return geoSpatialFiles
