import json
from typing import Callable
class StructureDef:
    """An object for storing a structure definition from Syntax file better, so errors can be found faster."""
    def __init__(self, definition: dict):
        self.name: str = definition["name"]
        self.structure: list[str] = definition["structure"]

class LanguageSyntax:
    def __init__(self, jsonDict: dict[str,list[dict]]):
        self.dict: dict[str,list[StructureDef]] = {}
        for structure, structureDefinitions in jsonDict.items():
            self.dict[structure] = [StructureDef(structureDefinition) for structureDefinition in structureDefinitions]

class LanguageLexicon:
    def __init__(self, jsonDict:dict[str,list[dict]]):
        self.dict: dict[str, list[LexiconWordObject]] = {}
        for type, words in jsonDict.items():
            self.dict[type] = [LexiconWordObject(word) for word in words]

class LexiconWordObject:
    def __init__(self, jsonDict: dict):
        try:
            self.root: str = jsonDict["root"]
            self.meaning: str = jsonDict.get("meaning", None)
            self.conjugations: list[str] = jsonDict.get("conjugations",[])
        except KeyError:
            raise ValueError(f"languageLexicon.json contains invalid word definition: {jsonDict}")

def wierdFunctionINeed(inputList: list[str], n: int):
    """
    function that returns a list of all the ways to split a list into n lists.\n
    I already hate this project.\n
    I had to rewrite this godforsaken garbage for n != 3\n
    I hate my life.\n
    DONOTEDIT
    TODO: Rename this and the other function to something better.
    """
    returnList: list[list[list[str]]] = []
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
    """Checks if the text (list of words) matches any of the structures in languageSyntax or words in langyageLexicon.\n
    Returns None if No."""
    if type not in languageSyntax.dict.keys():
        if type not in languageLexicon.dict.keys():
            raise ValueError(f"languageSyntax file contains unsupported Structure or word class: {type}")
        textStr = " ".join(text).lower()
        if textStr in [word.root for word in languageLexicon.dict[type]] or True in [(textStr in word.conjugations) for word in languageLexicon.dict[type]]:
            print(f"{textStr} is a valid {type}")
            return (type, textStr)
        else:
            print(f"{textStr} isn't a valid {type}")
            return None
    for structure in languageSyntax.dict[type]:
        #use wierdFunctionINeed to split text into various combinations, and check them against the structure.
        textVariations = wierdFunctionINeed(text,len(structure.structure))
        for variation in textVariations:
            returnTuplesList: list[tuple] = []
            for itemToBeChecked,element in zip(variation, structure.structure):
                #YAY! Recursion. :(
                if element[0] == "?":
                    element = element.removeprefix("?")
                    #Make this optional
                if element[0] == "*":
                    element = element.removeprefix("*")
                    #This part will be complicated.
                checkStructureResult = checkStructure(itemToBeChecked,element)
                if checkStructureResult is None:
                    break
                else:
                    returnTuplesList.append(checkStructureResult)
            else:
                return (structure.name,returnTuplesList)
    return None
    #TODO: Use the object constructor for the syntax to make this more predictable. (mostly done)
    #Make this return something like a tuple of something to identify the structure found, or raise an exception if none is found.

with open("languageSyntax.json") as f:
    languageSyntax = LanguageSyntax(json.load(f))
with open("languageLexicon.json") as f:
    languageLexicon = LanguageLexicon(json.load(f))
with open("knowledge.json") as f:
    knowledge = json.load(f)

class Bot:
    def __init__(self, UserInput: Callable[[],str], output: Callable[[str],None]):
        self.input: Callable[[],str] = UserInput
        self.output = output
    
    def run(self) -> None:
        while True:
            prompt: str = self.input()
            if prompt in ["STOP","stop","QUIT"]:
                break
            wordsList = prompt.split()
            print(checkStructure(wordsList, "sentence"))