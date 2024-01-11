from abc import ABC
from enum import Enum

from rpg.gamedesign.interval_system import Range
from rpg.gamedesign.progression_system import Rank
from rpg.gameplay.attributes import Attribute
from rpg.gameplay.powers import Chi, Energy, Mana, Power, PowerType, Rage, Rune
from rpg.gameplay.qualities import QualityType
from rpg.gameplay.spells import Spell, SpellBuilder, SpellsBook, SpellType, Projectil
from rpg.gameplay.stuffs import StuffPartType
from rpg.gameplay.talents import TalentsBook, TalentsBookFactory, TalentsTree
from rpg.gameplay.weapons import Weapon, WeaponFactory, WeaponType
from rpg.colors import Color

class ClassTypeValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: str = name
        self.__color: Color = color
        
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.__color.to_tuple()

class ClassType(Enum):
    DEMONIST: ClassTypeValue = ClassTypeValue("DEMONIST", Color(135,136,238))
    MAGE: ClassTypeValue = ClassTypeValue("MAGE", Color(63,199,235))
    PRIEST: ClassTypeValue = ClassTypeValue("PRIEST", Color(255,255,255))
    MONK: ClassTypeValue = ClassTypeValue("MONK", Color(0,255,152))
    HUNTER: ClassTypeValue = ClassTypeValue("HUNTER", Color(170,211,114))
    ROGUE: ClassTypeValue = ClassTypeValue("ROGUE", Color(255,244,104))
    PALADIN: ClassTypeValue = ClassTypeValue("PALADIN", Color(244,140,186))
    WARRIOR: ClassTypeValue = ClassTypeValue("WARRIOR", Color(198,155,109))
    SHAMAN: ClassTypeValue = ClassTypeValue("SHAMAN", Color(0,112,22))
    DRUID: ClassTypeValue = ClassTypeValue("DRUID", Color(255,124,10))
    DEMON_HUNTER: ClassTypeValue = ClassTypeValue("DEMON_HUNTER", Color(163,48,201))
    DEATH_KNIGHT: ClassTypeValue = ClassTypeValue("DEATH_KNIGHT", Color(196,30,58))
    # EVOKER: ClassTypeValue = ClassTypeValue("EVOKER", Color(51,147,127))
    
    @staticmethod
    def is_damage_spell_caster(class_type) -> bool:
        is_a_spell_caster: bool = False
        if (class_type is not None):
            if (class_type in [ClassType.DEMONIST, ClassType.MAGE, ClassType.PRIEST, ClassType.PALADIN, ClassType.MONK, ClassType.SHAMAN, ClassType.DRUID]):
                is_a_spell_caster = True
        return is_a_spell_caster

    @staticmethod
    def is_health_spell_caster(class_type) -> bool:
        is_a_spell_caster: bool = False
        if (class_type is not None):
            if (class_type in [ClassType.PRIEST, ClassType.PALADIN, ClassType.MONK, ClassType.SHAMAN, ClassType.DRUID]):
                is_a_spell_caster = True
        return is_a_spell_caster
    
class Class(ABC):
    def __init__(self, class_type: ClassType, resource: Power, talents_book: TalentsBook) -> None:
        self.__class_type: ClassType = class_type
        self.__resource: Power = resource
        self.__talents_book: TalentsBook = talents_book
        self.__spells_book: SpellsBook = SpellsBook()
        self._left_hand_supported_weapons: list[WeaponType] = []
        self._right_hand_supported_weapons: list[WeaponType] = []
        self._left_hand_weapon: Weapon = None
        self._right_hand_weapon: Weapon = None
        self._attributes: dict[Attribute, int] = {}
        self.__trigged_projectils: list[Projectil] = []

    def use_weapon(self, weapon: Weapon|None):
        if ((weapon is None) or (weapon.weapon_type in self._right_hand_supported_weapons)):
            self._right_hand_weapon = weapon
        elif ((weapon is None) or (weapon.weapon_type in self._left_hand_supported_weapons)):
            self._left_hand_weapon = weapon
        else:
            raise ValueError("This class cannot use this weapon")

    @property
    def trigged_projectils(self) -> list[Projectil]:
        return self.__trigged_projectils
    @property
    def allowed_weapons(self) -> list[WeaponType]:
        return list(self._left_hand_supported_weapons + self._right_hand_supported_weapons)
    
    @property
    def left_hand_allowed_weapons(self) -> list[WeaponType]:
        return self._left_hand_supported_weapons.copy()
    @property
    def right_hand_allowed_weapons(self) -> list[WeaponType]:
        return self._right_hand_supported_weapons.copy()
    @property
    def left_hand_weapon(self) -> Weapon:
        return self._left_hand_weapon
    
    @property
    def right_hand_weapon(self) -> Weapon:
        return self._right_hand_weapon
    @property
    def spells_book(self) -> SpellsBook:
        return self.__spells_book
    @property
    def class_type(self) -> ClassType:
        return self.__class_type
    
    @property
    def resource(self) -> Power:
        return self.__resource

    @property
    def talents_book(self) -> TalentsBook:
        return self.__talents_book
    @property
    def attributes(self) -> list[Attribute]:
        return list(self._attributes.keys())

    def get_attribute(self, attribute: Attribute) -> int:
        value: int = 0
        if (attribute in list(self._attributes.keys())):
            value = self._attributes.get(attribute)
        return value
    
