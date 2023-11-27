from enum import Enum
from rpg.objects import Object
from rpg.gameplay.qualities import QualityType


class StuffPartTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name

class StuffPartType(Enum):
    HELMET: StuffPartTypeValue = StuffPartTypeValue("HELMET")
    NECK: StuffPartTypeValue = StuffPartTypeValue("HELMET")
    SHOULDERS: StuffPartTypeValue = StuffPartTypeValue("HELMET")
    WRISTS: StuffPartTypeValue = StuffPartTypeValue("WRIST")
    HANDS: StuffPartTypeValue = StuffPartTypeValue("HANDS")
    CHEST: StuffPartTypeValue = StuffPartTypeValue("CHEST")
    BACK: StuffPartTypeValue = StuffPartTypeValue("BACK")
    LEGS: StuffPartTypeValue = StuffPartTypeValue("LEGS")
    FEET: StuffPartTypeValue = StuffPartTypeValue("FEET")
    LEFT_HAND_OBJECT: StuffPartTypeValue = StuffPartTypeValue("LEFT_HAND_OBJECT")
    RIGHT_HAND_OBJECT: StuffPartTypeValue = StuffPartTypeValue("RIGHT_HAND_OBJECT")

class Stuff(Object):
    def __init__(self, name: str, stuff_part_type: StuffPartType, description: str=None, quality: QualityType=QualityType.POOR) -> None:
        super().__init__(name, description, quality)
        self.__stuff_part_type: StuffPartType = stuff_part_type
    @property
    def stuff_part_type(self) -> StuffPartType:
        return self.__stuff_part_type