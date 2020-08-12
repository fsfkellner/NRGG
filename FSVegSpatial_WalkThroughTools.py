
def unzipAGOLReplicaGDBAndRenameToFSVeg(pathOfZippedReplicaGDB, outputLocation):
    with zipfile.ZipFile(pathOfZippedReplicaGDB, "r") as zipGDB:
        zipGDB = zipfile.ZipFile(pathOfZippedReplicaGDB, "r")
        uniqueAGOLGenerateReplicaGDBName = zipGDB.namelist()[0].split(r"/")[0]
        zipGDB.extractall(outputLocation)
        arcpy.Rename_management(
            outputLocation + "/" + uniqueAGOLGenerateReplicaGDBName, "FSVeg_Spatial_WT"
        )

def DeleteUneededFiedsFromFinalFeatureclass(finalFeatureClass):
    listOfFieldsToKeep = []
    fieldsToDelete = [
        field.name
        for field in arcpy.ListFields(finalFeatureClass)
        if field.name not in listOfFieldsToKeep
    ]
    arcpy.DeleteField_management("finalFeatureClass", fieldsToDelete)

def renamePlotsToFSVeg_Spatial_WT_PhotosInGDB(outputLocation):
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    # I use FC to FC here rather than rename as it allows for all the attachment
    # files inthe GDB to be called FSVeg_Spatial_WT_Photos and allows for
    # delteting of fields that Natalie and Renate did now want the end user to see
    arcpy.arcpy.FeatureClassToFeatureClass_conversion(
        "plots", outputLocation + "/FSVeg_Spatial_WT.gdb", "FSVeg_Spatial_WT_Photos"
    )
    
    arcpy.Delete_management(outputLocation + "/FSVeg_Spatial_WT.gdb/plots")
    arcpy.Delete_management(outputLocation + "/FSVeg_Spatial_WT.gdb/plots__ATTACH")
    arcpy.Delete_management(outputLocation + "/FSVeg_Spatial_WT.gdb/plots__ATTACHREL")

def createDictionaryOfFSVegGlobadIDsPlotSettingAndPlotNumber(outputLocation):
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    cursor = arcpy.da.SearchCursor(
        "FSVeg_Spatial_WT_Photos", ["GlobalID", "pl_setting_id", "plot_number_1"]
    )
    FSVegGlobalIDDictionary = {}
    for row in cursor:
        if row[1] is not None and row[1].isdigit():
            key = row[0]
            vals = row[1:]
            FSVegGlobalIDDictionary[key] = vals
    del cursor
    del row
    return FSVegGlobalIDDictionary


def writeAttachedPhotosAndMakeDictionaryOfFSVegPhotoNames(
    outputLocation, FSVegGlobalIDDictionary
):
    if os.path.exists(outputLocation + "//FSVeg_Spatial_WT_Photos"):
        pass
    else:
        os.mkdir(outputLocation + "//FSVeg_Spatial_WT_Photos")
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    photoNameDictionary = {}
    with arcpy.da.SearchCursor(
        "FSVeg_Spatial_WT_Photos__ATTACH", ["DATA", "ATT_NAME", "REL_GLOBALID"]
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
                stringStartLocation = attachmentName.find("photo_plot")
                if (
                    attachmentName[stringStartLocation + 10 : stringStartLocation + 11]
                    == "-"
                ):
                    filename = fileNumber + "_1.jpg"
                else:
                    filename = (
                        fileNumber
                        + "_"
                        + attachmentName[
                            stringStartLocation + 11 : stringStartLocation + 12
                        ]
                        + ".jpg"
                    )
                open(
                    outputLocation + "//FSVeg_Spatial_WT_Photos" + os.sep + filename,
                    "wb",
                ).write(attachment.tobytes())
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

def addPhotoNameFieldAndPopulateFinalFSVegFeatureClass(
    outputLocation, photoNameDictionary
):
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    arcpy.AddField_management(
        "FSVeg_Spatial_WT_Photos", "PhotoNames", "TEXT", "#", "#", 250
    )
    edit = arcpy.da.Editor(
        outputLocation + "/FSVeg_Spatial_WT.gdb"
    )  # dirname of the fc is the db name
    edit.startEditing(False, False)  # check these setting for your environment
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


def DeleteUneededFiedsFromFinalFSVegFeatureclass(outputLocation):
    arcpy.env.workspace = outputLocation + "/FSVeg_Spatial_WT.gdb"
    listOfFieldsToKeep = [
        "globalid",
        "pl_setting_id",
        "plot_number_1",
        "photo_1_text",
        "PhotoNames",
    ]
    fieldsToDelete = [
        field.name
        for field in arcpy.ListFields("FSVeg_Spatial_WT_Photos")
        if field.name not in listOfFieldsToKeep and not field.required
    ]
    arcpy.DeleteField_management("FSVeg_Spatial_WT_Photos", fieldsToDelete)

def deleteFeaturesWithIncorrectSettingIDValues(outputLocation):
    arcpy.MakeFeatureLayer_management(outputLocation + os.sep + "FSVeg_Spatial_WT.gdb" + os.sep + "FSVeg_Spatial_WT_Photos", "FSVeg_Spatial_WT_Photos")
    arcpy.SelectLayerByAttribute_management('FSVeg_Spatial_WT_Photos', "NEW_SELECTION", 'PhotoNames IS NULL')
    arcpy.DeleteFeatures_management("FSVeg_Spatial_WT_Photos")

def alterPlotSettingIDFieldName(outputLocation):
    arcpy.MakeTableView_management(outputLocation + os.sep + "FSVeg_Spatial_WT.gdb" + os.sep + "FSVeg_Spatial_WT_Photos", "FSVeg_Spatial_WT_PhotosTable")
    arcpy.AlterField_management("FSVeg_Spatial_WT_PhotosTable", "pl_setting_id", "Setting_ID", "Setting_ID")