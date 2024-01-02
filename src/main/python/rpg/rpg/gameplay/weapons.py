from enum import Enum
from random import randint, random

from rpg.gamedesign.interval_system import Range
from rpg.gameplay.qualities import QualityType
from rpg.gameplay.stuffs import Stuff, StuffPartType
from rpg.gameplay.attributes import Attribute


class WeaponTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name

class WeaponType(Enum):
    DAGGER: WeaponTypeValue = WeaponTypeValue("DAGGER")
    ONE_HAND_AXE: WeaponTypeValue = WeaponTypeValue("ONE_HAND_AXE")
    TWO_HANDS_AXE: WeaponTypeValue = WeaponTypeValue("TWO_HANDS_AXE")
    ONE_HAND_MACE: WeaponTypeValue = WeaponTypeValue("ONE_HAND_MACE")
    TWO_HANDS_MACE: WeaponTypeValue = WeaponTypeValue("TWO_HANDS_MACE")
    ONE_HAND_SWORD: WeaponTypeValue = WeaponTypeValue("ONE_HAND_SWORD")
    TWO_HANDS_SWORD: WeaponTypeValue = WeaponTypeValue("TWO_HANDS_SWORD")
    STICK: WeaponTypeValue = WeaponTypeValue("STICK")
    POLEARM: WeaponTypeValue = WeaponTypeValue("POLEARM")
    FIST_WEAPON: WeaponTypeValue = WeaponTypeValue("FIST_WEAPON") # 2.6
    WAR_GLAIVE: WeaponTypeValue = WeaponTypeValue("WAR_GLAIVE") # 2.6
    STAVE: WeaponTypeValue = WeaponTypeValue("STAVE")
    BOW: WeaponTypeValue = WeaponTypeValue("BOW")
    CROSSBOW: WeaponTypeValue = WeaponTypeValue("CROSSBOW")
    GUN: WeaponTypeValue = WeaponTypeValue("GUN")
    WAND: WeaponTypeValue = WeaponTypeValue("WAND")

class Weapon(Stuff):
    def __init__(self, name:str, description: str, weapon_type: WeaponType, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, stuff_part_type, description, quality, attributes, gems_capacity)
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        self.__weapon_type: WeaponType = weapon_type
        self.__damages: Range = damages
        self.__attack_speed: float = attack_speed
        self.__hit_chance: float = hit_chance
        self.__required_level: int = required_level
    
    @property
    def attack_speed(self) -> float:
        return self.__attack_speed
    @property
    def hit_chance(self) -> float:
        return self.__hit_chance
    @property
    def required_level(self) -> int:
        return self.__required_level
    @property
    def weapon_type(self) -> WeaponType:
        return self.__weapon_type
    
    def damage(self) -> int:
        return self.__damages.random()

class Dagger(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.DAGGER, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class OneHandAxe(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_AXE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class OneHandMace(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_MACE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class OneHandSword(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_SWORD, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class TwoHandsAxe(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_AXE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class TwoHandsMace(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_MACE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class TwoHandsSword(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_SWORD, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)
        
class Polearm(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.POLEARM, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)
        
class Stave(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.STAVE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)
        
class Wand(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.WAND, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)
class Bow(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.BOW, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)
        
class CrossBow(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.CROSSBOW, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class Gun(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.GUN, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)

class Stick(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float, attributes: dict[Attribute, int]={}, gems_capacity: int = 0) -> None:
        super().__init__(name, description, WeaponType.STICK, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed, attributes, gems_capacity)


class WeaponFactory:
    
    @staticmethod
    def dagger(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Dagger:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Dagger(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 1.8)
    @staticmethod
    def one_hand_axe(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> OneHandAxe:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandAxe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 2.6)
    @staticmethod
    def one_hand_mace(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> OneHandMace:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandMace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 2.6)
    @staticmethod
    def one_hand_sword(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> OneHandSword:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandSword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 2.6)
    @staticmethod
    def two_hands_axe(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> TwoHandsAxe:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsAxe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.6)
    @staticmethod
    def two_hands_mace(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> TwoHandsMace:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsMace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.6)
    @staticmethod
    def two_hands_sword(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> TwoHandsSword:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsSword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.6)
    @staticmethod
    def polearm(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Polearm:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Polearm(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.6)
    @staticmethod
    def wand(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Wand:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Wand(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 2.0)
    @staticmethod
    def stave(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Stave:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Stave(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.6)
    @staticmethod
    def bow(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Bow:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Bow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.0)

    @staticmethod
    def crossbow(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> CrossBow:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return CrossBow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.0)
    @staticmethod
    def gun(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Gun:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Gun(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, 3.0)
    
    @staticmethod
    def create(weapon_type: WeaponType, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float) -> Weapon:
        if (weapon_type is None):
            raise ValueError()
        if (stuff_part_type is None or stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        weapon: Weapon
        match weapon_type:
            case WeaponType.DAGGER:
                weapon = WeaponFactory.dagger(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.ONE_HAND_AXE:
                weapon = WeaponFactory.one_hand_axe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.ONE_HAND_MACE:
                weapon = WeaponFactory.one_hand_mace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.ONE_HAND_SWORD:
                weapon = WeaponFactory.one_hand_sword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.TWO_HANDS_AXE:
                weapon = WeaponFactory.two_hands_axe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.TWO_HANDS_MACE:
                weapon = WeaponFactory.two_hands_mace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.TWO_HANDS_SWORD:
                weapon = WeaponFactory.two_hands_sword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.WAND:
                weapon = WeaponFactory.wand(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.POLEARM:
                weapon = WeaponFactory.polearm(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.STAVE:
                weapon = WeaponFactory.stave(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.BOW:
                weapon = WeaponFactory.bow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.CROSSBOW:
                weapon = WeaponFactory.crossbow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
            case WeaponType.GUN:
                weapon = WeaponFactory.gun(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance)
        return weapon
