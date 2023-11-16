from abc import abstractmethod
from datetime import datetime
from math import atan2, cos, degrees, radians, sin, sqrt
from random import randint

import pygame

pygame.init()
pygame.joystick.init()


class InputEventHandler:
    """Interface that represents an events handler throw by user.
    """
    @abstractmethod
    def handle(self, event: pygame.event.Event):
        """Handle the given event.

        Args:
            event (pygame.event.Event): The user input event.
        """
        raise NotImplementedError()


class Draw:
    """Interface that represents a drawable object.
    """
    @abstractmethod
    def draw(self, master: pygame.Surface):
        """Draw something on the master surface.

        Args:
            master (pygame.Surface): The master surface that must be painted.
        """
        raise NotImplementedError()


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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Geometry:
    """Utilitary class that can be used to computes usefull algorythm for geometry computation.
    """

    @staticmethod
    def compute_slope(point1: Position, point2: Position) -> float:
        delta_y = point2.y - point1.y
        delta_x = point2.x - point1.x
        return delta_y / delta_x

    @staticmethod
    def compute_origin_point(point1: Position, point2: Position) -> Position:
        """Compute the original point from the two given points.

        Args:
            point1 (Position): First point
            point2 (Position): Second point

        Returns:
            Position: The new computed position
        """
        SLOPE: float = Geometry.compute_slope(point1, point2)
        COEFFICIENT = -1
        COEFFICIENT_OF_LINE = -SLOPE * point1.x - COEFFICIENT * point1.y
        X = COEFFICIENT_OF_LINE / SLOPE
        Y = 0
        return Position(X, Y)

    @staticmethod
    def calculate_point_from_y(point1: Position, point2: Position, y: float) -> Position:
        """Compute new point using 2 existing points and knowing the Y position.

        Args:
            point1 (Position): Firsrt point
            point2 (Position): Second point
            y (float): Y position of the new position to compute

        Returns:
            Position: The computed position
        """
        # Vérifier si les points sont sur la même ligne horizontale
        if point1.y == point2.y and point1.y != y:
            raise ValueError(
                "Les points ne forment pas une ligne horizontale à la hauteur de Y.")
        x: float = 0.0
        if point1.y == point2.y:
            x = (point1.x + point2.x) / 2
        else:
            x = point1.x + (y - point1.y) * (point2.x -
                                             point1.x) / (point2.y - point1.y)
        return Position(x, y)

    @staticmethod
    def compute_new_point_using_x(point1: Position, point2: Position, x: float) -> Position:
        """Compute new point using 2 exisitng points and knowing x position of the new position to compute.

        Args:
            point1 (Position): First point
            point2 (Position): Second point
            x (int): X of the new position

        Returns:
            Position: The new computed position
        """
        SLOPE = Geometry.compute_slope(point1, point2)
        Y = SLOPE * (x - point1.x) + point1.y
        return Position(x, Y)

    @staticmethod
    def compute_rotation_angle(point1: Position, point2: Position, point3: Position) -> float:
        angle = atan2(point2.y - point1.y, point2.x - point1.x) - \
            atan2(point3.y - point1.y, point3.x - point1.x)
        angle_degrees = degrees(angle)
        return angle_degrees

    @staticmethod
    def compute_rotation_point(point: Position, rotation_center: Position, angle: float) -> Position:
        relative_x: float = point.x - rotation_center.x
        relative_y: float = point.y - rotation_center.y
        rotated_x: float = relative_x * cos(angle) - relative_y * sin(angle)
        rotated_y: float = relative_x * sin(angle) + relative_y * cos(angle)

        return Position((rotated_x + rotation_center.x), (rotated_y + rotation_center.y))

    @staticmethod
    def compute_distance(point1: Position, point2: Position) -> float:
        return sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    @staticmethod
    def are_positions_equal(point1: Position, point2: Position) -> bool:
        print(Geometry.compute_distance(point1, point2))
        return point1.x == point2.x and point1.y == point2.y and point1.z == point2.z

