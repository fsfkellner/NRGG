import arcpy
import os


def listStringJoiner(inputList, joiner=","):
    '''listStringJoiner(sequence[list]) -> string
    Takes an input list and returns a string where each
    element in the list is joined together to form a string
    returned string value. Default value to is to
    join with a comma.
    Example: [1,2,3,4] -> '1,2,3,4'
    '''
    stringJoinedList = joiner.join(
        str(itemFromList) for itemFromList in inputList)
    return stringJoinedList


def findDigits(stringText):
    '''Takes a string of text and returns
    all the digits found in the string
    and returns a list of those digits
    '''
    textList = []
    for character in stringText:
        if character.isdigit():
            textList.append(character)
    return textList


def listFields(featureClass):
    fields = [field.name for field in arcpy.ListFields(featureClass) if not field.required]
    return fields


def deleteUneededFields(featureClass, fieldsToKeep):
    '''Provide a list of fields to keep within the featureclass
    and all other fields that are not required will be deleted
    '''
    fieldsToDelete = [
        field.name for field in arcpy.ListFields(featureClass)
        if field.name not in fieldsToKeep
        and not field.required]
    arcpy.DeleteField_management(featureClass, fieldsToDelete)


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


def findAllFeatureClasses(folder):
    '''Returns a list of all the feature classes
    that are within the provided folder and any
    addtional subfolders
    '''
    featureClasses = []
    walk = arcpy.da.Walk(folder, datatype="FeatureClass")

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            featureClasses.append(os.path.join(dirpath, filename))
    return featureClasses
