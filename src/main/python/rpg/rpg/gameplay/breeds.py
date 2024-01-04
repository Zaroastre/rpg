from enum import Enum
from rpg.gameplay.attributes import Attribute
from rpg.gamedesign.interval_system import Range

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
    GOBLIN: BreedTypeValue = BreedTypeValue("GOBLIN")
    WORGEN: BreedTypeValue = BreedTypeValue("WORGEN")


class Breed:
    def __init__(self, breed_type: BreedType) -> None:
        super().__init__()
        self.__breed_type: BreedType = breed_type
        self._attributes: dict[Attribute, int] = {}

    @property
    def breed_type(self) -> BreedType:
        return self.__breed_type
    
    @property
    def attributes(self) -> list[Attribute]:
        return list(self._attributes.keys())

    def get_attribute(self, attribute: Attribute) -> int:
        value: int = 0
        if (attribute in list(self._attributes.keys())):
            value = self._attributes.get(attribute)
        return value

class Human(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.HUMAN)
        self._attributes[Attribute.STRENGTH] = 20
        self._attributes[Attribute.AGILITY] = 20
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 20
        self._attributes[Attribute.SPIRIT] = 20
        
        
class Gnome(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.GNOME)
        self._attributes[Attribute.STRENGTH] = 15
        self._attributes[Attribute.AGILITY] = 22
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 23
        self._attributes[Attribute.SPIRIT] = 20
        
class Draenei(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.DRAENEI)
        self._attributes[Attribute.STRENGTH] = 21
        self._attributes[Attribute.AGILITY] = 17
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 20
        self._attributes[Attribute.SPIRIT] = 22
        
class NightElf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.NIGHT_ELF)
        self._attributes[Attribute.STRENGTH] = 16
        self._attributes[Attribute.AGILITY] = 24
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 20
        self._attributes[Attribute.SPIRIT] = 20
        
class Pandaren(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.PANDAREN)
        self._attributes[Attribute.STRENGTH] = 20
        self._attributes[Attribute.AGILITY] = 18
        self._attributes[Attribute.STAMANIA] = 21
        self._attributes[Attribute.INTELLECT] = 19
        self._attributes[Attribute.SPIRIT] = 22
        
class Knowrf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.KNOWF)
        self._attributes[Attribute.STRENGTH] = 25
        self._attributes[Attribute.AGILITY] = 16
        self._attributes[Attribute.STAMANIA] = 21
        self._attributes[Attribute.INTELLECT] = 19
        self._attributes[Attribute.SPIRIT] = 19
        
class BloodElf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.BLOOD_ELF)
        self._attributes[Attribute.STRENGTH] = 17
        self._attributes[Attribute.AGILITY] = 22
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 23
        self._attributes[Attribute.SPIRIT] = 18
        
class Undead(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.UNDEAD)
        self._attributes[Attribute.STRENGTH] = 19
        self._attributes[Attribute.AGILITY] = 18
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 18
        self._attributes[Attribute.SPIRIT] = 25
        
class Orc(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.ORC)
        self._attributes[Attribute.STRENGTH] = 23
        self._attributes[Attribute.AGILITY] = 17
        self._attributes[Attribute.STAMANIA] = 21
        self._attributes[Attribute.INTELLECT] = 17
        self._attributes[Attribute.SPIRIT] = 22
        
class Troll(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.TROLL)
        self._attributes[Attribute.STRENGTH] = 21
        self._attributes[Attribute.AGILITY] = 22
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 16
        self._attributes[Attribute.SPIRIT] = 21
        
class Tauren(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.TAUREN)
        self._attributes[Attribute.STRENGTH] = 25
        self._attributes[Attribute.AGILITY] = 16
        self._attributes[Attribute.STAMANIA] = 21
        self._attributes[Attribute.INTELLECT] = 16
        self._attributes[Attribute.SPIRIT] = 22
        
class Goblin(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.GOBLIN)
        self._attributes[Attribute.STRENGTH] = 17
        self._attributes[Attribute.AGILITY] = 22
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 17
        self._attributes[Attribute.SPIRIT] = 18
        
class Worgen(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.WORGEN)
        self._attributes[Attribute.STRENGTH] = 23
        self._attributes[Attribute.AGILITY] = 22
        self._attributes[Attribute.STAMANIA] = 20
        self._attributes[Attribute.INTELLECT] = 14
        self._attributes[Attribute.SPIRIT] = 19
        


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
            case BreedType.GOBLIN:
                breed = BreedFactory.goblin()
            case BreedType.WORGEN:
                breed = BreedFactory.worgen()
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
    @staticmethod
    def goblin() -> Goblin:
        return Goblin()
    @staticmethod
    def worgen() -> Worgen:
        return Worgen()