import arcpy


def listFields(featureClass, textValue=''):
    '''Returns a list of all the non required field names within
    an attribute table of a featureclass. Option textValue can
    be used to limit the returned results
    '''
    fields = [
        field.name for field in arcpy.ListFields(featureClass)
        if textValue in field.name and not field.required]
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


def returnAllValuesFromField(featureClass, field):
    '''Taks an input field and returns a sorted list off
    all the values in a field from an table or feature class attribute table
    '''
    allValues = [row[0] for row in arcpy.da.SearchCursor(featureClass, field)]
    allValues.sort()
    return allValues


def uniqueValuesFromFeatureClassField(featureClass, field):
    '''Returns the unique values from a
    fields in a feature class
    '''
    with arcpy.da.SearchCursor(featureClass, field) as cursor:
        uniqueValues = list(set(row[0] for row in cursor))
    return uniqueValues
