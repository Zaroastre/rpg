from abc import ABC
from enum import Enum

from rpg.utils import Color


class QualityTypeValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: str = name
        self.__color: Color = color
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.__color.to_tuple()

class QualityType(Enum):
    POOR: QualityTypeValue = QualityTypeValue(name="POOR", color=Color(157,157,157))
    COMMON: QualityTypeValue = QualityTypeValue(name="COMMON", color=Color(255,255,255))
    UNCOMMON: QualityTypeValue = QualityTypeValue(name="UNCOMMON", color=Color(30,255,0))
    RARE: QualityTypeValue = QualityTypeValue(name="RARE", color=Color(0,112,221))
    EPIC: QualityTypeValue = QualityTypeValue(name="EPIC", color=Color(163,53,238))
    LEGENDARY: QualityTypeValue = QualityTypeValue(name="LEGENDARY", color=Color(255,128,0))
    ARTIFACT: QualityTypeValue = QualityTypeValue(name="ARTIFACT", color=Color(230,204,128))