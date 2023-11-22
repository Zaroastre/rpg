from enum import Enum
from rpg.utils import Color

class FactionValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: name
        self.__color: Color = color
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.__color.to_tuple()

class Faction(Enum):
    HORDE: FactionValue = FactionValue("HORDE")
    ALLIANCE: FactionValue = FactionValue("ALLIANCE")
    NEUTRAL: FactionValue = FactionValue("NEUTRAL")