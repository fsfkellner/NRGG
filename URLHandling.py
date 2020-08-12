import arcpy
import urllib
import json


def urlRequest(inputUrl, *urlParameters):
    '''urlRequest(str, str(dictionary)) -> json object
    Takes input URL and optional urlencode parameters and returns
    a urllib.urlopen() json object. If open fails
    error handling occurs.'''

    try:
        urlurlResponse = urllib.urlopen(
            inputUrl,
            urlParameters
            ).read()
        return urlurlResponse
    except Exception as e:
        errorText = '''Unable to make URL request. Check your internet
        connection or input URL and try again.'''
        arcpy.AddMessage(errorMessageGenerator(errorText, traceBackError=e))
        exit()


def errorMessageGenerator(textForErrorMessage, traceBackError=''):

    '''errorMessageGenerator(string) -> string
    takes and input string and formats it to boiler-plate
    error message. The only reason this exists is because
    Forest Service End users Do not like Traceback error
    messages.
    '''

    errorText = '''There was an error {}.
    If you believe there was a mistake
    entering parameters please try the tool again. \
    \
    \
    {}'''.format(textForErrorMessage, traceBackError)
    return errorText


def jsonObjectErrorHandling(urlResponse, keyValue, errorMessage):
    try:
        return json.loads(urlResponse)[keyValue]
    except Exception as e:
        arcpy.AddMessage(errorMessageGenerator(errorMessage, traceBackError=e))
        exit()
