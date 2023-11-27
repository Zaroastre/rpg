from enum import Enum
from rpg.objects import Object
from rpg.gameplay.qualities import QualityType
from rpg.gameplay.attributes import Attribute


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
    def __init__(self, name: str, stuff_part_type: StuffPartType, description: str=None, quality: QualityType=QualityType.POOR, attributes: dict[Attribute, int] = {}) -> None:
        super().__init__(name, description, quality)
        self.__stuff_part_type: StuffPartType = stuff_part_type
        self.__attributes: dict[Attribute, int] = attributes
        
    @property
    def attributes(self) -> list[Attribute]:
        return list(self.__attributes.keys())

    def get_attribute(self, attribute: Attribute) -> int:
        value: int = 0
        if (attribute in len(self.__attributes.keys())):
            value = self.__attributes.get(attribute)
        return value
    @property
    def stuff_part_type(self) -> StuffPartType:
        return self.__stuff_part_type