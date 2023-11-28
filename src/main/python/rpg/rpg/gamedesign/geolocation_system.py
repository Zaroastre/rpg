from enum import Enum
from math import atan2, degrees, sqrt

class Position:
    """Class that represents a position in a geomatric space.
    """

    def __init__(self, x: float, y: float, z: float = 0.0) -> None:
        """Default constructor.

        Args:
            x (float): X
            y (float): Y
            z (float, optional): Z. Defaults to 0.0.
        """
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def copy(self):
        return Position(self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, __o: object) -> bool:
        are_equal: bool = False
        if (isinstance(__o, Position)):
            are_equal = (__o.x == self.x) and (__o.y == self.y) and (__o.z == self.z)
        return are_equal

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    @staticmethod
    def are_equivalent(first, second, error_threshold: int=0) -> bool:
        if (first is None or not isinstance(first, Position)):
            raise ValueError()
        if (second is None or not isinstance(second, Position)):
            raise ValueError()
        result: bool = False
        if (second.x-error_threshold <= first.x and first.x <= second.x+error_threshold):
            if (second.y-error_threshold <= first.y and first.y <= second.y+error_threshold):
                result = True
        return result

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

class Tracker:
    def __init__(self, default_position: Position, maximum_history_size: int = 5) -> None:
        self.__default_position: Position = default_position
        self.__previous_positions: list[Position] = []
        self.__previous_positions.append(default_position.copy())
        self.__current_position: Position = default_position.copy()
        self.__current_position.x += 1
        self.__destination_position: Position = None
        self.__must_walk: bool = True
        self.__must_run: bool = False
        self.__orientation: WindRose = WindRose.detect_direction(self.last_previous_position, self.__current_position)
        self.__maximum_history_size: int = maximum_history_size

    @property
    def orientation(self) -> WindRose:
        return self.__orientation
    @property
    def is_running(self) -> bool:
        return self.__must_run
    @property
    def is_walking(self) -> bool:
        return self.__must_walk
    @property
    def is_staying_on_place(self) -> bool:
        return (not self.is_walking) and (not self.is_running)
    @property
    def default_position(self) -> Position:
        return self.__default_position.copy()
    @property
    def current_position(self) -> Position:
        return self.__current_position.copy()
    @property
    def destination_position(self) -> Position:
        return self.__destination_position.copy()
    @property
    def last_previous_position(self) -> Position:
        return self.__previous_positions[-1].copy()

    def get_previous_positions(self) -> list[Position]:
        positions: list[Position] = []
        for previous_position in self.__previous_positions:
            positions.append(previous_position.copy())
        return positions
    def is_moving(self) -> bool:
        return (self.last_previous_position != self.current_position) and (not self.is_staying_on_place)
    def set_running_mode(self):
        self.__must_walk = False
        self.__must_run = True
    def set_walking_mode(self):
        self.__must_run = False
        self.__must_walk = True
    def set_stay_in_place_mode(self):
        self.__must_run = False
        self.__must_walk = False
    def set_current_position(self, position: Position):
        if (len(self.__previous_positions) >= self.__maximum_history_size):
            self.__previous_positions.pop(0)
        self.__previous_positions.append(self.__current_position.copy())
        self.__current_position = position.copy()
    def set_default_position(self, position: Position):
        self.__default_position = position.copy()
    def move(self, to_top: bool, to_bottom: bool, to_left: bool, to_right: bool, speed: float):
        # if (self.last_previous_position != self.current_position):
        #     self.last_previous_position = self.current_position
        is_moving_in_diagonal = (to_left or to_right) and (to_top or to_bottom)
        new_position: Position = None
        if (is_moving_in_diagonal):
            if to_left and (to_top or to_bottom):
                # self.character.current_position.x -= speed / sqrt(2)
                new_position = Position((self.current_position.x - speed / sqrt(2)), self.current_position.y)
            if to_right and (to_top or to_bottom):
                # self.character.current_position.x += speed / sqrt(2)
                new_position = Position((self.current_position.x + speed / sqrt(2)), self.current_position.y)
            if to_top and (to_left or to_right):
                # self.character.current_position.y -= speed / sqrt(2)
                new_position = Position(self.current_position.x, (self.current_position.y - speed / sqrt(2)))
            if to_bottom and (to_left or to_right):
                # self.character.current_position.y += speed / sqrt(2)
                new_position = Position(self.current_position.x, (self.current_position.y + speed / sqrt(2)))
        else:
            if to_left:
                # self.character.current_position.x -= speed
                new_position = Position((self.current_position.x - speed), self.current_position.y)
            if to_right:
                # self.character.current_position.x += speed
                new_position = Position((self.current_position.x + speed), self.current_position.y)
            if to_top:
                # self.character.current_position.y -= speed
                new_position = Position(self.current_position.x, (self.current_position.y - speed))
            if to_bottom:
                # self.character.current_position.y += speed
                new_position = Position(self.current_position.x, (self.current_position.y + speed))
        if (new_position is not None):
            self.set_current_position(new_position)
