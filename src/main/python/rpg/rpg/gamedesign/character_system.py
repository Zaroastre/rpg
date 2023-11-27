from threading import Thread
from time import sleep

from rpg.concurent import synchonized
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.progression_system import Level
from rpg.gamedesign.threat_system import Threat
from rpg.gameplay.attributes import Attribute
from rpg.gameplay.breeds import Breed, BreedFactory
from rpg.gameplay.classes import Class, ClassFactory
from rpg.gameplay.genders import Gender
from rpg.geolocation import Moveable, WindRose
from rpg.math.geometry import Position


class Life:
    def __init__(self, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else maximum
        self.__boost: list[int] = []
        
    @property
    def maximum(self) -> int:
        return self.__maximum

    @property
    def current(self) -> int:
        return self.__current
    
    @synchonized
    def loose(self, points: int):
        self.__current -= points
        if (self.__current <= 0):
            self.die()

    def die(self):
        self.__current = 0

    def is_dead(self) -> bool:
        return self.__current <= 0
    
    @synchonized
    def heal(self, points: int):
        self.__current += points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum
    
    def is_alive(self) -> bool:
        return not self.is_dead()
    
    def win_boost(self, boost_points: int):
        self.__maximum += boost_points
        self.__current += boost_points
    
    def loose_boost(self, boost_points: int):
        self.__maximum -= boost_points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum

class FormOfLife:
    def __init__(self) -> None:
        self._life: Life = Life(100, 100)
    
    @property
    def life(self) -> Life:
        return self._life

class BaseCharacter(FormOfLife, Moveable):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        FormOfLife.__init__(self)
        self.__name: str = name
        self.__gender: Gender = gender
        self.__faction: Faction = faction
        self.__level: Level = Level(1)
        self.__breed: Breed = breed
        self.__class: Class = character_class
        self.__threat: Threat = Threat()
        maximum_life: int = self.__breed.get_attribute(Attribute.STAMANIA) + self.__class.get_attribute(Attribute.STAMANIA)
        self._life = Life(maximum_life*10)
        self.__attack_speed: float = 2.6
        self.is_in_fight_mode: bool = False
        self.__move_speed: int = 2.5
        self.__can_be_moved: bool = True
        self.__position: Position = Position(0,0)
        self.__orientation: WindRose = WindRose.EAST
        self.previous_position: Position = Position(0, 0)
        self.is_moving: bool = False
        self.__level.set_on_level_up_event_listener(self.__on_level_up_handler)
        self.__health_regeneration: HealthRegenerationThread = HealthRegenerationThread(self)
        self.__power_regeneration: PowerRegenerationThread = PowerRegenerationThread(self)
        self.__health_regeneration.start()
        # self.__power_regeneration.start()
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
    @property
    def can_be_moved(self) -> bool:
        return self.__can_be_moved
    def get_orientation(self) -> WindRose:
        return self.__orientation

    def get_position(self) -> Position:
        return self.__position
    
    def set_position(self, new_position: Position):
        self.__position = new_position
    
    def move(self, speed: float, orientation: WindRose):
        if (self.__orientation is not orientation):
            self.__orientation = orientation
        # Impl not finished
    
    def move_foreward(self, speed: float):
        pass
    
    def move_backward(self, speed: float):
        pass
    
    def turn_around(self):
        self.__orientation = WindRose.opposite(self.__orientation)
    
    def turn_left(self):
        self.__orientation = WindRose.compute_following_direction_counterclockwise(self.__orientation)
    
    def turn_right(self):
        self.__orientation = WindRose.compute_following_direction_clockwise(self.__orientation)
    
    
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
        print("..s")
    
    def run(self) -> None:
        self.__must_regenerate = True
        while (self.__must_regenerate):
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
            if (self.__character.character_class.resource.current < self.__character.character_class.resource.maximum):
                if (not self.__character.is_in_fight_mode):
                    points: int = self.__character.get_attribute(Attribute.SPIRIT)
                    self.__character.character_class.resource.gain(points)   
                    sleep(2)
                else:
                    points: int = int((5 * self.__character.character_class.resource.maximum)/100)
                    self.__character.character_class.resource.gain(points)
                    sleep(5)
