import arcpy
import urllib
import json


def errorMessageGenerator(textForErrorMessage, traceBackError=''):

    '''errorMessageGenerator(string) -> string
    takes and input string and formats it to boiler-plate
    error message. The only reason this exists is because
    Forest Service End users do not like Traceback error
    messages.
    '''

    errorText = '''There was an error {}.
        If you believe there was a mistake
        entering parameters please
        try the tool again. \
            \
        {}'''.format(textForErrorMessage, traceBackError)
    return errorText


def urlRequest(inputUrl, *urlParameters):
    '''urlRequest(str, str(dictionary)) -> json object
    Takes input URL and optional urlencoded parameters and returns
    a urllib.urlopen() json object. If open fails
    error handling occurs.'''

    errorText = '''Unable to make URL request.
        Check your internet connection or input URL and try again.'''
    try:
        urlResponse = urllib.urlopen(inputUrl, "".join(urlParameters)).read()
        return urlResponse
    except Exception as e:
        errorMessage = errorMessageGenerator(errorText, e)
        arcpy.AddMessage(errorMessage)
        exit()


def jsonObjectErrorHandling(urlResponse, keyValue, errorText):
    try:
        valueFromJson = json.loads(urlResponse)[keyValue]
        return valueFromJson
    except Exception as e:
        errorMessage = errorMessageGenerator(errorText, e)
        arcpy.AddMessage(errorMessage)
        exit()


def generateAGOLToken(AGOLUsername, AGOLPassword):
    """Generates a Token for use with the REST
    API for ArcGIS Online
    """
    errorText = '''generating an AGOL token.
      It is likely that you entered an incorrect
      username or password'''
    errorMessage = errorMessageGenerator(errorText)
    parameters = urllib.urlencode(
        {
            "username": AGOLUsername,
            "password": AGOLPassword,
            "client": "referer",
            "referer": "https://www.arcgis.com",
            "expiration": 120,
            "f": "json",
        }
    )
    tokenURL = "https://www.arcgis.com/sharing/rest/generateToken?"
    tokenUrlResponse = urlRequest(tokenURL, parameters)
    AGOLToken = jsonObjectErrorHandling(
        tokenUrlResponse, "token", errorMessage)

    return AGOLToken
