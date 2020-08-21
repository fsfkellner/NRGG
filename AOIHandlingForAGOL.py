import arcpy
import os


class FeatureClassForAGOLFiltering:
    """A class to handle an area of interest
    feature class for spatial filtering
    an AGOL feature service
    """

    def __init__(self, areaOfInterestFeatureClassPath):
        self.pathToAOI = areaOfInterestFeatureClassPath

    def AOIToGCSWGS84InDefaultGDB(self):
        """Takes and area of interest and projects the
        data to a Geographic Coordinate System of
        WGS_84 into users current default workspace
        """
        projection = """GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',
        SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],
        UNIT['Degree',0.0174532925199433]]"""

        outputFile = os.path.join(
            arcpy.env.workspace, "projectedAreaofInterest")
        arcpy.Project_management(self.pathToAOI, outputFile, projection)
        return outputFile

    def getVerticesOfProjectedAOI(self, projectedAreaOfInterest):
        arcpy.MakeFeatureLayer_management(
            projectedAreaOfInterest, "projectedAreaofInterest")
        areaOfInterestVertices = []
        cursor = arcpy.da.SearchCursor(
            "projectedAreaofInterest", ["OID@", "SHAPE@"])
        locationOfShapeFieldInReturnedCursorRow = 1
        for row in cursor:
            for points in row[locationOfShapeFieldInReturnedCursorRow]:
                for point in points:
                    if point:
                        areaOfInterestVertices.append([point.X, point.Y])
        return areaOfInterestVertices

    def makeAOIVerticesDictionaryForRESTURL(self, areaOfInterestVertices):
        areaOfInterestVerticesDictionary = {}
        areaOfInterestVerticesDictionary["rings"] = [areaOfInterestVertices]
        # areaOfInterestVerticesDictionary["spatialReference"] = {"wkid": 4326}
        return areaOfInterestVerticesDictionary
