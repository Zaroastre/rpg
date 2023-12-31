from abc import ABC, abstractmethod
from enum import Enum
from rpg.gameplay.breeds import BreedType
from rpg.gameplay.classes import ClassType, Class
from rpg.gamedesign.progression_system import Level
from rpg.gameplay.spells import Spell, SpellType, Projectil
from rpg.gameplay.weapons import Weapon
from rpg.gamedesign.character_system import BaseCharacter
from rpg.gameplay.attributes import Attribute

class Attack(ABC):
    @abstractmethod
    def attack(self) -> None:
        raise NotImplementedError()

class AttackStategyType(Enum):
    SPEEL=1,
    WEAPON_TECHNIC=2,
    WEAPON=3,
    UNARMED=4

class AttackStategy:
    def __init__(self, attack_strategy_type: AttackStategyType, attacker: BaseCharacter) -> None:
        self.__attacker: BaseCharacter = attacker
        self.__attack_strategy_type: AttackStategyType = attack_strategy_type
    @property
    def attacker(self) -> BaseCharacter:
        return self.__attacker
    @property
    def attack_strategy_type(self) -> AttackStategyType:
        return self.__attack_strategy_type

    @abstractmethod
    def execute(self, target: BaseCharacter) -> int:
        raise NotImplementedError()

class UnarmedAttackStategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter) -> None:
        super().__init__(AttackStategyType.UNARMED, attacker)
    def execute(self, target: BaseCharacter) -> int:
        strength: int = self.attacker.character_class.get_attribute(Attribute.STRENGTH)
        if (strength == 0):
            strength = 1
        target.life.loose(strength)
        return strength

class RightWeaponAttackStrategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter) -> None:
        super().__init__(AttackStategyType.WEAPON, attacker)
        
    def execute(self, target: BaseCharacter) -> int:
        damage: int = 0
        if (self.attacker.character_class.right_hand_weapon is not None):
            damage = self.attacker.character_class.right_hand_weapon.damage()
        if (damage > 0):
            target.life.loose(damage)
        return damage

class LeftWeaponAttackStrategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter) -> None:
        super().__init__(AttackStategyType.WEAPON, attacker)
        
    def execute(self, target: BaseCharacter) -> int:
        damage: int = 0
        if (self.attacker.character_class.left_hand_weapon is not None):
            damage = self.attacker.character_class.left_hand_weapon.damage()
        if (damage > 0):
            target.life.loose(damage)
        return damage


class RangedWeaponAttackStrategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter) -> None:
        super().__init__(AttackStategyType.WEAPON, attacker)
    
    def execute(self, target: BaseCharacter) -> int:
        if (self.attacker.character_class.right_hand_weapon is not None):
            self.attacker.character_class.right_hand_weapon.damage()

class InstantDamageSpellAttackStrategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter, spell: Spell) -> None:
        super().__init__(AttackStategyType.SPEEL, attacker)
        self.__spell: Spell = spell
    @property
    def spell(self) -> Spell:
        return self.__spell
    def execute(self, target: BaseCharacter) -> int:
        damage: int = 0
        if (self.__spell.can_be_casted()):
            casted_projectil: Projectil = self.__spell.cast()
            casted_projectil.from_position = self.attacker.current_position.copy()
            casted_projectil.to_position = target.current_position.copy()
            self.attacker.character_class.trigged_projectils.append(casted_projectil)
            target.life.loose(casted_projectil.payload)
            damage = casted_projectil.payload
        return damage

class PeriodicDamageSpellAttackStrategy(AttackStategy):
    def __init__(self, attacker: BaseCharacter, spell: Spell) -> None:
        super().__init__(AttackStategyType.SPEEL, attacker)
        self.__spell: Spell = spell
    @property
    def spell(self) -> Spell:
        return self.__spell

    def execute(self, target: BaseCharacter) -> int:
        projectil: Projectil = self.__spell.cast(target)
        return projectil.payload

