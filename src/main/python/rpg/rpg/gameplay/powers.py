from abc import ABC
from enum import Enum

from rpg.utils import Color


class PowerTypeValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: str = name
        self.__color: Color = color
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.__color.to_tuple()

class PowerType(Enum):
    MANA: PowerTypeValue = PowerTypeValue(name="MANA", color=Color(0,0,255))
    RAGE: PowerTypeValue = PowerTypeValue(name="RAGE", color=Color(255,0,0))
    FOCUS: PowerTypeValue = PowerTypeValue(name="FOCUS", color=Color(255,128,64))
    ENERGY: PowerTypeValue = PowerTypeValue(name="ENERGY", color=Color(255,255,0))
    COMBO_POINTS: PowerTypeValue = PowerTypeValue(name="COMBO_POINTS", color=Color(255,245,105))
    RUNES: PowerTypeValue = PowerTypeValue(name="RUNES", color=Color(128,128,128))
    RUNIC_POWER: PowerTypeValue = PowerTypeValue(name="RUNIC_POWER", color=Color(0,209,255))
    SOUL_SHARDS: PowerTypeValue = PowerTypeValue(name="SOUL_SHARDS", color=Color(128,82,105))
    LUNAR_POWER: PowerTypeValue = PowerTypeValue(name="LUNAR_POWER", color=Color(77,133,230))
    HOLY_POWER: PowerTypeValue = PowerTypeValue(name="HOLY_POWER", color=Color(242,230,153))
    MAELSTROM: PowerTypeValue = PowerTypeValue(name="MAELSTROM", color=Color(0,128,255))
    INSANITY: PowerTypeValue = PowerTypeValue(name="INSANITY", color=Color(102,0,204))
    CHI: PowerTypeValue = PowerTypeValue(name="CHI", color=Color(181,255,235))
    ARCANE_CHARGE: PowerTypeValue = PowerTypeValue(name="ARCANE_CHARGE", color=Color(26,26,250))
    FURY: PowerTypeValue = PowerTypeValue(name="FURY", color=Color(201,66,253))
    PAIN: PowerTypeValue = PowerTypeValue(name="PAIN", color=Color(255,156,0))

class Power(ABC):
    def __init__(self, resource_type: PowerType, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else maximum
        self.__boost: list[int] = []
        self.__type: PowerType = resource_type

    @property
    def maximum(self) -> int:
        return self.__maximum
    @property
    def current(self) -> int:
        return self.__current
    @property
    def boosts(self) -> list[int]:
        return self.__boost
    @property
    def resource_type(self) -> PowerType:
        return self.__type

class Mana(Power):
    def __init__(self) -> None:
        super().__init__(PowerType.MANA, 100)

class Rage(Power):
    def __init__(self) -> None:
        super().__init__(PowerType.RAGE, 100, 0)
        
class Chi(Power):
    def __init__(self) -> None:
        super().__init__(PowerType.CHI, 100)
        
class Energy(Power):
    def __init__(self) -> None:
        super().__init__(PowerType.ENERGY, 100)
        
class Rune(Power):
    def __init__(self) -> None:
        super().__init__(PowerType.RUNES, 10)
