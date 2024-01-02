from math import cos, pi, sin, sqrt
from random import uniform

import rpg.constants
from rpg.gamedesign.character_system import BaseCharacter
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.geolocation_system import Position, Tracker
from rpg.gameplay.attack_strategy import (AttackStategy, AttackStategyChooser,
                                          UnarmedAttackStategy)
from rpg.gamedesign.currency_system import Currency
from rpg.gameplay.breeds import Breed
from rpg.gameplay.classes import Class
from rpg.gameplay.genders import Gender
from rpg.gameplay.spells import Projectil
from rpg.gameplay.storages import Storage
from rpg.math.geometry import Geometry
from rpg.utils import Color

class Character(BaseCharacter):
    _MINIMUM_AGGRO_AREA_RADIUS: int = 5
    _MAXIMUM_AGGRO_AREA_RADIUS: int = 45
    _DEFAULT_AGGRO_AREA_RADIUS: int = 20
    __DEFAULT_BAG_SIZE: int = 16

    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        BaseCharacter.__init__(self, name, breed, character_class, gender, faction)

        self.__radius: float = 10.0
        self.zone_center: Position = None
        self.zone_radius: float = 0.0
        
        self._aggro_area_radius: float = Character._DEFAULT_AGGRO_AREA_RADIUS # 1/diff(level)
        
        self.__can_be_moved_by_others: bool = False
        
        self.__currency: Currency = Currency()

        self.__trigged_projectils: list[Projectil] = []
        self.__is_selected: bool = False

        self.__storages: list[Storage] = []
        for _ in range(Character.__DEFAULT_BAG_SIZE):
            self.__storages.append(None)
            
        self.__target: Character = None
        self.__attack_strategy: AttackStategy = UnarmedAttackStategy(self)

    @property
    def has_target(self) -> bool:
        return self.__target is not None
    @property
    def target(self):
        return self.__target
    @property
    def currency(self) -> Currency:
        return self.__currency
    @property
    def can_be_moved(self) -> bool:
        return self.__can_be_moved_by_others
    @property
    def storages(self) -> list[Storage]:
        return self.__storages.copy()
    @property
    def radius(self) -> float:
        return self.__radius
    @property
    def trigged_projectils(self) -> list[Projectil]:
        return self.__trigged_projectils
    @property
    def aggro_area_radius(self) -> float:
        return self._aggro_area_radius

    def set_target(self, target):
        self.__target = target
    def set_attack_strategy(self, strategy: AttackStategy):
        if (strategy is None):
            raise ValueError()
        self.__attack_strategy = strategy
    def follow(self, target: Tracker):
        if (target is not None):
            direction_x = target.current_position.x - self.current_position.x
            direction_y = target.current_position.y - self.current_position.y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement du personnage
            new_x: int = self.current_position.x + direction_x * self.move_speed
            new_y: int = self.current_position.y + direction_y * self.move_speed
            new_position: Position = Position((new_x), (new_y))
            self.set_current_position(new_position)
    def is_touching(self, other: Tracker) -> bool:
        is_in_contact: bool = False
        if (isinstance(other, Character)):
            distance: float = Geometry.compute_distance(
                self.current_position, other.current_position)
            min_distance: float = (self.radius * 2)
            if (distance < min_distance):
                is_in_contact = True
        elif (isinstance(other, Projectil)):
            if (self.current_position.x-self.radius <= other.to_position.x <= self.current_position.x+self.radius):
                if (self.current_position.y-self.radius <= other.to_position.y <= self.current_position.y+self.radius):
                    is_in_contact = True
        return is_in_contact
    def is_feel_threatened(self, target: Tracker) -> bool:
        is_real_threat: bool = False
        if (target is not None):
            distance_between_enemy_and_target = Geometry.compute_distance(target.current_position, self.current_position)
            if (distance_between_enemy_and_target >= 0):
                is_real_threat = distance_between_enemy_and_target <= (self.radius + self.aggro_area_radius)
        return is_real_threat
    def avoid_collision_with_other(self, other: Tracker):
        if (other is not None):
            distance = Geometry.compute_distance(
                self.current_position, other.current_position)
            # Valeur minimale pour éviter la superposition
            min_distance = self.__radius * 2
            # Si un personnage est trop proche de nico, déplacer nico dans la direction opposée
            direction_x = self.current_position.x - other.current_position.x
            direction_y = self.current_position.y - other.current_position.y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement de nico
            if (self.can_be_moved):
                new_x: int = self.current_position.x + direction_x * (min_distance - distance)
                new_y: int = self.current_position.y + direction_y* (min_distance - distance)
                new_position: Position = Position((new_x), (new_y))
                self.set_current_position(new_position)
            else:
                new_x: int = other.current_position.x - direction_x * (min_distance - distance)
                new_y: int = other.current_position.y - direction_y* (min_distance - distance)
                new_position: Position = Position((new_x), (new_y))
                other.set_current_position(new_position)

    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    def attack(self, target=None) -> int:
        generated_threat: int = 1
        if (target is not None):
            damage: int = self.__attack_strategy.execute(target)
            # TODO Event listener call
        else:
            new_projectil: Projectil = Projectil(True, 10, False, 10.0, self.last_previous_position.copy(), self.current_position.copy(), 5, self.character_class.class_type.value.color)
            self.trigged_projectils.append(new_projectil)
            if (target is not None and isinstance(target, Character)):
                new_projectil.to_position = target.current_position.copy()
        return generated_threat

class Enemy(Character):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        super().__init__(name, breed, character_class, gender, faction)
        self.patrol_angle: float = 0.0
        self.__patrol_destination: Position = None
        self.__is_patrolling: bool = False
    
    def set_default_position(self, position: Position):
        super().set_default_position(position)
        self.set_current_position(position)
        self.zone_center = self.default_position.copy()
    
    @property
    def patrol_destination(self) -> Position:
        return self.__patrol_destination
    @property
    def is_patrolling(self) -> bool:
        return self.__is_patrolling
    
    def generate_patrol_path(self):
        self.patrol_angle = uniform(0, 2 * pi)
        distance = uniform(0, self.zone_radius)

        new_x = self.zone_center.x + distance * cos(self.patrol_angle)
        new_y = self.zone_center.y + distance * sin(self.patrol_angle)

        self.__patrol_destination = Position(new_x, new_y)
    
    def patrol(self):
        self.__is_patrolling = True
    
    def stop_patrolling(self):
        self.__is_patrolling = False
        
    def is_arrived_to_patrol_destination(self) -> bool:
        return Position.are_equivalent(self.current_position, self.__patrol_destination, 1)
    
    def is_arrived_to_default_position(self) -> bool:
        return Position.are_equivalent(self.current_position, self.default_position, 1)
    