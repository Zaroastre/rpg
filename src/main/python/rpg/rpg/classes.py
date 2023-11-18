from abc import ABC
from enum import Enum

from rpg.resources import Resource, Mana, Energy, Qi, Rage, Rune
from rpg.skills import SkillsTree

class ClassTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name


class ClassType(Enum):
    DEMONIST: ClassTypeValue = ClassTypeValue("DEMONIST")
    MAGE: ClassTypeValue = ClassTypeValue("MAGE")
    PRIEST: ClassTypeValue = ClassTypeValue("PRIEST")
    MONK: ClassTypeValue = ClassTypeValue("MONK")
    HUNTER: ClassTypeValue = ClassTypeValue("HUNTER")
    THIEFT: ClassTypeValue = ClassTypeValue("THIEFT")
    PALADIN: ClassTypeValue = ClassTypeValue("PALADIN")
    WARRIOR: ClassTypeValue = ClassTypeValue("WARRIOR")
    SHAMAN: ClassTypeValue = ClassTypeValue("SHAMAN")
    DRUID: ClassTypeValue = ClassTypeValue("DRUID")
    DEMON_HUNTER: ClassTypeValue = ClassTypeValue("DEMON_HUNTER")
    DEATH_KNIGHT: ClassTypeValue = ClassTypeValue("DEATH_KNIGHT")

class Class(ABC):
    def __init__(self, class_type: ClassType, resource: Resource, skills_trees: list[SkillsTree]) -> None:
        self.__class_type: ClassType = class_type
        self.__resource: Resource = resource
        self.__skills_trees: list[SkillsTree] = skills_trees
    
    @property
    def class_type(self) -> ClassType:
        return self.__class_type
    
    @property
    def resource(self) -> Resource:
        return self.__resource

    @property
    def skills_trees(self) -> list[SkillsTree]:
        return self.__skills_trees
    
class Paladin(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.PALADIN, Mana(), [SkillsTree("Holy",[]), SkillsTree("Protection",[]), SkillsTree("Retribution",[])])

class Demonist(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEMONIST, Mana(), [SkillsTree("Afflication",[]), SkillsTree("Demonology",[]), SkillsTree("Destruction",[])])
        
class Mage(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.MAGE, Mana(), [SkillsTree("Arcane",[]), SkillsTree("Fire",[]), SkillsTree("Frost",[])])
        
class Priest(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.PRIEST, Mana(), [SkillsTree("Discipline",[]), SkillsTree("Holy",[]), SkillsTree("Shadow",[])])
        
class Hunter(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.HUNTER, Mana(), [SkillsTree("Beast Mastery",[]), SkillsTree("Markmanship",[]), SkillsTree("Survival",[])])
        
class Shaman(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.SHAMAN, Mana(), [SkillsTree("Elemental",[]), SkillsTree("Enhancement",[]), SkillsTree("Restoration",[])])
        
class Druid(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DRUID, Mana(), [SkillsTree("Balance",[]), SkillsTree("Feral",[]), SkillsTree("Guardian",[]), SkillsTree("Restoration",[])])
        
class DemonHunter(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEMON_HUNTER, Rune(), [SkillsTree("Havoc",[]), SkillsTree("Vengeance",[])])
      
class Rogue(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.THIEFT, Energy(), [SkillsTree("Assasination",[]), SkillsTree("Outlaw",[]), SkillsTree("Subtlety",[])])
       
class Warrior(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.WARRIOR, Rage(), [SkillsTree("Protect",[]), SkillsTree("Light",[])])
          
class Monk(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.MONK, Qi(), [SkillsTree("Arms",[]), SkillsTree("Fury",[]), SkillsTree("Protection",[])])
         
class DeathKnight(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEATH_KNIGHT, Rune(), [SkillsTree("Blood",[]), SkillsTree("Frost",[]), SkillsTree("Unholy",[])])
        
class ClassFactory:
    @staticmethod
    def create(class_type: ClassType) -> Class:
        character_class: Class = None
        if (class_type is None):
            raise ValueError()
        match class_type:
            case ClassType.PALADIN:
                character_class = Paladin()
            case ClassType.WARRIOR:
                character_class = Warrior()
            case ClassType.DEATH_KNIGHT:
                character_class = DeathKnight()
            case ClassType.DEMON_HUNTER:
                character_class = DemonHunter()
            case ClassType.HUNTER:
                character_class = Hunter()
            case ClassType.MONK:
                character_class = Monk()
            case ClassType.SHAMAN:
                character_class = Shaman()
            case ClassType.DRUID:
                character_class = Druid()
            case ClassType.MAGE:
                character_class = Mage()
            case ClassType.PRIEST:
                character_class = Priest()
            case ClassType.DEMONIST:
                character_class = Demonist()
            case ClassType.THIEFT:
                character_class = Rogue()
                
        return character_class
    
    @staticmethod
    def paladin() -> Paladin:
        return Paladin()
    
    @staticmethod
    def demonist() -> Demonist:
        return Demonist()
    @staticmethod
    def mage() -> Mage:
        return Mage()
    @staticmethod
    def priest() -> Priest:
        return Priest()
    @staticmethod
    def hunter() -> Hunter:
        return Hunter()
    @staticmethod
    def shaman() -> Shaman:
        return Shaman()
    @staticmethod
    def monk() -> Monk:
        return Monk()
    @staticmethod
    def death_knight() -> DeathKnight:
        return DeathKnight()
    @staticmethod
    def warrior() -> Warrior:
        return Warrior()
    
    @staticmethod
    def rogue() -> Rogue:
        return Rogue()
    @staticmethod
    def demon_hunter() -> DemonHunter:
        return DemonHunter()