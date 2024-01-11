from enum import Enum
from pathlib import Path
from rpg.gameplay.attributes import Attribute
from rpg.gamedesign.interval_system import Range
from rpg.gameplay.physiology import Morphology
from rpg.csv import Csv, CsvReader
from rpg.utils import Optional
from rpg.gameplay.genders import Gender
from rpg.colors import Color, ColorPallet

class BreedTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__morphologies: dict[Gender, Morphology] = {}
        self.__skin_colors: list[Color] = []
        
        sizes_in_csv: Csv = CsvReader.read(Path("./resources/size-in-cm.csv"))
        weight_in_csv: Csv = CsvReader.read(Path("./resources/weight-in-kg.csv"))
        body_proportions_in_csv: Csv = CsvReader.read(Path("./resources/body-proportions.csv"))
        skin_color_in_csv: Csv = CsvReader.read(Path("./resources/skins-colors.csv"))
        
        potential_skin_colors: Optional[list[object]] = skin_color_in_csv.get_line_by_header(name)
        potential_sizes: Optional[list[object]] = sizes_in_csv.get_line_by_header(name)
        potential_weights: Optional[list[object]] = weight_in_csv.get_line_by_header(name)
        potential_head: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("head")
        potential_neck: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("neck")
        potential_arm: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("arm")
        potential_hand: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("hand")
        potential_body: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("body")
        potential_leg: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("leg")
        potential_foot: Optional[list[object]] = body_proportions_in_csv.get_line_by_header("foot")
        if (potential_sizes.is_present() and potential_weights.is_present() and potential_skin_colors.is_present()):
            sizes: list[int] = potential_sizes.get()
            weights: list[int] = potential_weights.get()
            head: list[int] = potential_head.get()
            neck: list[int] = potential_neck.get()
            arm: list[int] = potential_arm.get()
            hand: list[int] = potential_hand.get()
            body: list[int] = potential_body.get()
            leg: list[int] = potential_leg.get()
            foot: list[int] = potential_foot.get()
            male_morphology = Morphology(
                size=Range(sizes[0], sizes[1]), 
                weight=Range(weights[0], weights[1]), 
                arm_proportion=Range(arm[0], arm[1]),
                body_proportion=Range(body[0], body[1]),
                foot_proportion=Range(foot[0], foot[1]),
                hand_proportion=Range(hand[0], hand[1]),
                head_proportion=Range(head[0], head[1]),
                leg_proportion=Range(leg[0], leg[1]),
                neck_proportion=Range(neck[0], neck[1]))
            female_morphology = Morphology(
                size=Range(sizes[2], sizes[3]), 
                weight=Range(weights[2], weights[3]),
                arm_proportion=Range(arm[2], arm[3]),
                body_proportion=Range(body[2], body[3]),
                foot_proportion=Range(foot[2], foot[3]),
                hand_proportion=Range(hand[2], hand[3]),
                head_proportion=Range(head[2], head[3]),
                leg_proportion=Range(leg[2], leg[3]),
                neck_proportion=Range(neck[2], neck[3]))
            self.__morphologies[Gender.MAN] = male_morphology
            self.__morphologies[Gender.WOMAN] = female_morphology
            skins_colors_ranges: list[str] = str(potential_skin_colors.get()[0]).split(";")
            for skin_color_range in skins_colors_ranges:
                skin_colors: list[str] = skin_color_range.split("-")
                if (len(skin_colors) == 2):
                    skin_color_pallet: list[Color] = ColorPallet.generate_colors_pallet(Color.from_hexa(skin_colors[0].strip()), Color.from_hexa(skin_colors[1].strip()), 20)
                    for skin_color in skin_color_pallet:
                        self.__skin_colors.append(skin_color)
            
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def skin_colors(self) -> list[Color]:
        return self.__skin_colors

    def get_morphology(self, gender: Gender) -> Morphology:
        if (gender is None):
            raise ValueError()
        return self.__morphologies.get(gender)

class BreedType(Enum):
    HUMAN: BreedTypeValue = BreedTypeValue("HUMAN")
    GNOME: BreedTypeValue = BreedTypeValue("GNOME")
    DRAENEI: BreedTypeValue = BreedTypeValue("DRAENEI")
    NIGHT_ELF: BreedTypeValue = BreedTypeValue("NIGHT_ELF")
    PANDAREN: BreedTypeValue = BreedTypeValue("PANDAREN")
    DWARF: BreedTypeValue = BreedTypeValue("DWARF")
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
        
class Dwarf(Breed):
    def __init__(self) -> None:
        super().__init__(BreedType.DWARF)
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
        breed: Breed|None = None
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
            case BreedType.DWARF:
                breed = BreedFactory.dwarf()
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
    def dwarf() -> Dwarf:
        return Dwarf()
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