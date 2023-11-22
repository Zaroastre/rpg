from abc import ABC
from enum import Enum

from rpg.geolocation import Moveable, WindRose, Position
from rpg.gamedesign.character_system import AbstractCharacter


class FormOfLife(AbstractCharacter):
    def __init__(self) -> None:
        super().__init__()

class BreedTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name


class BreedType(Enum):
    HUMAN: BreedTypeValue = BreedTypeValue("HUMAN")
    GNOME: BreedTypeValue = BreedTypeValue("GNOME")
    DRAENEI: BreedTypeValue = BreedTypeValue("DRAENEI")
    NIGHT_ELF: BreedTypeValue = BreedTypeValue("NIGHT_ELF")
    PANDAREN: BreedTypeValue = BreedTypeValue("PANDAREN")
    KNOWF: BreedTypeValue = BreedTypeValue("KNOWF")
    BLOOD_ELF: BreedTypeValue = BreedTypeValue("BLOOD_ELF")
    UNDEAD: BreedTypeValue = BreedTypeValue("UNDEAD")
    ORC: BreedTypeValue = BreedTypeValue("ORC")
    TROLL: BreedTypeValue = BreedTypeValue("TROLL")
    TAUREN: BreedTypeValue = BreedTypeValue("TAUREN")


class Breed(FormOfLife):
    def __init__(self, breed_type: BreedType) -> None:
        super().__init__()
        self.__breed_type: BreedType = breed_type
    
    @property
    def breed_type(self) -> BreedType:
        return self.__breed_type

class Human(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.HUMAN)
class Gnome(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.GNOME)
class Draenei(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.DRAENEI)
class NightElf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.NIGHT_ELF)
class Pandaren(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.PANDAREN)
class Knowrf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.KNOWF)
class BloodElf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.BLOOD_ELF)
class Undead(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.UNDEAD)
class Orc(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.ORC)
class Troll(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.TROLL)
class Tauren(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.TAUREN)


class BreedFactory:
    @staticmethod
    def create(breed_type: BreedType) -> Breed:
        breed: Breed = None
        if (breed_type is None):
            raise ValueError()
        match breed_type:
            case BreedType.HUMAN:
                breed = BreedFactory.human()
            case BreedType.GNOME:
                breed = BreedFactory.gnome()
            case BreedType.DRAENEI:
                breed = BreedFactory.draenei()
            case BreedType.NIGHT_ELF:
                breed = BreedFactory.night_elf()
            case BreedType.PANDAREN:
                breed = BreedFactory.pandaren()
            case BreedType.KNOWF:
                breed = BreedFactory.knowrf()
            case BreedType.BLOOD_ELF:
                breed = BreedFactory.blood_elf()
            case BreedType.UNDEAD:
                breed = BreedFactory.undead()
            case BreedType.ORC:
                breed = BreedFactory.orc()
            case BreedType.TROLL:
                breed = BreedFactory.troll()
            case BreedType.TAUREN:
                breed = BreedFactory.tauren()
        return breed
    
    @staticmethod
    def human() -> Human:
        return Human()
    @staticmethod
    def gnome() -> Gnome:
        return Gnome()
    @staticmethod
    def draenei() -> Draenei:
        return Draenei()
    @staticmethod
    def night_elf() -> NightElf:
        return NightElf()
    @staticmethod
    def pandaren() -> Pandaren:
        return Pandaren()
    @staticmethod
    def knowrf() -> Knowrf:
        return Knowrf()
    @staticmethod
    def blood_elf() -> BloodElf:
        return BloodElf()
    @staticmethod
    def undead() -> Undead:
        return Undead()
    @staticmethod
    def orc() -> Orc:
        return Orc()
    @staticmethod
    def troll() -> Troll:
        return Troll()
    @staticmethod
    def tauren() -> Tauren:
        return Tauren()