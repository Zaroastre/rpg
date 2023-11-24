from enum import Enum
from rpg.objects import Object
from rpg.gamedesign.character_system import AbstractCharacter
from rpg.gamedesign.interval_system import Range
from random import random, randint


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
    

class Weapon(Object):
    def __init__(self, weapon_type: WeaponType, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(None)
        self.__weapon_type: WeaponType = weapon_type
        self.__damages: Range = damages
        
    
    @property
    def weapon_type(self) -> WeaponType:
        return self.__weapon_type
    
    def damage(self) -> int:
        return self.__damages.random()

class Dagger(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.DAGGER, required_level, damages, hit_chance, attack_speed)

class OneHandAxe(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.ONE_HAND_AXE, required_level, damages, hit_chance, attack_speed)

class OneHandMace(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.ONE_HAND_MACE, required_level, damages, hit_chance, attack_speed)

class OneHandSword(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.ONE_HAND_SWORD, required_level, damages, hit_chance, attack_speed)

class TwoHandsAxe(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.TWO_HANDS_AXE, required_level, damages, hit_chance, attack_speed)

class TwoHandsMace(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.TWO_HANDS_MACE, required_level, damages, hit_chance, attack_speed)

class TwoHandsSword(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.TWO_HANDS_SWORD, required_level, damages, hit_chance, attack_speed)
        
class Polearm(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.POLEARM, required_level, damages, hit_chance, attack_speed)
        
class Stave(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.STAVE, required_level, damages, hit_chance, attack_speed)
        
class Wand(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.WAND, required_level, damages, hit_chance, attack_speed)
class Bow(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.BOW, required_level, damages, hit_chance, attack_speed)
        
class CrossBow(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.CROSSBOW, required_level, damages, hit_chance, attack_speed)

class Gun(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.GUN, required_level, damages, hit_chance, attack_speed)

class Stick(Weapon):
    def __init__(self, required_level: int, damages: Range, hit_chance: float, attack_speed: float) -> None:
        super().__init__(WeaponType.STICK, required_level, damages, hit_chance, attack_speed)


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
    def dagger(weapon_level: int=1) -> Dagger:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.DAGGER, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.DAGGER)
        return Dagger(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_axe(weapon_level: int=1) -> OneHandAxe:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.ONE_HAND_AXE, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.ONE_HAND_AXE)
        return OneHandAxe(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_mace(weapon_level: int=1) -> OneHandMace:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.ONE_HAND_MACE, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.ONE_HAND_MACE)
        return OneHandMace(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def one_hand_sword(weapon_level: int=1) -> OneHandSword:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.ONE_HAND_SWORD, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.ONE_HAND_SWORD)
        return OneHandSword(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_axe(weapon_level: int=1) -> TwoHandsAxe:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.TWO_HANDS_AXE, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.TWO_HANDS_AXE)
        return TwoHandsAxe(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_mace(weapon_level: int=1) -> TwoHandsMace:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.TWO_HANDS_MACE, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.TWO_HANDS_MACE)
        return TwoHandsMace(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def two_hands_sword(weapon_level: int=1) -> TwoHandsSword:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.TWO_HANDS_SWORD, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.TWO_HANDS_SWORD)
        return TwoHandsSword(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def stick(weapon_level: int=1) -> Stick:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.STICK, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.STICK)
        return Stick(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def polearm(weapon_level: int=1) -> Polearm:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.POLEARM, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.POLEARM)
        return Polearm(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def wand(weapon_level: int=1) -> Wand:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.WAND, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.WAND)
        return Wand(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def stave(weapon_level: int=1) -> Stave:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.STAVE, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.STAVE)
        return Stave(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def bow(weapon_level: int=1) -> Bow:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.BOW, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.BOW)
        return Bow(weapon_level, damages, hit_chance, attack_speed)

    @staticmethod
    def crossbow(weapon_level: int=1) -> CrossBow:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.CROSSBOW, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.CROSSBOW)
        return CrossBow(weapon_level, damages, hit_chance, attack_speed)
    @staticmethod
    def gun(weapon_level: int=1) -> Gun:
        damages: Range = WeaponFactory.__generate_damage_range(WeaponType.GUN, weapon_level)
        hit_chance: float = WeaponFactory.__generate_hit_chance()
        attack_speed: float = WeaponFactory.__generate_attak_speed(WeaponType.GUN)
        return Gun(weapon_level, damages, hit_chance, attack_speed)
    
    @staticmethod
    def create(weapon_type: WeaponType, weapon_level: int=1) -> Weapon:
        weapon: Weapon = None
        if (weapon_type is None):
            raise ValueError()
        match weapon_type:
            case WeaponType.DAGGER:
                weapon = WeaponFactory.dagger(weapon_level)
            case WeaponType.ONE_HAND_AXE:
                weapon = WeaponFactory.one_hand_axe(weapon_level)
            case WeaponType.ONE_HAND_MACE:
                weapon = WeaponFactory.one_hand_mace(weapon_level)
            case WeaponType.ONE_HAND_SWORD:
                weapon = WeaponFactory.one_hand_sword(weapon_level)
            case WeaponType.TWO_HANDS_AXE:
                weapon = WeaponFactory.two_hands_axe(weapon_level)
            case WeaponType.TWO_HANDS_MACE:
                weapon = WeaponFactory.two_hands_mace(weapon_level)
            case WeaponType.TWO_HANDS_SWORD:
                weapon = WeaponFactory.two_hands_sword(weapon_level)
            case WeaponType.STICK:
                weapon = WeaponFactory.stick(weapon_level)
            case WeaponType.WAND:
                weapon = WeaponFactory.wand(weapon_level)
            case WeaponType.POLEARM:
                weapon = WeaponFactory.polearm(weapon_level)
            case WeaponType.STAVE:
                weapon = WeaponFactory.stave(weapon_level)
            case WeaponType.BOW:
                weapon = WeaponFactory.bow(weapon_level)
            case WeaponType.CROSSBOW:
                weapon = WeaponFactory.crossbow(weapon_level)
            case WeaponType.GUN:
                weapon = WeaponFactory.gun(weapon_level)
        return weapon