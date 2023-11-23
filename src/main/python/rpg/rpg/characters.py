from math import sqrt

import pygame

import rpg.constants
from rpg.gameplay.breeds import Breed
from rpg.gameplay.classes import Class
from rpg.gameapi import Draw, InputEventHandler
from rpg.math.geometry import Geometry, Position
from rpg.geolocation import Moveable, WindRose
from rpg.gamedesign.progression_system import Level
from rpg.gameplay.genders import Gender
from rpg.gameplay.storages import Storage

pygame.init()

class Threat:
    def __init__(self, level: int = 0) -> None:
        self.__level: int = level

    @property
    def level(self) -> int:
        return self.__level
    
    def increase(self, points: int):
        if (points is not None and points >= 0):
            self.__level += points

    def decrease(self, points: int):
        if (points is not None and points >= 0):
            self.__level -= points
        if (self.__level < 0):
            self.__level = 0
            
    def is_felling_threating(self) -> bool:
        return self.__level > 0

class Projectil:
    def __init__(self, is_damage: bool, value: float, move_speed: float, from_position: Position, to_position: Position, radius: float) -> None:
        self.from_position: Position = from_position
        self.to_position: Position = to_position
        self.__move_speed: float = move_speed
        self.__is_damage: bool = is_damage
        self.radius: float = radius
        self._texture = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
    @property
    def is_damage(self) -> bool:
        return self.__is_damage
    
    @property
    def move_speed(self) -> float:
        return self.__move_speed
    
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


class Character(Moveable):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender) -> None:
        self.__is_moving: bool = False
        self.__move_speed: int = 2.5
        self.__is_going_to_the_left: bool = False
        self.__is_going_to_the_bottom: bool = False
        self.__is_going_to_the_right: bool = False
        self.__is_going_to_the_top: bool = False
        self.__radius: float = 10.0
        self.__gender: Gender = gender
        self.__level: Level = Level(1, 100)
        self.__can_be_moved: bool = True
        self.zone_center: Position = None
        self.zone_radius: float = 0.0
        self.__breed: Breed = breed
        self.__class: Class = character_class
        self.__threat: Threat = Threat()
        self.__name: str = name
        self.__position: Position = Position(0,0)
        self.__hitbox: HitBox = HitBox(self.__position, self.__radius,self.__radius)
        self.is_in_fight_mode: bool = False
        self.__trigged_projectils: list[Projectil] = []
        self.__orientation: WindRose = WindRose.EAST
        self.__position: Position = Position(0, 0)
        self.previous_position: Position = Position(0, 0)
        self.__is_selected: bool = False
        self.is_moving: bool = False
        self.__bags: list[Storage] = []

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
    def radius(self) -> float:
        return self.__radius
    @property
    def move_speed(self) -> int:
        return self.__move_speed
    @property
    def can_be_moved(self) -> bool:
        return self.__can_be_moved
    @property
    def threat(self) -> Threat:
        return self.__threat
    @property
    def hitbox(self) -> HitBox:
        return self.__hitbox
    @property
    def trigged_projectils(self) -> list[Projectil]:
        return self.__trigged_projectils
    def get_orientation(self) -> WindRose:
        return self.__orientation

    def get_position(self) -> Position:
        return self.__position
    
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
            # is_in_contact = self.__hitbox.is_touching(other.hitbox)
        # if (isinstance(other, Projectil)):
        #     if (self.get_position().x-self.radius <= other.to_position.x <= self.get_position().x+self.radius):
        #         if (self.get_position().y-self.radius <= other.to_position.y <= self.get_position().y+self.radius):
        #             is_in_contact = True
        return is_in_contact

    def is_feel_threatened(self, target) -> bool:
        is_real_threat: bool = False
        if (isinstance(target, Character)):
            distance_between_enemy_and_target = Geometry.compute_distance(target.get_position(), self.get_position())
            is_real_threat = distance_between_enemy_and_target <= self.__threat.level
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

    def attack(self):
        new_projectil: Projectil = Projectil(True, 10.0, 5.0, self.previous_position.copy(), self.get_position().copy(), 5)
        self.trigged_projectils.append(new_projectil)

class Enemy(Character):
    def __init__(self, name: str, breed: Breed, character_class: Class, gender: Gender) -> None:
        super().__init__(name, breed, character_class, gender)
    
    