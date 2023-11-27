from rpg.concurent import synchonized
from rpg.gameplay.breeds import Breed, BreedFactory
from rpg.gameplay.classes import Class, ClassFactory
from rpg.gamedesign.progression_system import Level
from rpg.gameplay.genders import Gender
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.threat_system import Threat

class Life:
    def __init__(self, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else max
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
        self.__life: Life = Life(100, 100)
    
    @property
    def life(self) -> Life:
        return self.__life

class BaseCharacter(FormOfLife):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        super().__init__()
        self.__name: str = name
        self.__gender: Gender = gender
        self.__faction: Faction = faction
        self.__level: Level = Level(1)
        self.__breed: Breed = breed
        self.__class: Class = character_class
        self.__threat: Threat = Threat()
    
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