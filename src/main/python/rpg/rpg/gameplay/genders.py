from enum import Enum


class GenderValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
    
    @property
    def name(self) -> str:
        return self.__name

class Gender(Enum):
    MAN: GenderValue = GenderValue(name="MAN")
    WOMAN: GenderValue = GenderValue(name="WOMAN")
