from abc import ABC, abstractmethod
from rpg.gameplay.breeds import BreedType
from rpg.gameplay.classes import ClassType, Class
from rpg.gamedesign.progression_system import Level
from rpg.gameplay.spells import Spell, SpellType
from rpg.gameplay.weapons import Weapon
from rpg.gamedesign.character_system import BaseCharacter

class Attack(ABC):
    @abstractmethod
    def attack(self) -> None:
        raise NotImplementedError()

class AttackStategy:
    @abstractmethod
    def execute(self, target: BaseCharacter) -> None:
        raise NotImplementedError()

class UnarmedAttackStategy(AttackStategy):
    def __init__(self) -> None:
        pass
    def execute(self, target: BaseCharacter) -> None:
        pass

class WeaponAttackStrategy(AttackStategy):
    def __init__(self, right_weapon: Weapon, left_weapon: Weapon) -> None:
        self.__right_weapon: Weapon = right_weapon
        self.__left_weapon: Weapon = left_weapon
        
    def execute(self, target: BaseCharacter) -> None:
        self.__right_weapon.damage(target)
        if self.__left_weapon is not None:
            self.__left_weapon.damage(target)

class RangedWeaponAttackStrategy(AttackStategy):
    def __init__(self, weapon: Weapon) -> None:
        self.__weapon: Weapon = weapon
    
    def execute(self, target: BaseCharacter) -> None:
        self.__weapon.damage(target)

class InstantDamageSpellAttackStrategy(AttackStategy):
    def __init__(self, spell: Spell) -> None:
        self.__spell: Spell = spell
    
    def execute(self, target: BaseCharacter) -> None:
        self.__spell.cast()

class PeriodicDamageSpellAttackStrategy(AttackStategy):
    def __init__(self, spell: Spell) -> None:
        self.__spell: Spell = spell
    
    def execute(self, target: BaseCharacter) -> None:
        self.__spell.cast(target)

class AttackStategyChooser:
    def __init__(self, attacker: BaseCharacter) -> None:
        self.__attacker: BaseCharacter = attacker.copy()

    def __choose_default_strategy_for_spells_casters(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
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
                    strategy = InstantDamageSpellAttackStrategy(less_mana_usage_spell)
                elif (less_mana_usage_spell.spell_type == SpellType.DAMAGE_OVER_TIME):
                    strategy = PeriodicDamageSpellAttackStrategy(less_mana_usage_spell)
        else:
            if (self.__attacker.character_class.right_hand_weapon is not None):
                strategy = WeaponAttackStrategy(self.__attacker.character_class.right_hand_weapon)
        return strategy

    def __choose_default_strategy_for_melee_attackers(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
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
                    strategy = InstantDamageSpellAttackStrategy(less_mana_usage_spell)
                elif (less_mana_usage_spell.spell_type == SpellType.DAMAGE_OVER_TIME):
                    strategy = PeriodicDamageSpellAttackStrategy(less_mana_usage_spell)
        else:
            if (self.__attacker.character_class.right_hand_weapon is not None):
                strategy = WeaponAttackStrategy(self.__attacker.character_class.right_hand_weapon, self.__attacker.character_class.left_hand_weapon)
        return strategy

    def __choose_strategy_for_mage(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_spells_casters(target)
    def __choose_strategy_for_priest(self, target: BaseCharacter) -> AttackStategy:
        return self.__choose_default_strategy_for_spells_casters(target)
    def __choose_strategy_for_demonist(self, target: BaseCharacter) -> AttackStategy:
        print("Choosing for demonists")
        return self.__choose_default_strategy_for_spells_casters(target)
    
    def __choose_strategy_for_shaman(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
        return strategy
    def __choose_strategy_for_druid(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
        return strategy
    def __choose_strategy_for_paladin(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
        return strategy
    def __choose_strategy_for_hunter(self, target: BaseCharacter) -> AttackStategy:
        strategy: AttackStategy = UnarmedAttackStategy()
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
        target: BaseCharacter = target.copy()
        strategy: AttackStategy = UnarmedAttackStategy()
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