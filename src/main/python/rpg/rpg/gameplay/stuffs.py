from enum import Enum
from rpg.objects import Object
from rpg.gameplay.qualities import QualityType
from rpg.gameplay.attributes import Attribute
from rpg.gameplay.gems import GemsBox


class StuffPartTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name

class StuffPartType(Enum):
    HELMET: StuffPartTypeValue = StuffPartTypeValue("HELMET")
    NECK: StuffPartTypeValue = StuffPartTypeValue("NECK")
    SHOULDERS: StuffPartTypeValue = StuffPartTypeValue("SHOULDERS")
    WRISTS: StuffPartTypeValue = StuffPartTypeValue("WRISTS")
    HANDS: StuffPartTypeValue = StuffPartTypeValue("HANDS")
    CHEST: StuffPartTypeValue = StuffPartTypeValue("CHEST")
    BACK: StuffPartTypeValue = StuffPartTypeValue("BACK")
    LEGS: StuffPartTypeValue = StuffPartTypeValue("LEGS")
    FEET: StuffPartTypeValue = StuffPartTypeValue("FEET")
    LEFT_HAND_OBJECT: StuffPartTypeValue = StuffPartTypeValue("LEFT_HAND_OBJECT")
    RIGHT_HAND_OBJECT: StuffPartTypeValue = StuffPartTypeValue("RIGHT_HAND_OBJECT")

class Stuff(Object):
    def __init__(self, name: str, stuff_part_type: StuffPartType, description: str=None, quality: QualityType=QualityType.POOR, attributes: dict[Attribute, int] = {}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, quality)
        self.__stuff_part_type: StuffPartType = stuff_part_type
        self.__attributes: dict[Attribute, int] = attributes
        self.__gems_box: GemsBox = GemsBox(gems_capacity)
    

    @property
    def gem_box(self) -> GemsBox:
        return self.__gems_box

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

class Helmet(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.HELMET, description, quality, attributes, gems_capacity)

class Shoulders(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.SHOULDERS, description, quality, attributes, gems_capacity)


class Wrists(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.WRISTS, description, quality, attributes, gems_capacity)

class Hands(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.HANDS, description, quality, attributes, gems_capacity)

class Chest(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.CHEST, description, quality, attributes, gems_capacity)
    
class Back(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.BACK, description, quality, attributes, gems_capacity)
class Legs(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.LEGS, description, quality, attributes, gems_capacity)
class Feet(Stuff):
    def __init__(self, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int], gems_capacity: int) -> None:
        super().__init__(name, StuffPartType.FEET, description, quality, attributes, gems_capacity)

class StuffFactory:
    @staticmethod
    def helmet(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Helmet:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def shoulders(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Shoulders:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def wrists(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Wrists:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def hands(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Hands:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def chest(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Chest:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def back(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Back:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def legs(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Legs:
        return Helmet(name, description, quality, attributes, gems_capacity)
    @staticmethod
    def feet(name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0) -> Feet:
        return Helmet(name, description, quality, attributes, gems_capacity)
    
    @staticmethod
    def create(stuff_type: StuffPartType, name:str, description: str, quality: QualityType, attributes: dict[Attribute, int]={}, gems_capacity: int=0):
        if (stuff_type is None):
            raise ValueError()
        if (stuff_type is None or stuff_type not in [StuffPartType.HELMET, StuffPartType.HANDS, StuffPartType.CHEST, StuffPartType.BACK, StuffPartType.FEET, StuffPartType.NECK, StuffPartType.SHOULDERS]):
            raise ValueError()
        stuff: Stuff
        match stuff_type:
            case stuff_type.HELMET:
                stuff = StuffFactory.helmet(name, description, quality, attributes, gems_capacity)
            case stuff_type.WRISTS:
                stuff = StuffFactory.wrists(name, description, quality, attributes, gems_capacity)
            case stuff_type.SHOULDERS:
                stuff = StuffFactory.shoulders(name, description, quality, attributes, gems_capacity)
            case stuff_type.HANDS:
                stuff = StuffFactory.hands(name, description, quality, attributes, gems_capacity)
            case stuff_type.CHEST:
                stuff = StuffFactory.chest(name, description, quality, attributes, gems_capacity)
            case stuff_type.BACK:
                stuff = StuffFactory.back(name, description, quality, attributes, gems_capacity)
            case stuff_type.LEGS:
                stuff = StuffFactory.legs(name, description, quality, attributes, gems_capacity)
            case stuff_type.FEET:
                stuff = StuffFactory.feet(name, description, quality, attributes, gems_capacity)
        return stuff