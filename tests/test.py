# import os
import unittest
# import arcpy
import sys
from mock import patch
import urllib

sys.path.append(r'C:\Data')
from NRGG import FeatureClassForAGOLFiltering
from NRGG import errorMessageGenerator
from NRGG import listStringJoiner
from NRGG import jsonObjectErrorHandling

projectedVerticesList = [
    [-110.74940200956502, 46.89382592506291],
    [-110.75298764360036, 46.89351164692039],
    [-110.75751611406332, 46.894125919153566],
    [-110.75807324408873, 46.89928294590163],
    [-110.75418761696278, 46.9030542896121],
    [-110.74911630152633, 46.898754385980055],
    [-110.74940200956502, 46.89382592506291]
]


projectedVerticesDictionary = {
    'rings': [
        [
            [-110.74940200956502, 46.89382592506291],
            [-110.75298764360036, 46.89351164692039],
            [-110.75751611406332, 46.894125919153566],
            [-110.75807324408873, 46.89928294590163],
            [-110.75418761696278, 46.9030542896121],
            [-110.74911630152633, 46.898754385980055],
            [-110.74940200956502, 46.89382592506291]
        ]
    ]
}
urlResponse = '{"token":"5QBG6IERjwNyZdiDwqUjgKvVUn47J5bjklqN8D37ZQbDTfI6V6rolwy3daz18-S1oFL8j0eOTCaX1xgjRQGceJoRA4FJ9c9WEDrDWBVSkg4UawWlDDYmzpyRiwnwujsavjFzNfBTK6UFJa1iAWQT5Q..","expires":1597885097466,"ssl":true}'
jsonReturn = '''5QBG6IERjwNyZdiDwqUjgKvVUn47J5bjklqN8D37ZQbDTfI6V6rolwy3daz18-S1oFL8j0eOTCaX1xgjRQGceJoRA4FJ9c9WEDrDWBVSkg4UawWlDDYmzpyRiwnwujsavjFzNfBTK6UFJa1iAWQT5Q..'''
testErrorMessage = 'There was an error test text.\n    If you believe there was a mistake\n    entering parameters please try the tool again.             This is the Traceback'

# AOIFilePath = r'C:\Data\FSVeg_Sp_WT_AGOL_PhototDownload\tests\test_data.gdb\testAOI'
AOIFilePath = r'C:\Data\NRGG\tests\test_data.gdb\testAOI'
projectedTestAOIFilePath = r'C:\Data\NRGG\tests\test_data.gdb\projectedTestAOI'

AOI = FeatureClassForAGOLFiltering(AOIFilePath)


class TestFSVegPhotoDowloadTools(unittest.TestCase):

    def test_urlRequest(self):
        with patch('urllib.urlopen') as mock_urllib:
            

    def test_listStringJoiner(self):
        stringJoinedListFromFunction = listStringJoiner([1, 2, 3, 4])
        self.assertEqual(stringJoinedListFromFunction, '1,2,3,4')

    def test_errorMessageGenerator(self):
        errorMessageFromFunction = errorMessageGenerator(
            'test text', traceBackError='This is the Traceback')
        self.assertEqual(testErrorMessage, errorMessageFromFunction)

    def test_getVerticesOfProjectedAOI(self):
        verticesList = AOI.getVerticesOfProjectedAOI(projectedTestAOIFilePath)
        self.assertEqual(projectedVerticesList, verticesList)

    def test_makeAOIVerticesDictionaryForRESTURL(self):
        verticesDictionary = AOI.makeAOIVerticesDictionaryForRESTURL(
            projectedVerticesList)
        self.assertEqual(projectedVerticesDictionary, verticesDictionary)

    def test_jsonObjectErrorHandling(self):
        jsonValue = jsonObjectErrorHandling(
            urlResponse, "token", 'Hairy Chicken')
        self.assertEqual(jsonValue, jsonReturn)
