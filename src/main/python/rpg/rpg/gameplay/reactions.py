from abc import ABC
from enum import Enum

from rpg.colors import Color


class ReactionTypeValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: str = name
        self.__color: Color = color
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.__color.to_tuple()

class ReactionType(Enum):
    HOSTILE: ReactionTypeValue = ReactionTypeValue(name="HOSTILE", color=Color(255,0,0))
    NEUTRAL: ReactionTypeValue = ReactionTypeValue(name="NEUTRAL", color=Color(255,255,0))
    FRIENDLY: ReactionTypeValue = ReactionTypeValue(name="FRIENDLY", color=Color(0,255,0))