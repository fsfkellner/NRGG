import arcpy
import os
import zipfile


def unzipAGOLReplicaGDBAndRenameToFSVeg(
        pathOfZippedReplicaGDB, outputLocation):
    with zipfile.ZipFile(pathOfZippedReplicaGDB, "r") as zipGDB:
        zipGDB = zipfile.ZipFile(pathOfZippedReplicaGDB, "r")
        uniqueAGOLGeneratedReplicaGDBName = zipGDB.namelist()[0].split(r"/")[0]
        zipGDB.extractall(outputLocation)
        arcpy.Rename_management(
            os.path.join(outputLocation, uniqueAGOLGeneratedReplicaGDBName),
            "FSVeg_Spatial_WT")


def renamePlotsFilesToFSVeg(outputLocation):
    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')
    arcpy.env.workspace = FSVegGDBPath
    # I use FC to FC here rather than rename as it allows
    # for all the attachment files inthe GDB
    # to be called FSVeg_Spatial_WT_Photos and allows for
    # delteting of fields that Natalie and Renate
    # did now want the end user to see
    arcpy.arcpy.FeatureClassToFeatureClass_conversion(
        "plots", FSVegGDBPath,
        "FSVeg_Spatial_WT_Photos")

    plotFilesToDelete = ['plots', 'plots__ATTACH', 'plots__ATTACHREL']
    for plotFile in plotFilesToDelete:
        arcpy.Delete_management(os.path.join(FSVegGDBPath, plotFile))


def createDictOfFSVegIDsAndPlots(outputLocation):
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    cursor = arcpy.da.SearchCursor(
        "FSVeg_Spatial_WT_Photos",
        ["GlobalID", "pl_setting_id", "plot_number_1"])

    FSVegGlobalIDDictionary = {}
    for row in cursor:
        if row[1] is not None and row[1].isdigit():
            key = row[0]
            vals = row[1:]
            FSVegGlobalIDDictionary[key] = vals
    del cursor
    del row
    return FSVegGlobalIDDictionary


def writeAttachedPhotosMakeDictOfPhotoNames(
        outputLocation, FSVegGlobalIDDictionary):
    photoFolder = os.path.join(outputLocation, 'FSVeg_Spatial_WT_Photos')
    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')

    if os.path.exists(photoFolder):
        pass
    else:
        os.mkdir(photoFolder)
    arcpy.env.workspace = FSVegGDBPath
    photoNameDictionary = {}
    with arcpy.da.SearchCursor(
        "FSVeg_Spatial_WT_Photos__ATTACH",
        ["DATA", "ATT_NAME", "REL_GLOBALID"]
    ) as cursor:
        for row in cursor:
            if row[2] in FSVegGlobalIDDictionary:
                attachment = row[0]
                fileNumber = (
                    str(FSVegGlobalIDDictionary[row[2]][0])
                    + "_plot"
                    + str(FSVegGlobalIDDictionary[row[2]][1])
                )
                attachmentName = row[1].encode('utf-8', 'ignore')
                hyphenStart = attachmentName.find("photo_plot")
                hyphenStart = hyphenStart + 10
                hyphenEnd = hyphenStart + 1
                potentialHyphen = attachmentName[
                    hyphenStart:hyphenEnd]
                plotNumberStart = hyphenStart + 1
                plotNumberEnd = hyphenEnd + 1
                addtionalPlotNumber = attachmentName[
                    plotNumberStart:plotNumberEnd]
                if potentialHyphen == '-':
                    filename = fileNumber + "_1.jpg"
                else:
                    filename = '{}_{}.jpg'.format(
                        fileNumber, addtionalPlotNumber)

                photoFilePath = os.path.join(photoFolder, filename)
                open(photoFilePath, "wb",).write(attachment.tobytes())
                if row[2] not in photoNameDictionary:
                    photoNameDictionary[row[2]] = [filename]
                else:
                    photoNameDictionary[row[2]].append(filename)
                del row
                del fileNumber
                del filename
                del attachment
            else:
                pass
    return photoNameDictionary


def addPhotoNameFieldAndPopulate(
        outputLocation, photoNameDictionary):

    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')
    arcpy.env.workspace = FSVegGDBPath
    arcpy.AddField_management(
        "FSVeg_Spatial_WT_Photos", "PhotoNames", "TEXT", "#", "#", 250
    )
    edit = arcpy.da.Editor(FSVegGDBPath)
    edit.startEditing(False, False)
    edit.startOperation()
    cursor = arcpy.da.UpdateCursor(
        "FSVeg_Spatial_WT_Photos", ["GlobalID", "PhotoNames"]
    )
    for row in cursor:
        if row[0] in photoNameDictionary:
            row[1] = ",".join(photoNameDictionary[row[0]])
        cursor.updateRow(row)
    edit.stopOperation()
    edit.stopEditing(True)


def deleteFiedsFromFSVegPhotoFeatureClass(outputLocation):
    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')
    arcpy.env.workspace = FSVegGDBPath
    listOfFieldsToKeep = [
        "globalid",
        "pl_setting_id",
        "plot_number_1",
        "photo_1_text",
        "PhotoNames"
    ]
    fieldsToDelete = [
        field.name
        for field in arcpy.ListFields("FSVeg_Spatial_WT_Photos")
        if field.name not in listOfFieldsToKeep and not field.required
    ]
    arcpy.DeleteField_management("FSVeg_Spatial_WT_Photos", fieldsToDelete)


def deleteFeaturesWithIncorrectSettingIDValues(outputLocation):
    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')
    arcpy.MakeFeatureLayer_management(os.path.join(FSVegGDBPath,
        "FSVeg_Spatial_WT_Photos"),"FSVeg_Spatial_WT_Photos")
    arcpy.SelectLayerByAttribute_management('FSVeg_Spatial_WT_Photos',
        "NEW_SELECTION", 'PhotoNames IS NULL')
    arcpy.DeleteFeatures_management("FSVeg_Spatial_WT_Photos")


def alterPlotSettingIDFieldName(outputLocation):
    FSVegGDBPath = os.path.join(outputLocation, 'FSVeg_Spatial_WT.gdb')
    arcpy.MakeTableView_management(os.path.join(
            FSVegGDBPath, "FSVeg_Spatial_WT_Photos"),
        "FSVeg_Spatial_WT_PhotosTable")
    arcpy.AlterField_management("FSVeg_Spatial_WT_PhotosTable",
        "pl_setting_id", "Setting_ID", "Setting_ID")