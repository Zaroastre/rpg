from abc import ABC, abstractmethod
from enum import Enum
from math import atan2, degrees

from rpg.math.geometry import Position

class WindRoseTypeValue:
    def __init__(self, name: str, value: int) -> None:
        self.__name: str = name
        self.__value: int = value
    @property
    def name(self) -> str:
        return self.__name
    @property
    def value(self) -> int:
        return self.__value

class WindRose(Enum):
    NORTH: WindRoseTypeValue = WindRoseTypeValue("NORTH", 1)
    NORTH_EAST: WindRoseTypeValue = WindRoseTypeValue("NORTH_EAST", 2)
    EAST: WindRoseTypeValue = WindRoseTypeValue("EAST", 3)
    SOUTH_EAST: WindRoseTypeValue = WindRoseTypeValue("SOUTH_EAST", 4)
    SOUTH: WindRoseTypeValue = WindRoseTypeValue("SOUTH", 5)
    SOUTH_WEST: WindRoseTypeValue = WindRoseTypeValue("SOUTH_WEST", 6)
    WEST: WindRoseTypeValue = WindRoseTypeValue("WEST", 7)
    NORTH_WEST: WindRoseTypeValue = WindRoseTypeValue("NORTH_WEST", 8)

    @staticmethod
    def opposite(orientation):
        if (not isinstance(orientation, WindRose)):
            raise ValueError()
        new_orientation: WindRose
        match orientation:
            case WindRose.NORTH:
                new_orientation = WindRose.SOUTH
            case WindRose.NORTH_EAST:
                new_orientation = WindRose.SOUTH_WEST
            case WindRose.EAST:
                new_orientation = WindRose.WEST
            case WindRose.SOUTH_EAST:
                new_orientation = WindRose.NORTH_WEST
            case WindRose.SOUTH:
                new_orientation = WindRose.NORTH
            case WindRose.SOUTH_WEST:
                new_orientation = WindRose.NORTH_EAST
            case WindRose.WEST:
                new_orientation = WindRose.EAST
            case WindRose.NORTH_WEST:
                new_orientation = WindRose.SOUTH_EAST
        return new_orientation

    @staticmethod
    def compute_following_direction_clockwise(current_direction):
        if not isinstance(current_direction, WindRose):
            raise ValueError("Invalid direction")
        directions: dict[WindRose,WindRose] = {
            WindRose.NORTH: WindRose.NORTH_EAST,
            WindRose.NORTH_EAST: WindRose.EAST,
            WindRose.EAST: WindRose.SOUTH_EAST,
            WindRose.SOUTH_EAST: WindRose.SOUTH,
            WindRose.SOUTH: WindRose.SOUTH_WEST,
            WindRose.SOUTH_WEST: WindRose.WEST,
            WindRose.WEST: WindRose.NORTH_WEST,
            WindRose.NORTH_WEST: WindRose.NORTH
        }
        return directions[current_direction]
    
    @staticmethod
    def compute_following_direction_counterclockwise(current_direction):
        if not isinstance(current_direction, WindRose):
            raise ValueError("Invalid direction")
        directions: dict[WindRose,WindRose] = {
            WindRose.NORTH: WindRose.NORTH_WEST,
            WindRose.NORTH_EAST: WindRose.NORTH,
            WindRose.EAST: WindRose.NORTH_EAST,
            WindRose.SOUTH_EAST: WindRose.EAST,
            WindRose.SOUTH: WindRose.SOUTH_EAST,
            WindRose.SOUTH_WEST: WindRose.SOUTH,
            WindRose.WEST: WindRose.SOUTH_WEST,
            WindRose.NORTH_WEST: WindRose.WEST
        }
        return directions[current_direction]

    @staticmethod
    def detect_direction(before: Position, after: Position):
        if (before is None or after is None):
            raise ValueError()
        direction: WindRose
        delta_x = after.x - before.x
        delta_y = after.y - before.y

        angle_rad = atan2(delta_y, delta_x)
        angle_deg = degrees(angle_rad)

        # Convertir l'angle en une direction WindRose
        if -22.5 <= angle_deg <= 22.5:
            direction = WindRose.EAST
        elif 22.5 < angle_deg <= 67.5:
            direction = WindRose.NORTH_EAST
        elif 67.5 < angle_deg <= 112.5:
            direction = WindRose.NORTH
        elif 112.5 < angle_deg <= 157.5:
            direction = WindRose.NORTH_WEST
        elif 157.5 < angle_deg <= 180 or -180 <= angle_deg < -157.5:
            direction = WindRose.WEST
        elif -157.5 < angle_deg <= -112.5:
            direction = WindRose.SOUTH_WEST
        elif -112.5 < angle_deg <= -67.5:
            direction = WindRose.SOUTH
        elif -67.5 < angle_deg <= -22.5:
            direction = WindRose.SOUTH_EAST
        else:
            raise ValueError()
        return direction

class Moveable():
    
    @abstractmethod
    def get_orientation(self) -> WindRose:
        raise NotImplementedError()
    
    @abstractmethod
    def get_position(self) -> Position:
        raise NotImplementedError()
    
    @abstractmethod
    def move(self, speed: float, orientation: WindRose):
        raise NotImplementedError()
    
    @abstractmethod
    def move_forward(self, speed: float):
        raise NotImplementedError()
    
    @abstractmethod
    def move_backward(self, speed: float):
        raise NotImplementedError()
    
    @abstractmethod
    def turn_left(self):
        raise NotImplementedError()
    
    @abstractmethod
    def turn_around(self):
        raise NotImplementedError()
    
    @abstractmethod
    def turn_right(self):
        raise NotImplementedError()