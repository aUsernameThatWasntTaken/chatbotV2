import json
from typing import Callable, Any
import string

debug = True

class StructureDef:
    """An object for storing a structure definition from Syntax file better, so errors can be found faster."""
    def __init__(self, definition: dict):
        self.name: str = definition["name"]
        self.structure: list[str] = definition["structure"]
        self.reply: list = definition.get("reply",["say","ok"])
        self.variant: str = definition.get("variant","None")
        self.meaning: dict = definition.get("meaning",{})

class LanguageSyntax:
    def __init__(self, jsonDict: dict[str,list[dict]]):
        self.dict: dict[str,list[StructureDef]] = {}
        self.allstructures: list[StructureDef] = [StructureDef({"name":"specificWord","structure":["any"]})]
        for structure, structureDefinitions in jsonDict.items():
            self.dict[structure] = [StructureDef(structureDefinition) for structureDefinition in structureDefinitions]
            for structureDef in structureDefinitions:
                self.allstructures.append(StructureDef(structureDef))

class LanguageLexicon:
    def __init__(self, jsonDict:dict[str,Any]):
        self.dict: dict[str, list[LexiconWordObject]] = {}
        self.allWords: list[LexiconWordObject] = []
        for type, words in jsonDict.items():
            if type == "basic":
                self.basic = basicWords(words)
            elif type == "userInputTranslations":
                self.userInputTranslations: dict[str,str] = words
            elif type == "affixes":
                self.affixes: dict[str,dict[str,str]] = words
            else:
                self.dict[type] = [LexiconWordObject(word) for word in words]
                for word in words: 
                    self.allWords.append(LexiconWordObject(word)) 

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
    def __repr__(self):
        return f"word(root={self.root}, meaning={self.meaning}, conjugations={self.conjugations})"

class knowledgeObject:
    def __init__(self, jsonDict: dict[str,dict[str,dict]]):
        self.dict = jsonDict
    def __str__(self):
        return str(self.dict)

def generateListPartitions(inputList: list[str], n: int):
    """
    function that returns a list of all the ways to split a list into n lists.\n
    I already hate this project.\n
    I had to rewrite this godforsaken garbage for n != 3\n
    I hate my life.\n
    DONOTEDIT
    TODO: Rename this and the other function to something better.
    """
    returnList: list[list[list[str]]] = []
    for numbersPossibility in generateIntegerPartitions(n,len(inputList)):
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

def generateIntegerPartitions(n:int, i:int):
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
            for otherNumsPossibility in generateIntegerPartitions(n-1,i-j):
                possibility = [j]
                for number in otherNumsPossibility:
                    possibility.append(number)
                returnList.append(possibility)
    return returnList

def checkStructure(text: list[str], type: str):
    """Checks if the text (list of words) matches any of the structures in languageSyntax or words in langyageLexicon.\n
    Returns None if No."""
    if type == "any":
        return ("any",text)
    if type not in languageSyntax.dict.keys():
        if type not in languageLexicon.dict.keys():
            if (type not in [word.root for word in languageLexicon.allWords]) and (True not in [(type in word.conjugations) for word in languageLexicon.allWords]):
                if debug: print([(type in word.conjugations) for word in languageLexicon.allWords])
                raise ValueError(f"languageSyntax file contains unsupported Structure, word class or word: \"{type}\"")
            return ("specificWord",type)
        textStr = " ".join(text).lower()
        if textStr in [word.root for word in languageLexicon.dict[type]] or True in [(textStr in word.conjugations) for word in languageLexicon.dict[type]]:
            if debug:
                print(f"\"{textStr}\" is a valid {type}.")
            return (type, textStr)
        else:
            if debug:
                print(f"\"{textStr}\" is not a valid {type}.")
            return None
    for structure in languageSyntax.dict[type]:
        #use generateListPartitions to split text into various combinations, and check them against the structure.
        textVariations = generateListPartitions(text,len(structure.structure))
        for variation in textVariations:
            returnTuplesList: list[tuple] = []
            for itemToBeChecked,element in zip(variation, structure.structure):
                #YAY! Recursion. :(
                checkStructureResult = checkStructure(itemToBeChecked,element)
                if checkStructureResult is None:
                    break
                else:
                    returnTuplesList.append(checkStructureResult)
            else:
                return (structure.name,returnTuplesList)
    return None

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
    replyDefinition = [elementsList[item] if isinstance(item,int) else item for item in replyDefinition] # replaces any number with the corresponding element.
    match replyDefinition:
        case ["say",something]:
            return something
        case ["checkif",*something]:
            if answerClosedQuestion(something, elementsList):
                return languageLexicon.basic.yes
            else:
                return languageLexicon.basic.no
        case ["find",*something]:
            return decode(something, elementsList)
        case _:
            raise RuntimeError(f"invalid reply definition: {replyDefinition}")
    # Use the reply definition and the elementsList to get a reply.