class Projectil(pygame.sprite.Sprite, InputEventHandler, Draw):
    HEALTH_COLOR: pygame.Color = pygame.Color(0, 200, 0)
    DAMAGE_COLOR: pygame.Color = pygame.Color(200, 0, 0)
    def __init__(self, is_damage: bool, value: float, move_speed: float, position: Position, radius: float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.start_position: Position = position
        self.position: Position = Position(position.x, position.y)
        self.__move_speed: float = move_speed
        self.__is_damage: bool = is_damage
        self.radius: float = radius
        self._texture = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
    
    def handle(self, event: pygame.event.Event):
        print(self.position)
        print(self.start_position)
    
    def draw(self, master: pygame.Surface):
        pygame.draw.circle(master, Projectil.HEALTH_COLOR if not self.__is_damage else Projectil.DAMAGE_COLOR, (self.position.x, self.position.y), self.radius)
    
class Character(pygame.sprite.Sprite, InputEventHandler, Draw):
    MENACE_AREA_COLOR: pygame.Color = pygame.Color(255, 255, 0, a=100)
    ZONING_AREA_COLOR: pygame.Color = pygame.Color(255,200, 0)
    def __init__(self, name: str) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.is_moving: bool = False
        self.__move_speed: int = 2.5
        self.__is_going_to_the_left: bool = False
        self.__is_going_to_the_bottom: bool = False
        self.__is_going_to_the_right: bool = False
        self.__is_going_to_the_top: bool = False
        self.__can_be_moved: bool = True
        self.zone_center: Position = None
        self.zone_radius: float = 0.0
        self.menace: float = 0
        self.__name: str = name
        self._radius: float = 10.0
        self._texture = pygame.Surface([self._radius*2, self._radius*2], pygame.SRCALPHA)
        self.position: Position = Position(0,0)
        self.previous_position: Position = Position(0, 0)
        self.__is_selected: bool = False
        self._hitbox: pygame.Rect = None
        self.__font_size: int = 20
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self._title: pygame.Surface = self.__font.render(
            self.name[0], True, self.__font_color)
        self.is_in_fight_mode: bool = False
        self.trigged_projectils: list[Projectil] = []

    @property
    def move_speed(self) -> int:
        return self.__move_speed

    @property
    def can_be_moved(self) -> bool:
        return self.__can_be_moved


    def is_selected(self) -> bool:
        return self.__is_selected

    @property
    def name(self) -> str:
        return self.__name

    @property
    def hitbox(self) -> pygame.Rect:
        return self._hitbox

    @property
    def radius(self) -> float:
        return self._radius

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    def follow(self, target):
        if (isinstance(target, Character)):
            direction_x = target.position.x - self.position.x
            direction_y = target.position.y - self.position.y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement du personnage
            self.previous_position = Position(self.position.x, self.position.y)
            self.position.x += direction_x * self.move_speed
            self.position.y += direction_y * self.move_speed



    def handle(self, event: pygame.event.Event):
        if event is not None:
            if self.is_selected():
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_q)) or (event.type == pygame.JOYAXISMOTION and event.axis == 0 and event.value < 0.003906369212927641):
                    self.__is_going_to_the_left = True
                elif (event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_q)) or (event.type == pygame.JOYAXISMOTION and event.axis == 0  and event.value == 0.003906369212927641):
                    self.__is_going_to_the_left = False
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_d)) or (event.type == pygame.JOYAXISMOTION and event.axis == 0  and event.value > 0.003906369212927641):
                    self.__is_going_to_the_right = True
                elif (event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_d)) or (event.type == pygame.JOYAXISMOTION and event.axis == 0  and event.value == 0.003906369212927641):
                    self.__is_going_to_the_right = False
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_z)) or (event.type == pygame.JOYAXISMOTION and event.axis == 1  and event.value < 0.003906369212927641):
                    self.__is_going_to_the_top = True
                elif (event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == pygame.K_z)) or (event.type == pygame.JOYAXISMOTION and event.axis == 1  and event.value == 0.003906369212927641):
                    self.__is_going_to_the_top = False
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_s)) or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value > 0.003906369212927641):
                    self.__is_going_to_the_bottom = True
                elif (event.type == pygame.KEYUP and (event.key == pygame.K_DOWN or event.key == pygame.K_s)) or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value == 0.003906369212927641):
                    self.__is_going_to_the_bottom = False
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_a) or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
                    new_projectil: Projectil = Projectil(True, 10.0, 5.0, Position(self.previous_position.x, self.previous_position.y), 5)
                    new_projectil.position = Position(self.position.x, self.position.y)
                    self.trigged_projectils.append(new_projectil)
                    
        self.is_moving = self.__is_going_to_the_bottom or self.__is_going_to_the_left or self.__is_going_to_the_right or self.__is_going_to_the_top
        if self.is_selected():
            diagonal_movement = (self.__is_going_to_the_left or self.__is_going_to_the_right) and \
                                (self.__is_going_to_the_top or self.__is_going_to_the_bottom)

            if (diagonal_movement):

                if self.__is_going_to_the_left and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.x -= self.__move_speed / sqrt(2)
                if self.__is_going_to_the_right and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.x += self.__move_speed / sqrt(2)
                if self.__is_going_to_the_top and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.y -= self.__move_speed / sqrt(2)
                if self.__is_going_to_the_bottom and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.y += self.__move_speed / sqrt(2)
            else:
                if self.__is_going_to_the_left:
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.x -= self.__move_speed
                if self.__is_going_to_the_right:
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.x += self.__move_speed
                if self.__is_going_to_the_top:
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.y -= self.__move_speed
                if self.__is_going_to_the_bottom:
                    self.previous_position = Position(self.position.x, self.position.y)
                    self.position.y += self.__move_speed

        for projectil in self.trigged_projectils:
            projectil.handle(event)

    def is_touching(self, other) -> bool:
        is_in_contact: bool = False
        if (isinstance(other, Character)):
            distance: float = Geometry.compute_distance(
                self.position, other.position)
            min_distance: float = (self.radius * 2)
            if (distance < min_distance):
                is_in_contact = True
        return is_in_contact

    def is_feel_threatened(self, target) -> bool:
        is_real_threat: bool = False
        if (isinstance(target, Character)):
            distance_between_enemy_and_target = Geometry.compute_distance(target.position, self.position)
            is_real_threat = distance_between_enemy_and_target <= self.menace
        return is_real_threat

    def avoid_collision_with_other(self, other):
        if (isinstance(other, Character)):
            distance = Geometry.compute_distance(
                self.position, other.position)
            # Valeur minimale pour éviter la superposition
            min_distance = self.radius * 2
            # Si un personnage est trop proche de nico, déplacer nico dans la direction opposée
            direction_x = self.position.x - other.position.x
            direction_y = self.position.y - other.position.y
            direction_length = sqrt(direction_x**2 + direction_y**2)

            # Normalisation de la direction
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacement de nico
            if (other.can_be_moved):
                other.previous_position = Position(other.position.x, other.position.y)
                other.position.x -= direction_x * \
                    (min_distance - distance)
                other.position.y -= direction_y * \
                    (min_distance - distance)
            else:
                self.previous_position = Position(self.position.x, self.position.y)
                self.position.x += direction_x * \
                    (min_distance - distance)
                self.position.y += direction_y * \
                    (min_distance - distance)

    def draw(self, master: pygame.Surface):
        pygame.draw.circle(master, Character.MENACE_AREA_COLOR, (self.position.x,self.position.y), self.menace, 2)
        if (self.zone_center is not None):
            pygame.draw.circle(master, Character.ZONING_AREA_COLOR, (self.zone_center.x,self.zone_center.y), self.zone_radius, 1)
        self._texture.fill(pygame.Color(0,0,0,0))
        point_color: pygame.Color
        if (self.is_selected()):
            point_color = pygame.Color(50,150,50)
        else:
            point_color = pygame.Color(0,150,250)
        self._hitbox = pygame.draw.circle(
            self._texture, point_color, (self._radius, self._radius), self._radius)
        self._hitbox = master.blit(self._texture, (self.position.x-self._radius, self.position.y-self._radius))
        master.blit(self._title, (self.position.x-(self._radius/2), self.position.y-(self._radius/2)))
        for projectil in self.trigged_projectils:
            projectil.draw(master)


