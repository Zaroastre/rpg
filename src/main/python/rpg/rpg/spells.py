from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from threading import Thread
from time import sleep

from rpg.breeds import Breed
from rpg.gamedesign.character_system import AbstractCharacter
from rpg.gamedesign.progression_system import Rank
from rpg.resources import RessourceType
from rpg.gamedesign.interval_system import Range

class SpellTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        
    @property
    def name(self) -> str:
        return self.__name

class SpellType(Enum):
    HEALTH_OVER_TIME: SpellTypeValue = SpellTypeValue("HEALTH_OVER_TIME"),
    INCREASE_STAT_OVER_TIME: SpellTypeValue = SpellTypeValue("INCREASE_STAT_OVER_TIME"),
    DAMAGE_OVER_TIME: SpellTypeValue = SpellTypeValue("DAMAGE_OVER_TIME"),
    DECREASE_STAT_OVER_TIME: SpellTypeValue = SpellTypeValue("DECREASE_STAT_OVER_TIME"),
    HEALTH: SpellTypeValue = SpellTypeValue("HEALTH"),
    DAMAGE: SpellTypeValue = SpellTypeValue("DAMAGE")

class Spell(ABC):
    def __init__(
            self, 
            name: str, 
            description: str, 
            rank: Rank, 
            spell_type: SpellType,
            resource_usage: int,
            incantation_duration: float, 
            cooldown: float,
            instant_damage: Range,
            periodic_damage: Range,
            instant_health: Range,
            periodic_health: Range,
            effect_duration: float
            ) -> None:
        self.__name: str = name
        self.__description: str = description
        self.__rank: Rank = rank
        self.__cooldown: float = cooldown
        self.__incantation_duration: float = incantation_duration
        self.__resource_usage: int = resource_usage
        self.__last_cast_timestamp: int = 0
        self.__spell_type: SpellType = spell_type
        self.__instant_health: Range = instant_health
        self.__instant_damage: Range = instant_damage
        self.__periodic_health: Range = periodic_health
        self.__periodic_damage: Range = periodic_damage
        self.__effect_duration: float = effect_duration
    @property
    def effect_duration(self) -> float:
        return self.__effect_duration
    @property
    def magical_effect_minimum(self) -> int:
        minimum: int = 0
        if (self.__instant_health is not None):
            minimum = self.__instant_health.minimum
        elif (self.__instant_damage is not None):
            minimum = self.__instant_damage.minimum
        elif (self.__periodic_health is not None):
            minimum = self.__periodic_health.minimum
        elif (self.__periodic_damage is not None):
            minimum = self.__periodic_damage.minimum
        return minimum
    @property
    def magical_effect_maximum(self) -> int:
        maximum: int = 0
        if (self.__instant_health is not None):
            maximum = self.__instant_health.maximum
        elif (self.__instant_damage is not None):
            maximum = self.__instant_damage.maximum
        elif (self.__periodic_health is not None):
            maximum = self.__periodic_health.maximum
        elif (self.__periodic_damage is not None):
            maximum = self.__periodic_damage.maximum
        return maximum
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        text: str = self.__description
        if (self.__instant_health is not None):
            text = text.replace("instant_health.minimum", str(self.__instant_health.minimum))
            text = text.replace("instant_health.maximum", str(self.__instant_health.maximum))
        if (self.__instant_damage is not None):
            text = text.replace("instant_damage.minimum", str(self.__instant_damage.minimum))
            text = text.replace("instant_damage.maximum", str(self.__instant_damage.maximum))
        if (self.__periodic_health is not None):
            text = text.replace("periodic_health.minimum", str(self.__periodic_health.minimum))
            text = text.replace("periodic_health.maximum", str(self.__periodic_health.maximum))
        if (self.__periodic_damage is not None):
            text = text.replace("periodic_damage.minimum", str(self.__periodic_damage.minimum))
            text = text.replace("periodic_damage.maximum", str(self.__periodic_damage.maximum))
        return text

    @property
    def rank(self) -> int:
        return self.__rank
    
    @property
    def cooldown(self) -> float:
        return self.__cooldown
    
    @property
    def incantation_duration(self) -> float:
        return self.__incantation_duration
    
    @property
    def resource_usage(self) -> int:
        return self.__resource_usage
    @property
    def last_cast_timestamp(self) -> int:
        return self.__last_cast_timestamp
    
    @property
    def spell_type(self) -> SpellType:
        return self.__spell_type
    
    def can_be_casted(self) -> bool:
        now: float = datetime.now().timestamp()
        return (self.__last_cast_timestamp + self.__cooldown) <= now
    
    def _update_last_cast_timestamp(self):
        self.__last_cast_timestamp = datetime.now().timestamp()
        
    @abstractmethod
    def cast(self, target: AbstractCharacter):
        raise NotImplementedError()

