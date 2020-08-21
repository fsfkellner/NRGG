import urllib
import arcpy
from HelperFunctions import listStringJoiner
from URLHandling import (
    urlRequest,
    errorMessageGenerator,
    jsonObjectErrorHandling
)


class Python2RESTAPI:
    """Leverages the ESRI Rest API to return information about feature services
    and REST URL endpoints for AGOL using Python 2.7 because the FS is still
    using ArcGIS Desktop at the Virtual Data Center
    """

    def __init__(self, AGOLFeatureServiceURL,
                 AGOLToken, AGOLFeatureServiceLayerNumber):
        self.url = AGOLFeatureServiceURL
        self.token = AGOLToken
        self.layerNumber = AGOLFeatureServiceLayerNumber

    def layerHasPhotoAttachments(self):
        """Checks to see if an AGOL Feature Service has attachments."""

        errorText = '''when trying to see if the input feature service
            has attachments or the input feature service does
            not allow attachments.'''

        errorMessage = errorMessageGenerator(errorText)
        areThereAttachmentsURL = urlRequest(
            "{}/{}?&f=json&token={}".format(
                self.url,
                self.layerNumber,
                self.token
                )
        )
        if jsonObjectErrorHandling(areThereAttachmentsURL,
                                   "hasAttachments", errorMessage):
            return True

    def name(self):
        """Returns the name of the AGOL Feature
         Service from the input AGOL Feature Service URL
        """

        errorText = '''There was an error trying to retreive
        the name of the input feature service'''
        errorMessage = errorMessageGenerator(errorText)

        AGOLFeatureServiceNameURL = urlRequest(
            "{0}?&f=json&token={1}".format(self.url, self.token)
        )
        AGOLFeatureServiceName = jsonObjectErrorHandling(
            AGOLFeatureServiceNameURL, "layers", errorMessage)
        AGOLFeatureServiceName = AGOLFeatureServiceName[0]
        AGOLFeatureServiceName = AGOLFeatureServiceName["name"].encode(
            'utf-8',
            'ignore'
            )
        return AGOLFeatureServiceName

    def getObjectIDs(self):
        """Returns the ObjectIDs for each item in the AGOL Feature Service.
        it is best to use this method as ObjectIDs may not be sequential.
        for example the ObjectIDs could number 1,2,3,5,6,12,13... this
        is a result of delete field collected data after syncing
        """

        errorText = '''when trying to retrieve the ObjectIds
        for the input feature service'''
        errorMessage = errorMessageGenerator(errorText)

        featureServiceObjectIDsURL = urlRequest(
            "{0}/{1}/query?where=1=1&returnIdsOnly=true&f=json&token={2}".
            format(self.url, self.layerNumber, self.token))
        featureServiceObjectIDs = jsonObjectErrorHandling(
            featureServiceObjectIDsURL, "objectIds", errorMessage)
        featureServiceObjectIDs = featureServiceObjectIDs[:]
        featureServiceObjectIDs = listStringJoiner(featureServiceObjectIDs)
        return featureServiceObjectIDs

    def getObjectIDsInAOI(
            self, areaOfInterestVerticesDictionary):
        """Returns the ObjectIDs for each item in the AGOL Feature Service that
        that fall within an end user provided area of interst.
        it is best to use this method as ObjectIDs may not be sequential.
        for example the ObjectIDs could number 1,2,3,5,6,12,13... this
        is a result of delete field collected data after syncing
        """

        errorText = '''when trying to find points
        that fall within the provided area of interest'''
        errorMessage = errorMessageGenerator(errorText)

        urlEncodedParameters = urllib.urlencode(
            {
                "geometryType": "esriGeometryPolygon",
                "spatialRel": "esriSpatialRelContains",
                "inSR": 4326,
                "geometry": areaOfInterestVerticesDictionary
            }
        )
        queryAGOLURL = 'query?where=1=1&returnIdsOnly=true&f=json&token='
        urlRequestString = '{}/{}/{}{}'.format(
            self.url, self.layerNumber, queryAGOLURL, self.token)

        featureServiceObjectIDs = urlRequest(urlRequestString,
                                             urlEncodedParameters)

        featureServiceObjectIDs = jsonObjectErrorHandling(
            featureServiceObjectIDs, "objectIds", errorMessage)

        featureServiceObjectIDs = featureServiceObjectIDs[:]
        featureServiceObjectIDs = listStringJoiner(featureServiceObjectIDs)
        return featureServiceObjectIDs

    def queryObjectIDsForAttachments(self, AGOLfeatureServiceOjbectIDs):
        """Returns the ObjectIds for each feature in the AGOL Feature Service
        which has attachments.
        """

        errorText = '''when trying to retrieve objectIDs for
        input feature service'''
        errorMessage = errorMessageGenerator(errorText)

        urlEncodedParameters = urllib.urlencode(
            {"objectIds": AGOLfeatureServiceOjbectIDs}
        )
        urlRequestString = "{}/{}/queryAttachments?&f=json&token={}".format(
            self.url, self.layerNumber, self.token)

        featureServiceObjectIDsThatHaveAttachmentsURL = urlRequest(
            urlRequestString, urlEncodedParameters)

        featureServiceObjectIDswithAttacments = jsonObjectErrorHandling(
            featureServiceObjectIDsThatHaveAttachmentsURL,
            "attachmentGroups", errorMessage)

        featureServiceObjectIDswithAttacments = [
            objectIDWithPhoto["parentObjectId"]
            for objectIDWithPhoto in featureServiceObjectIDswithAttacments
        ]

        featureServiceObjectIDswithAttacments = listStringJoiner(
            featureServiceObjectIDswithAttacments)

        return featureServiceObjectIDswithAttacments
