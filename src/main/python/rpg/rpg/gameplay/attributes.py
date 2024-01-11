from enum import Enum
from rpg.colors import Color

class AttributeType(Enum):
    PRIMARY=1
    SECONDARY=2
    TERTIARY=3
    DERIVED=4
    OTHER=5
    
class AttributeValue:
    def __init__(self, name: str, attribute_type: AttributeType) -> None:
        self.__name: name
        self.__attribute_type: AttributeType = attribute_type
    @property
    def attribute_type(self) -> Color:
        return self.__attribute_type
    @property
    def name(self) -> str:
        return self.__name

class Attribute(Enum):
    STAMANIA: AttributeValue = AttributeValue("STAMANIA", AttributeType.PRIMARY)
    STRENGTH: AttributeValue = AttributeValue("STRENGTH", AttributeType.PRIMARY)
    AGILITY: AttributeValue = AttributeValue("AGILITY", AttributeType.PRIMARY)
    INTELLECT: AttributeValue = AttributeValue("INTELLECT", AttributeType.PRIMARY)
    SPIRIT: AttributeValue = AttributeValue("SPIRIT", AttributeType.PRIMARY)
    
    CRITICAL_STRIKE: AttributeValue = AttributeValue("CRITICAL_STRIKE", AttributeType.SECONDARY)
    HASTE: AttributeValue = AttributeValue("HASTE", AttributeType.SECONDARY)
    MASTERY: AttributeValue = AttributeValue("MASTERY", AttributeType.SECONDARY)
    VERSATILITY: AttributeValue = AttributeValue("VERSATILITY", AttributeType.SECONDARY)
    
    AVOIDANCE: AttributeValue = AttributeValue("AVOIDANCE", AttributeType.TERTIARY)
    INDESTRUCTIBLE: AttributeValue = AttributeValue("INDESTRUCTIBLE", AttributeType.TERTIARY)
    LEECH: AttributeValue = AttributeValue("LEECH", AttributeType.TERTIARY)
    SPEED: AttributeValue = AttributeValue("SPEED", AttributeType.TERTIARY)
    
    PHYSICAL: AttributeValue = AttributeValue("PHYSICAL", AttributeType.DERIVED)
    SPELL: AttributeValue = AttributeValue("SPELL", AttributeType.DERIVED)
    DEFENSE: AttributeValue = AttributeValue("DEFENSE", AttributeType.DERIVED)
    
    BONUS_ARMOR: AttributeValue = AttributeValue("BONUS_ARMOR", AttributeType.OTHER)
    RESISTENCE: AttributeValue = AttributeValue("RESISTENCE", AttributeType.OTHER)
    SPELL_PENETRATION: AttributeValue = AttributeValue("SPELL_PENETRATION", AttributeType.OTHER)