class TemporalSpell(Thread):
    def __init__(self, interval_in_milliseconds: int, points: int, duration_in_milliseconds: int, targets: list[AbstractCharacter]) -> None:
        super().__init__()
        self.__interval_in_milliseconds: int = interval_in_milliseconds
        self.__duration_in_milliseconds: int = duration_in_milliseconds
        self.__points: int = points
        self.__targets: list[AbstractCharacter] = targets
        self.__is_processing: bool = False
    @property
    def interval_in_milliseconds(self) -> int:
        return self.__interval_in_milliseconds
    @property
    def duration_in_milliseconds(self) -> int:
        return self.__duration_in_milliseconds
    @property
    def points(self) -> int:
        return self.__points
    @property
    def targets(self) -> list[AbstractCharacter]:
        return self.__targets.copy()
    @property
    def is_processing(self) -> bool:
        return self.__is_processing

    def cancel_effect(self) -> None:
        self.__is_processing = False
    
    def run(self) -> None:
        self.__is_processing = True

class HealEffectTemporalSpell(TemporalSpell):
    def __init__(self, interval_in_milliseconds: int, effect: int, duration_in_milliseconds: int, targets: list) -> None:
        super().__init__(interval_in_milliseconds, effect, duration_in_milliseconds, targets)
        
    def run(self) -> None:
        super().run()
        cast_datetime: float = datetime.now().timestamp()
        while (self.is_processing and (datetime.now().timestamp() < (cast_datetime + self.duration_in_milliseconds))):
            for target in self.targets:
                target.life.heal(self.points)
            sleep(self.interval_in_milliseconds)
            
class DamageEffectTemporalSpell(TemporalSpell):
    def __init__(self, interval_in_milliseconds: int, effect: int, duration_in_milliseconds: int, targets: list) -> None:
        super().__init__(interval_in_milliseconds, effect, duration_in_milliseconds, targets)
        
    def run(self) -> None:
        super().run()
        cast_datetime: float = datetime.now().timestamp()
        while (self.is_processing and (datetime.now().timestamp() < (cast_datetime + self.duration_in_milliseconds))):
            for target in self.targets:
                if (target.life.is_alive()):
                    target.life.loose(self.points)
            sleep(self.interval_in_milliseconds)

class DamageSpell(Spell):
    def __init__(self, name: str, description: str, rank: Rank, resource_usage: int, incantation_duration: float, cooldown: float, instant_damage: Range, periodic_damage: Range, instant_health: Range, periodic_health: Range, effect_duration: float) -> None:
        super().__init__(name, description, rank, SpellType.DAMAGE, resource_usage, incantation_duration, cooldown, instant_damage, periodic_damage, instant_health, periodic_health, effect_duration)

    def cast(self, target: AbstractCharacter):
        pass

class GuardianSpell(Spell):
    def __init__(self, name: str, description: str, rank: Rank, resource_usage: int, incantation_duration: float, cooldown: float, instant_damage: Range, periodic_damage: Range, instant_health: Range, periodic_health: Range, effect_duration: float) -> None:
        super().__init__(name, description, rank, SpellType.HEALTH_OVER_TIME, resource_usage, incantation_duration, cooldown, instant_damage, periodic_damage, instant_health, periodic_health, effect_duration)
    def cast(self, target: AbstractCharacter):
        pass
class HealthSpell(Spell):
    def __init__(self, name: str, description: str, rank: Rank, resource_usage: int, incantation_duration: float, cooldown: float, instant_damage: Range, periodic_damage: Range, instant_health: Range, periodic_health: Range, effect_duration: float) -> None:
        super().__init__(name, description, rank, SpellType.HEALTH, resource_usage, incantation_duration, cooldown, instant_damage, periodic_damage, instant_health, periodic_health, effect_duration)
    def cast(self, target: AbstractCharacter):
        pass
class InfectSpell(Spell):
    def __init__(self, name: str, description: str, rank: Rank, resource_usage: int, incantation_duration: float, cooldown: float, instant_damage: Range, periodic_damage: Range, instant_health: Range, periodic_health: Range, effect_duration: float) -> None:
        super().__init__(name, description, rank, SpellType.DAMAGE_OVER_TIME, resource_usage, incantation_duration, cooldown, instant_damage, periodic_damage, instant_health, periodic_health, effect_duration)
    def cast(self, target: AbstractCharacter):
        pass