class Paladin(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.PALADIN, Mana(), TalentsBookFactory.paladin())
        self.__casted_spells: list[Spell] = []
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self.spells_book.learn(
            SpellBuilder("Holy Light")
                .description("Heals a friendly target for instant_health.minimum to instant_health.maximum.")
                .rank(Rank(70))
                .resource_usage(35)
                .incantation_duration(2.5)
                .cooldown(1.5)
                .instant_health(Range(39, 47))
                .spell_color(Color(255,255,0))
                .build())
        self._right_hand_weapon = WeaponFactory.one_hand_mace("Little Mace", "Little mace", StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 5
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 17
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 9

class Demonist(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEMONIST, Mana(), TalentsBookFactory.demonist())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.WAND)

        self.spells_book.learn(
            SpellBuilder("Shadow Bolt")
                .description("Sends a shadowy bolt at the enemy, causing instant_damage.minimum to instant_damage.maximum Shadow damage.")
                .rank(Rank(70))
                .resource_usage(25)
                .incantation_duration(1.7)
                .cooldown(1.5)
                .instant_damage(Range(12, 16))
                .spell_color(Color(100,0,255))
                .build())
        self.spells_book.learn(
            SpellBuilder("Immolate")
                .description("Burns the enemy for instant_damage.maximum Fire damage and then an additional 20 Fire damage over 15 sec.")
                .rank(Rank(70))
                .resource_usage(25)
                .incantation_duration(2.0)
                .cooldown(1.5)
                .instant_damage(Range(8, 8))
                .periodic_damage(Range(1,2), 15.0)
                .spell_color(Color(255,50,0))
                .build())
        self._right_hand_weapon = WeaponFactory.stave(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 12
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 6
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 13

class Mage(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.MAGE, Mana(), TalentsBookFactory.mage())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.WAND)
        self.spells_book.learn(
            SpellBuilder("Fireball")
                .description("Sends a shadowy bolt at the enemy, causing instant_damage.minimum to instant_damage.maximum Shadow damage.")
                .rank(Rank(70))
                .resource_usage(30)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_damage(Range(16, 25))
                .spell_color(Color(255,0,0))
                .build())
        self.spells_book.learn(
            SpellBuilder("Frostball")
                .description("Sends a shadowy bolt at the enemy, causing instant_damage.minimum to instant_damage.maximum Shadow damage.")
                .rank(Rank(70))
                .resource_usage(30)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_damage(Range(16, 25))
                .spell_color(Color(0,0,255))
                .build())
        self._right_hand_weapon = WeaponFactory.stave(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 10
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 8
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 13

class Priest(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.PRIEST, Mana(), TalentsBookFactory.priest())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.WAND)
        self.spells_book.learn(
            SpellBuilder("Lesser Heal")
                .description("Heal your target for instant_health.minimum to instant_health.maximum.")
                .rank(Rank(70))
                .resource_usage(30)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_health(Range(39, 47))
                .spell_color(Color(255,255,200))
                .build())
        
        self.spells_book.learn(
            SpellBuilder("Smite")
                .description("Sends a shadowy bolt at the enemy, causing instant_health.minimum to instant_health.maximum Shadow damage.")
                .rank(Rank(70))
                .resource_usage(30)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_damage(Range(46, 56))
                .spell_color(Color(0,0,255))
                .build())
        self._right_hand_weapon = WeaponFactory.stave(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 12
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 10
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 9

class Hunter(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.HUNTER, Mana(), TalentsBookFactory.hunter())
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.DAGGER)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.BOW)
        self._right_hand_supported_weapons.append(WeaponType.GUN)
        self._right_hand_supported_weapons.append(WeaponType.CROSSBOW)
        self.spells_book.learn(
            SpellBuilder("Raptor Strike")
                .description("A strong attack that increases melee damage by 5.")
                .rank(Rank(70))
                .resource_usage(15)
                .cooldown(6.0)
                .instant_damage(Range(46, 56))
                .build())
        self._right_hand_weapon = WeaponFactory.bow(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 15
        self._attributes[Attribute.INTELLECT] = 10
        self._attributes[Attribute.STRENGTH] = 10
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 8

class Shaman(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.SHAMAN, Mana(), TalentsBookFactory.shaman())
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.DAGGER)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self.spells_book.learn(
            SpellBuilder("Lightning Bolt")
                .description("Casts a bolt of lightning at the target for instant_health.minimum to instant_health.maximum Nature damage.")
                .rank(Rank(70))
                .resource_usage(15)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_damage(Range(15, 17))
                .build())
        self.spells_book.learn(
            SpellBuilder("Healing Wave")
                .description("Heal a friendly target for instant_health.minimum to instant_health.maximum.")
                .rank(Rank(70))
                .resource_usage(25)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_health(Range(36, 47))
                .build())
        self._right_hand_weapon = WeaponFactory.one_hand_axe(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 15
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 7
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 9

class Druid(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DRUID, Mana(), TalentsBookFactory.druid())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self.spells_book.learn(
            SpellBuilder("Wrath")
                .description("Causes instant_damage.minimum to instant_damage.maximum Nature damage to the target")
                .rank(Rank(70))
                .resource_usage(20)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_damage(Range(13, 16))
                .build())
        self.spells_book.learn(
            SpellBuilder("Healing Touch")
                .description("Heals a friendly target for instant_health.minimum to instant_health.maximum.")
                .rank(Rank(70))
                .resource_usage(25)
                .incantation_duration(1.5)
                .cooldown(1.5)
                .instant_health(Range(40, 55))
                .build())
        self._right_hand_weapon = WeaponFactory.stave(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 15
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 7
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 9

class DemonHunter(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEMON_HUNTER, Rune(), TalentsBookFactory.demon_hunter())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        self._left_hand_supported_weapons.append(WeaponType.DAGGER)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_weapon = WeaponFactory.dagger(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._left_hand_weapon = WeaponFactory.dagger(None, None, StuffPartType.LEFT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 10
        self._attributes[Attribute.INTELLECT] = 10
        self._attributes[Attribute.STRENGTH] = 15
        self._attributes[Attribute.STAMANIA] = 15
        self._attributes[Attribute.SPIRIT] = 7

class Rogue(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.ROGUE, Energy(), TalentsBookFactory.rogue())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._left_hand_supported_weapons.append(WeaponType.DAGGER)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self.spells_book.learn(
            SpellBuilder("Eviscerate")
                .description("Heals a friendly target for instant_damage.minimum to instant_damage.maximum.")
                .rank(Rank(70))
                .resource_usage(35)
                .cooldown(1.0)
                .instant_damage(Range(5, 25))
                .build())
        
        self.spells_book.learn(
            SpellBuilder("Sinister Strike")
                .description("An instant strike that causes instant_damage.maximum damage in addition to your normal weapon damage.  Awards 1 combo point.")
                .rank(Rank(70))
                .resource_usage(45)
                .cooldown(1.0)
                .instant_damage(Range(3, 3))
                .build())
        
        self.spells_book.learn(
            SpellBuilder("Stealth")
                .description("Heals a friendly target for 40 to 55.")
                .rank(Rank(70))
                .cooldown(10.0)
                .build())
       
        self._right_hand_weapon = WeaponFactory.dagger(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._left_hand_weapon = WeaponFactory.dagger(None, None, StuffPartType.LEFT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 15
        self._attributes[Attribute.INTELLECT] = 8
        self._attributes[Attribute.STRENGTH] = 14
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 6

class Monk(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.MONK, Chi(), TalentsBookFactory.monk())
        self._right_hand_supported_weapons.append(WeaponType.DAGGER)
        self._left_hand_supported_weapons.append(WeaponType.DAGGER)
        self._right_hand_supported_weapons.append(WeaponType.STAVE)
        self._right_hand_weapon = WeaponFactory.stave(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 15
        self._attributes[Attribute.INTELLECT] = 12
        self._attributes[Attribute.STRENGTH] = 7
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 9
 
class Warrior(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.WARRIOR, Rage(), TalentsBookFactory.warrior())
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._left_hand_supported_weapons.append(WeaponType.POLEARM)
        self._left_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._left_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._left_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        
        self.spells_book.learn(
            SpellBuilder("Heroic Strike")
                .description("A strong attack that increases melee damage by instant_damage.maximum and causes a high amount of threat.")
                .rank(Rank(70))
                .resource_usage(15)
                .instant_damage(Range(11, 11))
                .build())
        self._right_hand_weapon = WeaponFactory.two_hands_sword(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 10
        self._attributes[Attribute.INTELLECT] = 8
        self._attributes[Attribute.STRENGTH] = 17
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 8

class DeathKnight(Class):
    def __init__(self) -> None:
        super().__init__(ClassType.DEATH_KNIGHT, Rune(), TalentsBookFactory.death_knight())
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._right_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)
        self._right_hand_supported_weapons.append(WeaponType.POLEARM)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_MACE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_AXE)
        self._right_hand_supported_weapons.append(WeaponType.TWO_HANDS_SWORD)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_MACE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_AXE)
        self._left_hand_supported_weapons.append(WeaponType.ONE_HAND_SWORD)

        self._right_hand_weapon = WeaponFactory.one_hand_sword(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._left_hand_weapon = WeaponFactory.one_hand_sword(None, None, StuffPartType.LEFT_HAND_OBJECT, QualityType.COMMON, 1, Range(1, 5), 1.0)
        self._attributes[Attribute.AGILITY] = 13
        self._attributes[Attribute.INTELLECT] = 7
        self._attributes[Attribute.STRENGTH] = 17
        self._attributes[Attribute.STAMANIA] = 11
        self._attributes[Attribute.SPIRIT] = 7

class ClassFactory:
    @staticmethod
    def create(class_type: ClassType) -> Class:
        character_class: Class
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
            case ClassType.ROGUE:
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
