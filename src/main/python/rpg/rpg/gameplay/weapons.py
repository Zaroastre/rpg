from enum import Enum
from random import randint, random

from rpg.gamedesign.interval_system import Range
from rpg.gameplay.qualities import QualityType
from rpg.gameplay.stuffs import Stuff, StuffPartType


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
    STAVE: WeaponTypeValue = WeaponTypeValue("STAVE")
    BOW: WeaponTypeValue = WeaponTypeValue("BOW")
    CROSSBOW: WeaponTypeValue = WeaponTypeValue("CROSSBOW")
    GUN: WeaponTypeValue = WeaponTypeValue("GUN")
    WAND: WeaponTypeValue = WeaponTypeValue("WAND")

class Weapon(Stuff):
    def __init__(self, name:str, description: str, weapon_type: WeaponType, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, stuff_part_type, description, quality)
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        self.__weapon_type: WeaponType = weapon_type
        self.__damages: Range = damages
        
        
    
    @property
    def weapon_type(self) -> WeaponType:
        return self.__weapon_type
    
    def damage(self) -> int:
        return self.__damages.random()

class Dagger(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.DAGGER, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class OneHandAxe(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_AXE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class OneHandMace(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_MACE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class OneHandSword(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.ONE_HAND_SWORD, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class TwoHandsAxe(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_AXE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class TwoHandsMace(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_MACE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class TwoHandsSword(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.TWO_HANDS_SWORD, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)
        
class Polearm(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.POLEARM, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)
        
class Stave(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.STAVE, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)
        
class Wand(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.WAND, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)
class Bow(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.BOW, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)
        
class CrossBow(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.CROSSBOW, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class Gun(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.GUN, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)

class Stick(Weapon):
    def __init__(self, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(name, description, WeaponType.STICK, stuff_part_type, quality, required_level, damages, hit_chance, attack_speed)


class WeaponFactory:
    
    @staticmethod
    def __generate_hit_chance() -> float:
        return round(randint(0,5) + random(), 2)
    
    @staticmethod
    def __generate_damage_range(weapon_type: WeaponType, level: int) -> Range:
        minimum: int = int(level*2)
        maximum: int = minimum*2
        damage: Range = Range(minimum, maximum)
        return damage
    
    @staticmethod
    def __generate_attak_speed(weapon_type: WeaponType) -> float:
        speed: float = 1.0
        return speed
    
    @staticmethod
    def dagger(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Dagger:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Dagger(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_axe(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> OneHandAxe:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandAxe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_mace(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> OneHandMace:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandMace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_sword(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> OneHandSword:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return OneHandSword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_axe(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> TwoHandsAxe:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsAxe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_mace(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> TwoHandsMace:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsMace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_sword(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> TwoHandsSword:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return TwoHandsSword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def stick(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Stick:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Stick(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def polearm(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Polearm:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Polearm(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def wand(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Wand:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Wand(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def stave(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Stave:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Stave(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def bow(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Bow:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Bow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)

    @staticmethod
    def crossbow(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> CrossBow:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return CrossBow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def gun(name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Gun:
        if (stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        return Gun(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
    
    @staticmethod
    def create(weapon_type: WeaponType, name:str, description: str, stuff_part_type: StuffPartType, quality: QualityType, weapon_level: int, damages: Range, hit_chance: float, attack_speed: float) -> Weapon:
        if (weapon_type is None):
            raise ValueError()
        if (stuff_part_type is None or stuff_part_type not in [StuffPartType.LEFT_HAND_OBJECT, StuffPartType.RIGHT_HAND_OBJECT]):
            raise ValueError()
        match weapon_type:
            case WeaponType.DAGGER:
                weapon = WeaponFactory.dagger(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.ONE_HAND_AXE:
                weapon = WeaponFactory.one_hand_axe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.ONE_HAND_MACE:
                weapon = WeaponFactory.one_hand_mace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.ONE_HAND_SWORD:
                weapon = WeaponFactory.one_hand_sword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.TWO_HANDS_AXE:
                weapon = WeaponFactory.two_hands_axe(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.TWO_HANDS_MACE:
                weapon = WeaponFactory.two_hands_mace(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.TWO_HANDS_SWORD:
                weapon = WeaponFactory.two_hands_sword(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.STICK:
                weapon = WeaponFactory.stick(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.WAND:
                weapon = WeaponFactory.wand(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.POLEARM:
                weapon = WeaponFactory.polearm(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.STAVE:
                weapon = WeaponFactory.stave(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.BOW:
                weapon = WeaponFactory.bow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.CROSSBOW:
                weapon = WeaponFactory.crossbow(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
            case WeaponType.GUN:
                weapon = WeaponFactory.gun(name, description, stuff_part_type, quality, weapon_level, damages, hit_chance, attack_speed)
        return weapon