class SpellBuilder:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__description: str = None
        self.__rank: Rank = None
        self.__cooldown: float = 0.0
        self.__incantation_duration: float = 0.0
        self.__effect_duration: float = 0.0
        self.__resource_usage: int = None
        self.__spell_type: SpellType = None
        self.__instant_health: Range = None
        self.__instant_damage: Range = None
        self.__periodic_health: Range = None
        self.__periodic_damage: Range = None
    def description(self, description: str):
        self.__description = description
        return self
    def rank(self, rank: Rank):
        self.__rank = rank
        return self
    def cooldown(self, cooldown: float):
        self.__cooldown = cooldown
        return self
    def resource_usage(self, resource_usage: int):
        self.__resource_usage = resource_usage
        return self
    def incantation_duration(self, incantation_duration: float):
        self.__incantation_duration = incantation_duration
        return self
    def spell_type(self, spell_type: SpellType):
        self.__spell_type = spell_type
        return self
    def instant_health(self, instant_health: Range):
        self.__instant_health = instant_health
        return self
    def instant_damage(self, instant_damage: Range):
        self.__instant_damage = instant_damage
        return self
    def periodic_health(self, total_points: Range, duration: float):
        self.__periodic_health = total_points
        self.__effect_duration = duration
        return self
    def periodic_damage(self, total_points: Range, duration: float):
        self.__periodic_damage = total_points
        self.__effect_duration = duration
        return self
    def build(self) -> Spell:
        spell: Spell = None
        if (self.__periodic_damage is not None):
            spell = InfectSpell(
                self.__name,
                self.__description, 
                self.__rank, 
                self.__resource_usage, 
                self.__incantation_duration, 
                self.__cooldown, 
                self.__instant_damage, 
                self.__periodic_damage, 
                self.__instant_health, 
                self.__periodic_health,
                self.__effect_duration
            )
        elif (self.__periodic_health is not None):
            spell = GuardianSpell(
                self.__name,
                self.__description, 
                self.__rank, 
                self.__resource_usage, 
                self.__incantation_duration, 
                self.__cooldown, 
                self.__instant_damage, 
                self.__periodic_damage, 
                self.__instant_health, 
                self.__periodic_health,
                self.__effect_duration
            )
        elif (self.__instant_damage is not None):
            spell = DamageSpell(
                self.__name,
                self.__description, 
                self.__rank, 
                self.__resource_usage, 
                self.__incantation_duration, 
                self.__cooldown, 
                self.__instant_damage, 
                self.__periodic_damage, 
                self.__instant_health, 
                self.__periodic_health,
                self.__effect_duration
            )
        elif (self.__instant_health is not None):
            spell = HealthSpell(
                self.__name,
                self.__description, 
                self.__rank, 
                self.__resource_usage, 
                self.__incantation_duration, 
                self.__cooldown, 
                self.__instant_damage, 
                self.__periodic_damage, 
                self.__instant_health, 
                self.__periodic_health,
                self.__effect_duration
            )
        return spell

class SpellsBook:
    def __init__(self) -> None:
        self.__damages_spells: list[DamageSpell] = []
        self.__guardians_spells: list[GuardianSpell] = []
        self.__health_spells: list[HealthSpell] = []
        self.__infect_spells: list[InfectSpell] = []
    
    
    @property
    def damages_spells(self) -> list[DamageSpell]:
        return self.__damages_spells.copy()
    @property
    def guardians_spells(self) -> list[GuardianSpell]:
        return self.__guardians_spells.copy()
    @property
    def health_spells(self) -> list[HealthSpell]:
        return self.__health_spells.copy()
    @property
    def infect_spells(self) -> list[InfectSpell]:
        return self.__infect_spells.copy()
    
    @property
    def spells(self) -> list[Spell]:
        return self.__damages_spells + self.__guardians_spells + self.__health_spells + self.__infect_spells
    
    def learn(self, spell: Spell):
        if (spell is not None):
            match spell.spell_type:
                case SpellType.DAMAGE:
                    if (spell.spell_type == SpellType.DAMAGE):
                        if (spell not in self.__damages_spells):
                            self.__damages_spells.append(spell)
                case SpellType.DAMAGE_OVER_TIME:
                    if (spell.spell_type == SpellType.DAMAGE_OVER_TIME):
                        if (spell not in self.__infect_spells):
                            self.__infect_spells.append(spell)
                case SpellType.HEALTH:
                    if (spell.spell_type == SpellType.HEALTH):
                        if (spell not in self.__health_spells):
                            self.__health_spells.append(spell)
                case SpellType.HEALTH_OVER_TIME:
                    if (spell.spell_type == SpellType.HEALTH_OVER_TIME):
                        if (spell not in self.__guardians_spells):
                            self.__guardians_spells.append(spell)
    
    def unlearn(self, spell: Spell):
        if (spell is not None):
            match spell.spell_type:
                case SpellType.DAMAGE:
                    if (spell in self.__damages_spells):
                        self.__damages_spells.remove(spell)
                case SpellType.DAMAGE_OVER_TIME:
                    if (spell in self.__infect_spells):
                        self.__infect_spells.remove(spell)
                case SpellType.HEALTH:
                    if (spell in self.__health_spells):
                        self.__health_spells.remove(spell)
                case SpellType.HEALTH_OVER_TIME:
                    if (spell in self.__guardians_spells):
                        self.__guardians_spells.remove(spell)