def answerClosedQuestion(question: list, elementsList) -> bool:
    """Uses decode to answer questions with True/False answers, such as whether the description
    of an object contains a specific adjective"""
    match question:
        case [x, "in", *aList]:
            if debug:
                print(question)
                print(x)
            return x[1] in decode(aList, elementsList)
        case _:
            raise RuntimeError(f"languageSyntax file contains invalid reply definition: {question}")


def decode(code: list, elementsList):
    """Currently returns the description of an object, but it can do much more if told how."""
    if debug:
        print(f"decoding {elementsList} using {code}")
    match code:
        case ["desc",Object]:
            if debug:
                print(f"Returning the description of {Object}")
            return knowledge.dict["objects"][decodePhrase(Object, elementsList)]["desc"]
        case [attribute, "of", Object]:
            if debug:
                print(f"Pattern [attribute, \"of\", Object] matched by {code}")
                print(f"searching for {attribute[1]} in {knowledge.dict["objects"][decodePhrase(Object, elementsList).removesuffix(languageLexicon.affixes["plural"]["suffix"])]["desc"]}")
            return knowledge.dict["objects"][decodePhrase(Object, elementsList).removesuffix(languageLexicon.affixes["plural"]["suffix"])]["desc"][attribute[1]]
        case _:
            raise RuntimeError(f"invalid code: {code}")

def decodePhrase(phrase: tuple[str,list], elementsList):
    if phrase[0] == "specificWord":
        return phrase[1]
    # checks if it is a structure
    structureList = [structure for structure in languageSyntax.allstructures if structure.name == phrase[0]]
    if len(structureList) == 1:
        structure = structureList[0]
        if debug:
            print(structure.variant)
        match structure.variant:
            case "normalNounPhrase":
                return dict(phrase[1])["noun"]
            case "possesiveNounPhrase":
                newElementsList = phrase[1]
                meaning = [newElementsList[item] if isinstance(item,int) else item for item in structure.meaning]
                if debug:
                    print(f"Possesive Noun Phrase to decode: {phrase}, using {meaning}")
                return decode (meaning, newElementsList)
        raise RuntimeError("No clue how this happened.")
    #checks if it is a word
    wordsList = [word for word in languageLexicon.allWords if word.root == phrase[1] or phrase[1] in word.conjugations]
    if len(wordsList) == 1:
        return wordsList[0].root
    raise RuntimeError(f"Neither structuresList ({structureList}) nor wordsList ({wordsList}) contain exactly one element.")

def restringify(sentenceElement: tuple):
    returnStr = ""
    _, elements = sentenceElement   
    if isinstance(elements, str):
        returnStr = returnStr +" "+ elements
    else:
        for e in elements:
            returnStr = returnStr+" "+restringify(e)
    return returnStr.removeprefix(" ")

with open("languageSyntax.json") as f:
    languageSyntax = LanguageSyntax(json.load(f))
with open("languageLexicon.json") as f:
    languageLexicon = LanguageLexicon(json.load(f))
with open("knowledge.json") as f:
    knowledge = knowledgeObject(json.load(f))

def removePunctuation(text:str):
    for character in string.punctuation:
        if character == "'":
            continue
        text = text.replace(character,"")
    return text


class Bot:
    def __init__(self, UserInput: Callable[[],str], output: Callable[[str],None]):
        self.input: Callable[[],str] = UserInput
        self.output = output
    
    def run(self) -> None:
        self.output(languageLexicon.basic.greeting)
        while True:
            prompt: str = " " + removePunctuation(self.input().lower())
            for word, translation in languageLexicon.userInputTranslations.items():
                prompt = prompt.replace(word,translation)
            prompt = prompt.removeprefix(" ")
            if prompt in ["stop","quit"]:
                break
            wordsList = prompt.split()
            sentenceDef = checkStructure(wordsList, "sentence") # I don't know what to name this variable
            if sentenceDef is None:
                self.output("I don't understand how you structured that sentence.")
                if debug:
                    print(f"(The sentence was \"{prompt}\")")
                continue
            if debug:
                print(sentenceDef)
            self.output(answer(sentenceDef))
        if debug:
            print("KNOWLEDGE:")
            print(str(knowledge))