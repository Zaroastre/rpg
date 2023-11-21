from enum import Enum

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
    POLEARM: WeaponTypeValue = WeaponTypeValue("POLEARM")
    STAVE: WeaponTypeValue = WeaponTypeValue("STAVE")
    BOW: WeaponTypeValue = WeaponTypeValue("BOW")
    CROSSBOW: WeaponTypeValue = WeaponTypeValue("CROSSBOW")
    GUN: WeaponTypeValue = WeaponTypeValue("GUN")
    WAND: WeaponTypeValue = WeaponTypeValue("WAND")
    

class Weapon:
    def __init__(self) -> None:
        pass
