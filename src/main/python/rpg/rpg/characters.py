from math import sqrt, pi, cos, sin
from random import uniform

import pygame

import rpg.constants
from rpg.gameplay.breeds import Breed
from rpg.gameplay.classes import Class
from rpg.gameplay.genders import Gender
from rpg.gamedesign.faction_system import Faction
from rpg.math.geometry import Geometry, Position
from rpg.geolocation import Moveable, WindRose
from rpg.gameplay.storages import Storage
from rpg.gameplay.attack_strategy import AttackStategyChooser, AttackStategy, UnarmedAttackStategy
from rpg.gamedesign.character_system import BaseCharacter
from rpg.gameplay.spells import Projectil
from rpg.utils import Color

pygame.init()

class HitBox:
    def __init__(self, top_left: Position, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.size: tuple[int, int] = [self.width, self.height]
        self.top: int = top_left.y
        self.left: int = top_left.x
        self.bottom: int = top_left.y + self.height
        self.right: int = top_left.x + self.width
        self.topleft: Position = top_left
        self.bottomleft: Position = Position(self.left, self.bottom)
        self.topright: Position = Position(self.right, self.top)
        self.bottomright: Position = Position(self.right, self.bottom)
        self.centerx: int = int(self.left + (self.width/2))
        self.centery: int = int(self.top + (self.height/2))
        self.midtop: Position = Position(self.centerx, self.top)
        self.midleft: Position = Position(self.left, self.centery)
        self.midbottom: Position = Position(self.centerx, self.bottom)
        self.midright: Position = Position(self.right, self.centery)
        self.center: Position = Position(self.centerx, self.centery)
        self.x: int = self.left
        self.y: int = self.top

    def is_touching(self, other) -> bool:
        if (not isinstance(other, HitBox)):
            raise ValueError()
        is_in_contact: bool = False
        distance: float = Geometry.compute_distance(self.center, other.center)
        min_distance: float = (self.width * 2)
        if (distance < min_distance):
            is_in_contact = True
        return is_in_contact


class Character(BaseCharacter):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        BaseCharacter.__init__(self, name, breed, character_class, gender, faction)

        self.__radius: float = 10.0
        self.zone_center: Position = None
        self.zone_radius: float = 0.0
        self._aggro_area_radius: float = 0.0

        # self.__hitbox: HitBox = HitBox(self.__position, self.__radius,self.__radius)
        self.__trigged_projectils: list[Projectil] = []
        self.__is_selected: bool = False
        self.__storages: list[Storage] = []
        self.target: Character = None
        self.__attack_strategy: AttackStategy = UnarmedAttackStategy(self)
        for _ in range(4):
            self.__storages.append(None)
    
    @property
    def storages(self) -> list[Storage]:
        return self.__storages.copy()
    @property
    def radius(self) -> float:
        return self.__radius
    # @property
    # def hitbox(self) -> HitBox:
    #     return self.__hitbox
    @property
    def trigged_projectils(self) -> list[Projectil]:
        return self.__trigged_projectils
    
    @property
    def aggro_area_radius(self) -> float:
        return self._aggro_area_radius
    
    def set_attack_strategy(self, strategy: AttackStategy):
        if (strategy is None):
            raise ValueError()
        self.__attack_strategy = strategy
    
    def follow(self, target):
        if (isinstance(target, Character)):
            direction_x = target.get_position().x - self.get_position().x
            direction_y = target.get_position().y - self.get_position().y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement du personnage
            # self.previous_position = Position(self.get_position().x, self.get_position().y)
            before: Position = self.get_position().copy()
            self.get_position().x += direction_x * self.move_speed
            self.get_position().y += direction_y * self.move_speed
            after: Position = self.get_position().copy()
            if (before != after):
                self.__orientation = WindRose.detect_direction(before, after)

    def is_touching(self, other) -> bool:
        is_in_contact: bool = False
        if (isinstance(other, Character)):
            distance: float = Geometry.compute_distance(
                self.get_position(), other.get_position())
            min_distance: float = (self.radius * 2)
            if (distance < min_distance):
                is_in_contact = True
        elif (isinstance(other, Projectil)):
            if (self.get_position().x-self.radius <= other.to_position.x <= self.get_position().x+self.radius):
                if (self.get_position().y-self.radius <= other.to_position.y <= self.get_position().y+self.radius):
                    is_in_contact = True
        return is_in_contact

    def is_feel_threatened(self, target) -> bool:
        is_real_threat: bool = False
        if (isinstance(target, Character)):
            distance_between_enemy_and_target = Geometry.compute_distance(target.get_position(), self.get_position())
            if (distance_between_enemy_and_target >= 0):
                is_real_threat = distance_between_enemy_and_target <= self.aggro_area_radius
            
        return is_real_threat

    def avoid_collision_with_other(self, other):
        if (isinstance(other, Character)):
            distance = Geometry.compute_distance(
                self.get_position(), other.get_position())
            # Valeur minimale pour éviter la superposition
            min_distance = self.__radius * 2
            # Si un personnage est trop proche de nico, déplacer nico dans la direction opposée
            direction_x = self.get_position().x - other.get_position().x
            direction_y = self.get_position().y - other.get_position().y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement de nico
            if (other.can_be_moved):
                # other.previous_position = other.get_position().copy()
                other.get_position().x -= direction_x * \
                    (min_distance - distance)
                other.get_position().y -= direction_y * \
                    (min_distance - distance)
            else:
                # self.previous_position = self.get_position().copy()
                self.get_position().x += direction_x * \
                    (min_distance - distance)
                self.get_position().y += direction_y * \
                    (min_distance - distance)

    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    def attack(self, target=None) -> int:
        generated_threat: int = 1
        if (target is not None and isinstance(target, Character)):
            self.__attack_strategy.execute(target)
        else:
            new_projectil: Projectil = Projectil(True, 10, False, 10.0, self.previous_position.copy(), self.get_position().copy(), 5, self.character_class.class_type.value.color)
            self.trigged_projectils.append(new_projectil)
            if (target is not None and isinstance(target, Character)):
                new_projectil.to_position = target.get_position().copy()
        return generated_threat

class Enemy(Character):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> None:
        super().__init__(name, breed, character_class, gender, faction)
        self.__default_position: Position = self.get_position()
        self.patrol_angle: float = 0.0
        self.__patrol_destination: Position = None
        self.__is_patrolling: bool = False
        self._aggro_area_radius = 50
    
    def set_default_position(self, position: Position):
        self.__default_position = position.copy()
        self.get_position().x = position.x
        self.get_position().y = position.y
        self.get_position().z = position.z
        self.zone_center = self.__default_position.copy()
    
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

        # # Se déplacer progressivement vers la nouvelle position
        # direction_x = new_x - self.get_position().x
        # direction_y = new_y - self.get_position().y
        # direction_length = sqrt(direction_x ** 2 + direction_y ** 2)

        # # Normaliser la direction
        # if direction_length != 0:
        #     direction_x /= direction_length
        #     direction_y /= direction_length
        self.__patrol_destination = Position(new_x, new_y)
    
    def patrol(self):
        self.__is_patrolling = True
    
    def stop_patrolling(self):
        self.__is_patrolling = False
        
    def is_arrived_to_patrol_destination(self) -> bool:
        return Position.are_equivalent(self.get_position(), self.__patrol_destination, 1)
    
    def is_arrived_to_default_position(self) -> bool:
        return Position.are_equivalent(self.get_position(), self.__default_position, 1)
    
    @property
    def default_position(self) -> Position:
        return self.__default_position.copy()