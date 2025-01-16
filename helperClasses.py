from typing import Protocol, Any, Callable


class checkStructureReturnType(Protocol):
    """The protocol for anything returned by checkStructure"""
    structureName: str
    contents: Any
    def answer(self, languageSyntax, languageLexicon, decode: Callable[[list,list],Any], answerClosedQuestion) -> Any: ...
    def __getitem__(self, key: int): ...


class Structure:
    """The class for when checkStructure returns a structure"""
    def __init__(self, structureName: str, contents: list[checkStructureReturnType]):
        self.structureName = structureName
        self.contents = contents

    def __getitem__(self, key: int): 
        if key == 0:
            return self.structureName
        if key == 1:
            return self.contents
        else:
            raise KeyError(key)

    def answer(self, languageSyntax, languageLexicon, decode: Callable[[list,list[checkStructureReturnType]],Any], answerClosedQuestion: Callable[[list,list[checkStructureReturnType]],bool]) -> str:
        # find the definition of the structure, and get the reply definition from it.
        replyDefinitions: list[list[str|int]] = [structure.reply for structure in languageSyntax.dict["sentence"] if structure.name == self.structureName]
        if len(replyDefinitions) < 1:
            # This will probably never happen, but it will be good to know if it does. 
            raise RuntimeError(f"checkStructure returned an invalid structure name: {self.structureName}. Please contact developer.")
        if len(replyDefinitions) > 1:
            # This is a legitimate concern.
            raise RuntimeError(f"Syntax file contains duplicate structure names: {self.structureName}. Please contact the maker of the syntax file.")
        replyDefinition: list[checkStructureReturnType|str|int] = list(replyDefinitions[0])
        replyDefinition = [self.contents[item] if isinstance(item,int) else item for item in replyDefinition] # replaces any number with the corresponding element.
        match replyDefinition:
            case ["say",something]:
                return str(something)
            case ["checkif",*something]:
                if answerClosedQuestion(something, self.contents):
                    return languageLexicon.basic.yes
                else:
                    return languageLexicon.basic.no
            case ["find",*something]:
                return decode(something, self.contents)
            case _:
                raise RuntimeError(f"invalid reply definition: {replyDefinition}")
        # Use the reply definition and the self.contents to get a reply.

class OneWord:
    """The class for when checkStructure returns one word"""
    def __init__(self, structureName: str, contents: str):
        self.structureName = structureName
        self.contents = contents
        
    def __getitem__(self, key: int): 
        print(f"Key provided: {key}")
        if key == 0:
            return self.structureName
        if key == 1:
            return self.contents
        else:
            raise KeyError(f"Word ({self.structureName} {self.contents}) subscribed with invalid key: {key}")

    def answer(self, lS, lL, d, aCQ) -> str:
        raise RuntimeError("Tried to answer non-sentence")
    
class AnyStructure:
    """The class for when checkStructure returns a structure labelled "any\""""
    def __init__(self, contents: list[str]):
        self.structureName = "any"
        self.contents = contents

    def __getitem__(self, key: int):
        if key == 0:
            return self.structureName
        if key == 1:
            return self.contents
        else:
            raise KeyError(key)

    def answer(self, lS,lL,d,aCQ):
        raise RuntimeError("Tried to answer non-sentence")



class ReplyDefinition:
    def __init__(self, items: list[str|int]):
        self.command, *self.argument = items