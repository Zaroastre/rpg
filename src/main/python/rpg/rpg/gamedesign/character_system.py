from math import sqrt
from threading import Thread
from time import sleep

from rpg.concurent import synchonized
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.geolocation_system import Position, Tracker
from rpg.gamedesign.progression_system import Level
from rpg.gamedesign.threat_system import Threat
from rpg.gameplay.attributes import Attribute
from rpg.gameplay.breeds import Breed, BreedFactory
from rpg.gameplay.classes import Class, ClassFactory
from rpg.gameplay.genders import Gender


class Life:
    def __init__(self, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else maximum
        self.__boost: list[Life] = []
        
        self.__on_life_lost_callbacks: list[callable] = []
        self.__on_life_gained_callbacks: list[callable] = []
        self.__on_die_callbacks: list[callable] = []
        self.__on_resurrect_callbacks: list[callable] = []
        self.__on_boost_win: callable = None
        self.__on_boost_lost: callable = None
        self.__on_maximum_changed: callable = None
    
    def add_on_life_lost_event_listener(self, callback: callable):
        if (callback is not None):
            self.__on_life_lost_callbacks.append(callback)
    def add_on_life_gained_event_listener(self, callback: callable):
        if (callback is not None):
            self.__on_life_gained_callbacks.append(callback)
    def add_on_die_event_listener(self, callback: callable):
        if (callback is not None):
            self.__on_die_callbacks.append(callback)
    def add_on_resurrect_event_listener(self, callback: callable):
        if (callback is not None):
            self.__on_resurrect_callbacks.append(callback)
    def set_on_boost_win_event_listener(self, callback: callable):
        self.__on_boost_win = callback
    def set_on_boost_lost_event_listener(self, callback: callable):
        self.__on_boost_lost = callback
    def set_on_maximum_changed_event_listener(self, callback: callable):
        self.__on_maximum_changed = callback
    
    def set_maximum(self, points: int):
        old_maximum: int = self.__maximum
        self.__maximum = points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum
        if (self.__on_maximum_changed is not None):
            self.__on_maximum_changed(old_maximum, self.__maximum)
    
    @property
    def maximum(self) -> int:
        maximum_boosts: int = 0
        if (len(self.__boost) > 0):
            maximum_boosts = sum([boost.maximum for boost in self.__boost], 0)
        return self.__maximum + maximum_boosts
    
    @property
    def current(self) -> int:
        current_boosts: int = 0
        if (len(self.__boost) > 0):
            current_boosts = sum([boost.current for boost in self.__boost], 0)
        return self.__current + current_boosts
    
    @synchonized
    def loose(self, points: int):
        self.__current -= points
        for callback in self.__on_life_lost_callbacks:
            callback(points)
        if (self.__current <= 0):
            self.die()

    def die(self):
        self.__current = 0
        for callback in self.__on_die_callbacks:
            callback()

    def is_dead(self) -> bool:
        return self.__current <= 0
    
    @synchonized
    def heal(self, points: int):
        if ((points is None) or (points < 0)):
            raise ValueError()    
        self.__current += points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum
            for callback in self.__on_life_gained_callbacks:
                callback(points)

    def is_alive(self) -> bool:
        return not self.is_dead()
    
    def resurect(self):
        self.heal(self.__maximum)
        for callback in self.__on_resurrect_callbacks:
            callback()
    
    def win_boost(self, boost_life):
        if ((boost_life is not None) and (isinstance(boost_life, Life))):
            self.__boost.append(boost_life)
            if (self.__on_boost_win is not None):
                self.__on_boost_win(boost_life)
    
    def loose_boost(self, boost_life):
        if ((boost_life is not None) and (isinstance(boost_life, Life)) and (boost_life in self.__boost)):
            self.__boost.remove(boost_life)
            if (self.__on_boost_lost is not None):
                self.__on_boost_lost(boost_life)
        if (self.__current > self.__maximum):
            self.__current = self.__maximum

class FormOfLife:
    def __init__(self) -> None:
        self.__life: Life = Life(100, 100)

    @property
    def life(self) -> Life:
        return self.__life

class BaseCharacter(FormOfLife, Tracker):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        FormOfLife.__init__(self)
        Tracker.__init__(self, default_position=Position(0,0))
        self.__name: str = name
        self.__gender: Gender = gender
        self.__faction: Faction = faction
        self.__level: Level = Level(1)
        self.__breed: Breed = breed
        self.__class: Class = character_class
        self.__threat: Threat = Threat()
        maximum_life: int = self.__breed.get_attribute(Attribute.STAMANIA) + self.__class.get_attribute(Attribute.STAMANIA)
        self.life.set_maximum(maximum_life*10)
        self.__attack_speed: float = 2.6
        self.is_in_fight_mode: bool = False
        
        self.__move_speed: float = 2.5
        
        self.__level.set_on_level_up_event_listener(self.__on_level_up_handler)
        self.__health_regeneration: HealthRegenerationThread = HealthRegenerationThread(self)
        self.__power_regeneration: PowerRegenerationThread = PowerRegenerationThread(self)
        self.__health_regeneration.start()
        # self.__power_regeneration.start()
        
        self.__on_die_handler: callable = None
        
    def set_on_die_event_listener(self, callback: callable):
        self.__on_die_handler = callback
        self.life.add_on_die_event_listener(self.__on_die_event_listener)

    def __on_die_event_listener(self):
        self.__on_die_handler(self)
        
    def __on_level_up_handler(self):
        maximum_life: int = self.__breed.get_attribute(Attribute.STAMANIA) + self.__class.get_attribute(Attribute.STAMANIA)
        self._life = Life((maximum_life*10)*self.level.value)

    def get_attribute(self, attribute: Attribute) -> int:
        value: int = 0
        value += self.__breed.get_attribute(attribute)
        value += self.__class.get_attribute(attribute)
        return value
    
    @property
    def attack_speed(self) -> float:
        return self.__attack_speed
    @property
    def gender(self) -> Gender:
        return self.__gender
    @property
    def faction(self) -> Faction:
        return self.__faction
    @property
    def name(self) -> str:
        return self.__name
    @property
    def breed(self) -> Breed:
        return self.__breed
    @property
    def character_class(self) -> Class:
        return self.__class
    @property
    def level(self) -> Level:
        return self.__level
    @property
    def threat(self) -> Threat:
        return self.__threat
    
    @property
    def move_speed(self) -> int:
        return self.__move_speed
    
    def copy(self):
        name: str = self.__name
        gender: Gender = [value for value in list(Gender) if value == self.__gender][0]
        faction: Faction = [value for value in list(Faction) if value == self.__faction][0]
        breed: Breed = BreedFactory.create(self.__breed.breed_type)
        character_class: Class = ClassFactory.create(self.__class.class_type)
        the_copy: BaseCharacter = BaseCharacter(name, breed, character_class, gender, faction)
        the_copy.threat.increase(self.__threat.level)
        while (the_copy.level.value < self.__level.value):
            the_copy.level.up()
        the_copy.level.gain(self.__level.experience.current)
        return the_copy

class HealthRegenerationThread(Thread):
    def __init__(self, character: BaseCharacter) -> None:
        super().__init__()
        self.__character: BaseCharacter = character
        self.__must_regenerate: bool = False
    
    def run(self) -> None:
        self.__must_regenerate = True
        while (self.__must_regenerate):
            if (self.__character.life.is_alive()):
                if (self.__character.life.current < self.__character.life.maximum):
                    if (not self.__character.is_in_fight_mode):
                        points: int = int((5 * self.__character.life.maximum)/100)
                        self.__character.life.heal(points)
            sleep(2)

class PowerRegenerationThread(Thread):
    def __init__(self, character: BaseCharacter) -> None:
        super().__init__()
        self.__character: BaseCharacter = character
        self.__must_regenerate: bool = False
    
    def run(self) -> None:
        self.__must_regenerate = True
        while (self.__must_regenerate):
            if (self.__character.life.is_alive()):
                if (self.__character.character_class.resource.current < self.__character.character_class.resource.maximum):
                    if (not self.__character.is_in_fight_mode):
                        points: int = self.__character.get_attribute(Attribute.SPIRIT)
                        self.__character.character_class.resource.gain(points)
                        sleep(2)
                    else:
                        points: int = int((5 * self.__character.character_class.resource.maximum)/100)
                        self.__character.character_class.resource.gain(points)
                        sleep(5)
                else:
                    sleep(1)
            else:
                sleep(1)
