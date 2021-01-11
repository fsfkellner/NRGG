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


def findDigits(stringText):
    '''Takes a string of text and returns
    all the digits found in the string
    and returns a list of those digits
    '''
    textList = []
    for character in stringText:
        if character.isdigit():
            textList.append(character)
    return textList


def returnDuplicates(yourList):
    '''Takes an input list and returns
    a list of only the duplicate values
    '''
    notDuplicate = set()
    isDuplicate = set()
    notDuplicate_add = notDuplicate.add
    isDuplicate_add = isDuplicate.add
    for item in yourList:
        if item in notDuplicate:
            isDuplicate_add(item)
        else:
            notDuplicate_add(item)
    return list(isDuplicate)
