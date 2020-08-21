import os
import urllib
import requests
import json
import time
import arcpy
from URLHandling import (
    urlRequest,
    errorMessageGenerator,
    jsonObjectErrorHandling
)


def getStatusURLForAGOLReplica(
        AGOLFeatureServiceName, AGOLFeatureServiceURL, AGOLToken,
        AGOLFeatureServiceLayerNumber, AGOLFeatureServiceObjectIDs):

    errorText = '''trying to retrieve the status URL for the replica
    of the AGOL Feature Service'''
    errorMessage = errorMessageGenerator(errorText)
    replicaParameters = urllib.urlencode(
        {
            "name": AGOLFeatureServiceName,
            "layers": AGOLFeatureServiceLayerNumber,
            "layerQueries": {
                AGOLFeatureServiceLayerNumber:
                {
                    "where": "OBJECTID IN (" + AGOLFeatureServiceObjectIDs + ")"
                }
            },
            "transportType": "esriTransportTypeUrl",
            "returnAttachments": True,
            "returnAttachmentsDatabyURL": True,
            "syncDirection": "bidirectional",
            "attachmentsSyncDirection": "bidirectional",
            "async": True,
            "syncModel": "none",
            "dataFormat": "filegdb",
        }
    )

    createFeatureServieReplicaURL = "{}/createReplica/?f=json&token={}".format(
        AGOLFeatureServiceURL, AGOLToken)
    featureServiceCreateRepilcaRequest = urlRequest(
        createFeatureServieReplicaURL, replicaParameters)

    featureServiceReplicaStatusUrl = jsonObjectErrorHandling(
        featureServiceCreateRepilcaRequest, "statusUrl", errorMessage)

    return featureServiceReplicaStatusUrl


def waitForAGOLReplica(featureServiceReplicaStatusUrl,
                                     AGOLToken):
    timer = 0
    status = json.loads(
        urllib.urlopen(
            "{}?f=json&token={}".format(
                featureServiceReplicaStatusUrl, AGOLToken)
        ).read()
    )
    while status["resultUrl"] == "":
        time.sleep(10)
        timer += 10
        status = json.loads(
            urllib.urlopen(
                "{}?f=json&token={}".format(
                    featureServiceReplicaStatusUrl, AGOLToken
                )
            ).read()
        )
        if timer > 1000:
            raise Exception(
                '''It took too long to make the AGOL Repica.
                Try again at a different time'''
            )
        if status["status"] in ("Failed", "CompletedWithErrors"):
            raise Exception(
                '''There was an error creating the AGOL Replica.
                Check your inputs and try again'''
            )
    else:
        featureServiceReplicaResultURL = status["resultUrl"]
        return featureServiceReplicaResultURL


def downloadAGOLReplicaInFGDB(
        AGOLReplicaResultURL, AGOLToken,
        AGOLFeatureServiceName, outputLocation):

    urlResponse = requests.get(
        "{0}?token={1}".format(AGOLReplicaResultURL, AGOLToken), stream=True
    )
    nameOfAGOLReplicaZipFile = unicode("{}.zip".format(AGOLFeatureServiceName))
    fullPathAGOLReplicaOfZipFile = os.path.join(
        outputLocation, nameOfAGOLReplicaZipFile
    )
    with open(fullPathAGOLReplicaOfZipFile, "wb") as AGOLReplicaOfZipFile:
        sizeOfFile = urlResponse.headers.get("content-length")
        if sizeOfFile is None:
            AGOLReplicaOfZipFile.write(urlResponse.content)
        else:
            sizeOfFile = int(sizeOfFile)
        chunk = 1
        for data in urlResponse.iter_content(chunk_size=sizeOfFile / 10):
            arcpy.AddMessage(
                str(int((float(chunk) / float(sizeOfFile)) * 100))
                + "% of the file has downloaded"
            )
            AGOLReplicaOfZipFile.write(data)
            chunk += sizeOfFile / 10
    return fullPathAGOLReplicaOfZipFile