class Enemy(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def draw(self, master: pygame.Surface):
        # pygame.draw.circle(master, pygame.Color(150,0,0), (self.position.x,self.position.y), self.menace, 2)
        # if (self.zone_center is not None):
        #     pygame.draw.circle(master, pygame.Color(255, 0, 255), (self.zone_center.x,self.zone_center.y), self.zone_radius, 1)
        self._texture.fill(pygame.Color(0,0,0,0))
        point_color: pygame.Color
        if (self.is_selected()):
            point_color = pygame.Color(50,150,50)
        else:
            point_color = pygame.Color(255,150,0)
        self._hitbox = pygame.draw.circle(
            self._texture, point_color, (self._radius, self._radius), self._radius)
        self._hitbox = master.blit(self._texture, (self.position.x-self._radius, self.position.y-self._radius))
        # master.blit(self._title, (self.position.x+self._radius*2, self.position.y-(self._radius/2)))


class Group(InputEventHandler, Draw):
    def __init__(self, max_capacity: int) -> None:
        self.__members: list[Character] = []
        self.__max_size: int = max_capacity

    @property
    def members(self) -> list[Character]:
        return self.__members

    def add_member(self, new_member: Character):
        if (len(self.__members) < self.__max_size):
            self.__members.append(new_member)

    def is_full(self) -> bool:
        return len(self.__members) == self.__max_size

    def remove_member(self, member_to_remove: Character):
        if (member_to_remove in self.__members):
            self.__members.remove(member_to_remove)

    def __handle_character_selection_in_group(self, event: pygame.event.Event):
        selected_members: list[Character] = [member for member in self.members if member.is_selected()]
        if (len(selected_members) == 1):
            previous_selected_member = selected_members[0]
            index: int = self.__members.index(previous_selected_member)
            if (event.type == pygame.JOYBUTTONDOWN and event.button == 5):
                if (index+1 > len(self.__members)-1):
                    index = 0
                else:
                    index += 1
            if (event.type == pygame.JOYBUTTONDOWN and event.button == 4):
                if (index == 0):
                    index = len(self.__members)-1
                else:
                    index -= 1
            previous_selected_member.unselect()
            self.__members[index].select()

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            self.__handle_character_selection_in_group(event)
        for member in self.__members:
            member.handle(event)

    def draw(self, master: pygame.Surface):
        for member in self.__members:
            member.draw(master)

class MemberPanel(InputEventHandler, Draw):
    def __init__(self, member: Character) -> None:
        self.__member: Character = member
        self.position: Position = Position(0, 0)
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 22
        self.__avatar_picture_radius: float = 40
        self.__texture: pygame.Surface = pygame.Surface([250, self.__avatar_picture_radius*2], pygame.SRCALPHA)
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__title: pygame.Surface = self.__font.render(
            self.__member.name, True, self.__font_color)
        self.__current_life_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__current_resource_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__current_menace_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__life_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__resource_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__menace_bar: pygame.Surface = pygame.Surface((150, 10))

    @property
    def height(self) -> float:
        return self.__avatar_picture_radius*2

    def handle(self, event: pygame.event.Event):
        self.__current_life_bar = pygame.Surface((150, 10))
        self.__current_resource_bar = pygame.Surface((150, 10))
        self.__current_menace_bar = pygame.Surface(((self.__member.menace*150)/100, 10))

    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(30,30,30))
        pygame.draw.circle(self.__texture, pygame.Color(50,50,50), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius)
        if (self.__member.is_selected()):
            pygame.draw.circle(self.__texture, pygame.Color(100,200,0), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius, 5)
        else:
            pygame.draw.circle(self.__texture, pygame.Color(200,200,200), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius, 5)
        self.__texture.blit(self.__title, (self.__avatar_picture_radius*2, 0))

        
        self.__life_bar.fill(pygame.Color(10, 10, 10))
        self.__resource_bar.fill(pygame.Color(10, 10, 10))
        self.__menace_bar.fill(pygame.Color(10, 10, 10))
        
        self.__current_life_bar.fill(pygame.Color(50, 200, 0))
        self.__current_resource_bar.fill(pygame.Color(0, 150, 200))
        self.__current_menace_bar.fill(pygame.Color(200, 0, 0))

        self.__texture.blit(self.__life_bar, ((self.__avatar_picture_radius*2)+10, self.__font_size))
        self.__texture.blit(self.__resource_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + self.__life_bar.get_height()+10)))
        self.__texture.blit(self.__menace_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + (self.__life_bar.get_height()+10)*2)))
        
        self.__texture.blit(self.__current_life_bar, ((self.__avatar_picture_radius*2)+10, self.__font_size))
        self.__texture.blit(self.__current_resource_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + self.__life_bar.get_height()+10)))
        self.__texture.blit(self.__current_menace_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + (self.__life_bar.get_height()+10)*2)))

        master.blit(self.__texture, (self.position.x, self.position.y))