class AttackStategyChooser:
    def __init__(self, attacker: BaseCharacter) -> None:
        self.__attacker: BaseCharacter = attacker

    def __choose_default_strategy_for_spells_casters(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        damages_spells: list[Spell] = self.__attacker.character_class.spells_book.damages_spells
        infect_spells: list[Spell] = self.__attacker.character_class.spells_book.infect_spells
        
        # Si il y a des sorts
        if (len(damages_spells) > 0 or len(infect_spells) > 0):
            damages_spells_that_can_be_cast: list[Spell] = []
            infect_spells_that_can_be_cast: list[Spell] = []
            
            # Si il y a des sorts qui peuvent être lancé
            if (len(damages_spells) > 0):
                damages_spells_that_can_be_cast = [spell for spell in damages_spells if (self.__attacker.character_class.resource.current >= spell.resource_usage and spell.can_be_casted())]
            if (len(infect_spells_that_can_be_cast) > 0):
                infect_spells_that_can_be_cast = [spell for spell in infect_spells if (self.__attacker.character_class.resource.current >= spell.resource_usage and spell.can_be_casted())]
        
            most_damaded_spells: list[Spell] = []
            most_infected_spells: list[Spell] = []
            
            # Récupère les sorts qui au minimum font le plus de dégats
            if (len(damages_spells_that_can_be_cast) > 0):
                most_damaded_spells = sorted(damages_spells_that_can_be_cast, key=lambda spell: spell.magical_effect_minimum, reverse=True)
            if (len(infect_spells_that_can_be_cast) > 0):
                most_infected_spells = sorted(infect_spells_that_can_be_cast, key=lambda spell: spell.magical_effect_minimum, reverse=True)

            # Récupère le sort qui utilise le moins de mana
            selected_spells: list[Spell] = []
            if (len(most_damaded_spells) > 0):
                selected_spells.append(most_damaded_spells[0])
            if (len(most_infected_spells) > 0):
                selected_spells.append(most_infected_spells[0])
            if (len(selected_spells) > 0):
                less_mana_usage_spell: Spell = sorted(selected_spells, key=lambda spell: spell.resource_usage, reverse=False)[0]
                if (less_mana_usage_spell.spell_type == SpellType.DAMAGE):
                    strategy = InstantDamageSpellAttackStrategy(target, less_mana_usage_spell)
                elif (less_mana_usage_spell.spell_type == SpellType.DAMAGE_OVER_TIME):
                    strategy = PeriodicDamageSpellAttackStrategy(target, less_mana_usage_spell)
        else:
            if (self.__attacker.character_class.right_hand_weapon is not None):
                strategy = RightWeaponAttackStrategy(self.__attacker.character_class.right_hand_weapon)
        return strategy

    def __choose_default_strategy_for_melee_attackers(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        if (self.__attacker.character_class.right_hand_weapon is not None):
            pass
        if (self.__attacker.character_class.left_hand_weapon is not None):
            if (self.__attacker.character_class.left_hand_weapon.stuff_part_type):
                pass
        damages_spells: list[Spell] = self.__attacker.character_class.spells_book.damages_spells
        infect_spells: list[Spell] = self.__attacker.character_class.spells_book.infect_spells
        
        # Si il y a des sorts
        if (len(damages_spells) > 0 or len(infect_spells) > 0):
            damages_spells_that_can_be_cast: list[Spell] = []
            infect_spells_that_can_be_cast: list[Spell] = []
            
            # Si il y a des sorts qui peuvent être lancé
            if (len(damages_spells) > 0):
                damages_spells_that_can_be_cast = [spell for spell in damages_spells if (self.__attacker.character_class.resource.current >= spell.resource_usage and spell.can_be_casted())]
            if (len(infect_spells_that_can_be_cast) > 0):
                infect_spells_that_can_be_cast = [spell for spell in infect_spells if (self.__attacker.character_class.resource.current >= spell.resource_usage and spell.can_be_casted())]
        
            most_damaded_spells: list[Spell] = []
            most_infected_spells: list[Spell] = []
            
            # Récupère les sorts qui au minimum font le plus de dégats
            if (len(damages_spells_that_can_be_cast) > 0):
                most_damaded_spells = sorted(damages_spells_that_can_be_cast, key=lambda spell: spell.magical_effect_minimum, reverse=True)
            if (len(infect_spells_that_can_be_cast) > 0):
                most_infected_spells = sorted(infect_spells_that_can_be_cast, key=lambda spell: spell.magical_effect_minimum, reverse=True)

            # Récupère le sort qui utilise le moins de mana
            selected_spells: list[Spell] = []
            if (len(most_damaded_spells) > 0):
                selected_spells.append(most_damaded_spells[0])
            if (len(most_infected_spells) > 0):
                selected_spells.append(most_infected_spells[0])
            if (len(selected_spells) > 0):
                less_mana_usage_spell: Spell = sorted(selected_spells, key=lambda spell: spell.resource_usage, reverse=False)[0]
                if (less_mana_usage_spell.spell_type == SpellType.DAMAGE):
                    strategy = InstantDamageSpellAttackStrategy(target, less_mana_usage_spell)
                elif (less_mana_usage_spell.spell_type == SpellType.DAMAGE_OVER_TIME):
                    strategy = PeriodicDamageSpellAttackStrategy(target, less_mana_usage_spell)
        else:
            if (self.__attacker.character_class.right_hand_weapon is not None):
                strategy = RightWeaponAttackStrategy(self.__attacker)
        return strategy

    def __choose_strategy_for_mage(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_spells_casters(target)
    def __choose_strategy_for_priest(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_spells_casters(target)
    def __choose_strategy_for_demonist(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_spells_casters(target)
    def __choose_strategy_for_shaman(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        return strategy
    def __choose_strategy_for_druid(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        return strategy
    def __choose_strategy_for_paladin(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        return strategy
    def __choose_strategy_for_hunter(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        return strategy
    def __choose_strategy_for_monk(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_melee_attackers(target)
    def __choose_strategy_for_warrior(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_melee_attackers(target)
    def __choose_strategy_for_rogue(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_melee_attackers(target)
    def __choose_strategy_for_death_knight(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_melee_attackers(target)
    def __choose_strategy_for_demon_hunter(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_melee_attackers(target)

    def choose_best_attack_strategy(self, target: BaseCharacter) -> AttackStategy:
        target: BaseCharacter = target
        strategy: AttackStategy = UnarmedAttackStategy(self.__attacker)
        match (self.__attacker.character_class.class_type):
            case ClassType.MAGE:
                strategy = self.__choose_strategy_for_mage(target)
            case ClassType.PRIEST:
                strategy = self.__choose_strategy_for_priest(target)
            case ClassType.DEMONIST:
                strategy = self.__choose_strategy_for_demonist(target)
            case ClassType.SHAMAN:
                strategy = self.__choose_strategy_for_shaman(target)
            case ClassType.DRUID:
                strategy = self.__choose_strategy_for_druid(target)
            case ClassType.PALADIN:
                strategy = self.__choose_strategy_for_paladin(target)
            case ClassType.WARRIOR:
                strategy = self.__choose_strategy_for_warrior(target)
            case ClassType.MONK:
                strategy = self.__choose_strategy_for_monk(target)
            case ClassType.HUNTER:
                strategy = self.__choose_strategy_for_hunter(target)
            case ClassType.ROGUE:
                strategy = self.__choose_strategy_for_rogue(target)
            case ClassType.DEATH_KNIGHT:
                strategy = self.__choose_strategy_for_death_knight(target)
            case ClassType.DEMON_HUNTER:
                strategy = self.__choose_strategy_for_demon_hunter(target)
        # Définir les règles pour choisir la meilleure stratégie d'attaque
        return strategy