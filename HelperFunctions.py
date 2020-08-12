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


def errorMessageGenerator(textForErrorMessage):
    '''errorMessageGenerator(string) -> string
    takes and input string and formats it to boiler-plate
    error message.
    '''

    errorText = '''There was an error {}.
    If you believe there was a mistake
    entering parameters please try the tool again.'''.format(textForErrorMessage)
    return errorText
