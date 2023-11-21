from enum import Enum

class FactionValue:
    def __init__(self, name: str) -> None:
        self.__name: name
    @property
    def name(self) -> str:
        return self.__name

class Faction(Enum):
    HORDE: FactionValue = FactionValue("HORDE")
    ALLIANCE: FactionValue = FactionValue("ALLIANCE")
    NEUTRAL: FactionValue = FactionValue("NEUTRAL")