import json

class LanguageSyntax:
    def __init__(self, jsonDict: dict[str,list[list[str]]]):
        self.dict: dict[str,list[list[str]]] = {}
        for structure, structureDefinition in jsonDict.items():
            self.dict[structure] = structureDefinition

def wierdFunctionINeed(inputList: list[str], n: int):
    """
    function that returns a list of all the ways to split a list into n lists.\n
    I already hate this project.\n
    edit: I had to rewrite this godforsaken garbage for n != 3\n
    I hate my life.\n
    DONOTEDIT
    """
    returnList: list[list] = []
    for numbersPossibility in functionThatHelpsTheAbove(n,len(inputList)):
        iterator = iter(inputList)
        possibility: list[list[str]] = []
        for number in numbersPossibility:
            possibility.append([])
            for i in range(number):
                try:
                    possibility[-1].append(next(iterator))
                except StopIteration:
                    break
        returnList.append(possibility)
    return returnList

def functionThatHelpsTheAbove(n:int, i:int):
    """
    Another weird function using recursiveness to generate all sets of n positive integers (not including 0) that add up to i.\n
    Fuck my life and the person I have chosen to be.\n
    DO NOT TOUCH IF NOT BROKEN
    """
    returnList: list[list[int]] = []
    if n == 2:
        for j in range(1,i):
            returnList.append([j,i-j])
    else:
        for j in range(1,i):
            for otherNumsPossibility in functionThatHelpsTheAbove(n-1,i-j):
                possibility = [j]
                for number in otherNumsPossibility:
                    possibility.append(number)
                returnList.append(possibility)
    return returnList

def checkStructure(text: list[str], type: str):
    if type not in languageSyntax.dict.keys():
        raise NotImplementedError("""This isn't a language structure type. I will soon 
                                  implement this to look for word classes, but not today.""")
    for structure in languageSyntax.dict[type]:
        textVariations = wierdFunctionINeed(text,len(structure))
        print(textVariations,structure)
        for variation,element in zip(textVariations, structure):
                #YAY! Recursion. :ε
                if element[0] == "?":
                    element = element.removeprefix("?")
                    #Make this optional
                checkStructure(variation,element)
        #use wierdFunctionINeed to split text into various combinations, and check them against the structure.
        #TODO: Add an object constructor for the syntax to make this more predictable.
        #Make this return something like a tuple of something to identify the structure found, or raise an exception if none is found.

#define a custom exception (structureNotFoundError)
with open("languageSyntax.json") as f:
    languageSyntax = LanguageSyntax(json.load(f))
with open("languageLexicon.json") as f:
    languageLexicon = json.load(f)

prompt = input("Input: ")
wordsList = prompt.split()
#catch exceptions here
checkStructure(wordsList, "sentence")
