from abc import ABC
from enum import Enum


class Life:
    def __init__(self, max: int, left: int = None) -> None:
        self.__maximum: int = max
        self.__current: int = left if left is not None else max
        self.__boost: list[int] = []
        
    @property
    def max(self) -> int:
        return self.__maximum

    @property
    def actual(self) -> int:
        return self.__current
    
    def loose(self, points: int):
        self.__current -= points
        if (self.__current <= 0):
            self.die()

    def die(self):
        self.__current = 0

    def is_dead(self) -> bool:
        return self.__current <= 0
    
    def health(self, points: int):
        self.__current += points
    
    def is_alive(self) -> bool:
        return not self.is_dead()

class FormOfLife(ABC):
    def __init__(self) -> None:
        self.__life: Life = Life(100, 100)
    
    @property
    def life(self) -> Life:
        return self.__life
    

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