class GroupPanel(InputEventHandler, Draw):
    def __init__(self, group: Group, width: int, height: int, position: Position) -> None:
        self.__group: Group = group
        self.__members_panels: list[MemberPanel] = []
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        for member in self.__group.members:
            self.__members_panels.append(MemberPanel(member=member))

    
    def handle(self, event: pygame.event.Event):
        self.__group.handle(event)
        self.__members_panels.clear()
        member_panel_position: Position = Position(0, 0)
        for member in self.__group.members:
            member_panel: MemberPanel = MemberPanel(member=member)
            member_panel.position = Position(member_panel_position.x, member_panel_position.y)
            self.__members_panels.append(member_panel)
            member_panel_position.y += member_panel.height
            member_panel.handle(event)
        self.__texture = pygame.Surface((self.__texture.get_width(), member_panel_position.y))
    
    def draw(self, master: pygame.Surface):
        self.__group.draw(master)
        self.__texture.fill(pygame.Color(0,0,0, 0))
        for member_panel in self.__members_panels:
            member_panel.draw(self.__texture)
        master.blit(self.__texture, (self.__position.x,self.__position.y))

class ActionPanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.character: Character = None
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position

    
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(200,200,200))
        master.blit(self.__texture, (self.__position.x, self.__position.y))


class App:
    """Class that represents the program.
    """
    FRAMES_PER_SECOND: int = 60
    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080
    TIMELINE_WIDTH: int = WINDOW_WIDTH
    TIMELINE_HEIGHT: int = 100
    WORKSPACE_WIDTH: int = WINDOW_WIDTH / 2
    WORKSPACE_HEIGHT: int = WINDOW_HEIGHT - TIMELINE_HEIGHT
    MOVIE_WIDTH: int = WORKSPACE_WIDTH
    MOVIE_HEIGHT: int = WORKSPACE_HEIGHT
    MOVIE_FPS: int = 30
    BACKGROUND_COLOR: pygame.Color = pygame.Color(0, 0, 0)
    GROUP_PANEL_WIDTH: int = 250
    GROUP_PANEL_HEIGHT: int = 600
    GROUP_PANEL_POSITION: Position = Position(10, 10)
    ACTION_PANEL_WIDTH: int = WINDOW_WIDTH/1.5
    ACTION_PANEL_HEIGHT: int = 80
    ACTION_PANEL_POSITION: Position = Position(WINDOW_WIDTH/6, WINDOW_HEIGHT-ACTION_PANEL_HEIGHT)
    RETURN_SPEED = 2
    FRIENDS_NAMES: list[str] = [
        "Victor TRUONG",
        "Rébecca MOLARET",
        "Lucie LAURENT",
        "Jimi TRUONG",
        "Anthony GIRARDO",
        "Nicolas PIAR",
        "C... M... 3e",
    ]

    def __init__(self) -> None:
        print("Starting application...")
        print("Creating window...")
        # self.screen: pygame.Surface = pygame.display.set_mode((App.WINDOW_WIDTH, App.WINDOW_HEIGHT))
        self.screen: pygame.Surface = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Sprites Motion Creator")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running: bool = True
        self.__action_panel: ActionPanel = ActionPanel(App.ACTION_PANEL_WIDTH, App.ACTION_PANEL_HEIGHT, App.ACTION_PANEL_POSITION)
        self.__available_friends: Group = Group(max_capacity=10)
        self.__enemies: Group = Group(max_capacity=100)
        self.__group_of_the_player: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__group_of_the_player, width=App.GROUP_PANEL_WIDTH, height=App.GROUP_PANEL_HEIGHT, position=App.GROUP_PANEL_POSITION)
        self.__played_character: Character = None
        
    def __generate_friends(self):
        for name in App.FRIENDS_NAMES:
            friend: Character = Character(name)
            friend.position = Position(
                randint(0, App.WINDOW_WIDTH), randint(0, App.WINDOW_HEIGHT))
            friend.menace = 20
            self.__available_friends.add_member(friend)
        
    def __generate_enemies(self):
        for counter in range(randint(10, 100)):
            enemy: Enemy = Enemy("Vilain #" + str(counter))
            enemy.menace = 100
            enemy.zone_radius = 200
            enemy.position = Position(randint(0, App.WINDOW_WIDTH), randint(0, App.WINDOW_HEIGHT))
            enemy.zone_center = Position(enemy.position.x, enemy.position.y)
            self.__enemies.add_member(enemy)

    def __generate_player_character(self):
        player: Character = Character("Nicolas METIVIER")
        player.position = Position(
            randint(0, App.WINDOW_WIDTH), randint(0, App.WINDOW_HEIGHT))
        player.select()
        player.menace = 20.0
        self.__group_of_the_player.add_member(player)
        self.__played_character = player
    
    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.position.x < (App.GROUP_PANEL_WIDTH + App.GROUP_PANEL_POSITION.x)):
            character.position.x = App.GROUP_PANEL_WIDTH + App.GROUP_PANEL_POSITION.x
        if (character.position.x > self.screen.get_width()):
            character.position.x = self.screen.get_width()
        if (character.position.y < 0):
            character.position.y = 0
        if (character.position.y > self.screen.get_height()):
            character.position.y = self.screen.get_height()

    def __handle_interaction_and_moves_for_friends(self, group: Group):
        for member in group.members:
            others: list[Character] = [
                other for other in group.members if other is not member]
            others += self.__available_friends.members
            others += self.__enemies.members
            for other in others:
                if member.is_touching(other):
                    member.avoid_collision_with_other(other)
            if member.is_touching(self.__played_character):
                member.avoid_collision_with_other(self.__played_character)
            else:
                member.follow(self.__played_character)
            self.__prevent_character_to_disapear_from_scene(member)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        
        # if (attacking_enemy is None):
        #     self.__played_character.is_in_fight_mode = False
        
        if Geometry.compute_distance(enemy.position, enemy.zone_center) > 1:
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.zone_center.x - enemy.position.x
            direction_y = enemy.zone_center.y - enemy.position.y
            direction_length = Geometry.compute_distance(enemy.position, enemy.zone_center)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa position initiale
            enemy.position.x += direction_x * App.RETURN_SPEED
            enemy.position.y += direction_y * App.RETURN_SPEED

    def __prepare_enemy_to_fight(self, enemy: Enemy, target: Character):
        target.is_in_fight_mode = True
        distance_between_enemy_and_zone_center = Geometry.compute_distance(enemy.position, enemy.zone_center)
        if distance_between_enemy_and_zone_center < enemy.zone_radius:
            enemy.follow(target)
            

    def __recruit_member(self, member: Character):
        if (not self.__group_of_the_player.is_full()):
            self.__group_of_the_player.add_member(member)
            self.__available_friends.remove_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.__played_character)):
            self.__recruit_member(member)
        

    def run(self):
        
        self.__generate_player_character()
        self.__generate_friends()
        self.__generate_enemies()

        
        joystick: pygame.joystick.Joystick
        while (self.is_running):
            events: list[pygame.event.Event] = pygame.event.get()
            if (len(events) > 0):
                for event in events:
                    if (event.type == pygame.JOYDEVICEADDED):
                        joystick = pygame.joystick.Joystick(event.device_index)
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    else:
                        # HANDLE YOUR GAME HERE
                        self.__available_friends.handle(event)
                        self.__group_panel.handle(event)
                        self.__action_panel.handle(event)
            else:
                self.__available_friends.handle(None)
                self.__group_panel.handle(None)
                self.__action_panel.handle(None)
            
            self.__played_character = [character for character in self.__group_of_the_player.members if character.is_selected()][0]
            self.__action_panel.character = self.__played_character
            if (self.__played_character.is_moving):
                for member in self.__available_friends.members:
                    self.__recruit_member_if_is_touching(member)

            self.__handle_interaction_and_moves_for_friends(self.__group_of_the_player)

            for enemy in self.__enemies.members:
                if (enemy.is_feel_threatened(self.__played_character)):
                    self.__prepare_enemy_to_fight(enemy, self.__played_character)
                else:
                    self.__move_enemy_to_the_default_observation_position(enemy)
            self.screen.fill(App.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            self.__enemies.draw(self.screen)
            self.__available_friends.draw(self.screen)
            self.__group_panel.draw(self.screen)
            self.__action_panel.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(App.FRAMES_PER_SECOND)
        pygame.quit()

    @staticmethod
    def main():
        app: App = App()
        app.run()


if (__name__ == "__main__"):
    App.main()
