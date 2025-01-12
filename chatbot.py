import json
from typing import Callable, Any
import string

class StructureDef:
    """An object for storing a structure definition from Syntax file better, so errors can be found faster."""
    def __init__(self, definition: dict):
        self.name: str = definition["name"]
        self.structure: list[str] = definition["structure"]
        self.reply: list = definition.get("reply",["say","ok"])

class LanguageSyntax:
    def __init__(self, jsonDict: dict[str,list[dict]]):
        self.dict: dict[str,list[StructureDef]] = {}
        for structure, structureDefinitions in jsonDict.items():
            self.dict[structure] = [StructureDef(structureDefinition) for structureDefinition in structureDefinitions]

class LanguageLexicon:
    def __init__(self, jsonDict:dict[str,Any]):
        self.dict: dict[str, list[LexiconWordObject]] = {}
        for type, words in jsonDict.items():
            if type == "basic":
                self.basic = basicWords(words)
            else:
                self.dict[type] = [LexiconWordObject(word) for word in words]

class basicWords:
    # Why do I need to make a class for every little thing just to process the jsons into objects inside objects?
    def __init__(self, jsonDict:dict[str,str]):
        self.yes = jsonDict["yes"]
        self.no = jsonDict["no"]
        self.greeting = jsonDict["greeting"]

class LexiconWordObject:
    def __init__(self, jsonDict: dict):
        try:
            self.root: str = jsonDict["root"]
            self.meaning: str = jsonDict.get("meaning", None)
            self.conjugations: list[str] = jsonDict.get("conjugations",[])
        except KeyError:
            raise ValueError(f"languageLexicon.json contains invalid word definition: {jsonDict}")

class knowledgeObject:
    def __init__(self, jsonDict: dict[str,dict[str,dict]]):
        self.dict = jsonDict

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
            return (type, textStr)
        else:
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

def answer(structuredSentence: tuple[str,list[tuple]]):
    structureName, elementsList = structuredSentence
    # find the definition of the structure, and get the reply definition from it.
    replyDefinitions = [structure.reply for structure in languageSyntax.dict["sentence"] if structure.name == structureName]
    if len(replyDefinitions) < 1:
        # This will probably never happen, but it will be good to know if it does. 
        raise RuntimeError(f"checkStructure returned an invalid structure name: {structureName}. Please contact developer.")
    if len(replyDefinitions) > 1:
        # This is a legitimate concern.
        raise RuntimeError(f"Syntax file contains duplicate structureNames: {structureName}. Please contact the maker of the syntax file.")
    replyDefinition = replyDefinitions[0]
    match replyDefinition[0]:
        case "say":
            return replyDefinition[1]
        case "checkif":
            _,*remainder = replyDefinition
            if answerQuestion(remainder):
                return languageLexicon.basic.yes
            else:
                return languageLexicon.basic.no
    # Use the reply definition and the elementsList to get a reply.

def answerQuestion(question: list) -> bool:
    #TODO: Make this actually do something
    return True

with open("languageSyntax.json") as f:
    languageSyntax = LanguageSyntax(json.load(f))
with open("languageLexicon.json") as f:
    languageLexicon = LanguageLexicon(json.load(f))
with open("knowledge.json") as f:
    knowledge = knowledgeObject(json.load(f))

def removePunctuation(text:str):
    for character in string.punctuation:
        text = text.replace(character,"")
    return text


class Bot:
    def __init__(self, UserInput: Callable[[],str], output: Callable[[str],None]):
        self.input: Callable[[],str] = UserInput
        self.output = output
    
    def run(self) -> None:
        self.output(languageLexicon.basic.greeting)
        while True:
            prompt: str = removePunctuation(self.input().lower())
            if prompt in ["STOP","stop","QUIT"]:
                break
            wordsList = prompt.split()
            sentenceDef = checkStructure(wordsList, "sentence") # I don't know what to name this variable
            self.output(answer(sentenceDef))