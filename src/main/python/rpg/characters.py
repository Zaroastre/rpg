from math import sqrt

import pygame

import constants
from gameapi import Draw, InputEventHandler
from geometry import Geometry, Position

class Projectil(pygame.sprite.Sprite, InputEventHandler, Draw):
    HEALTH_COLOR: pygame.Color = pygame.Color(0, 200, 0)
    DAMAGE_COLOR: pygame.Color = pygame.Color(200, 0, 0)
    def __init__(self, is_damage: bool, value: float, move_speed: float, from_position: Position, to_position: Position, radius: float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.from_position: Position = from_position
        self.to_position: Position = to_position
        self.__move_speed: float = move_speed
        self.__is_damage: bool = is_damage
        self.radius: float = radius
        self._texture = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
    
    def handle(self, event: pygame.event.Event):
        self.to_position = Geometry.compute_new_point_using_speed(self.from_position, self.to_position, self.__move_speed)
    
    def draw(self, master: pygame.Surface):
        pygame.draw.circle(master, Projectil.HEALTH_COLOR if not self.__is_damage else Projectil.DAMAGE_COLOR, (self.to_position.x, self.to_position.y), self.radius)


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
            # self.previous_position = Position(self.position.x, self.position.y)
            self.position.x += direction_x * self.move_speed
            self.position.y += direction_y * self.move_speed

    def __handle_detect_moves_direction(self, event: pygame.event.Event):
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
        self.is_moving = self.__is_going_to_the_bottom or self.__is_going_to_the_left or self.__is_going_to_the_right or self.__is_going_to_the_top
        
    def __handle_apply_moves(self):
        if (self.previous_position != self.position):
            self.previous_position = self.position.copy()
        is_moving_in_diagonal = (self.__is_going_to_the_left or self.__is_going_to_the_right) and \
                                (self.__is_going_to_the_top or self.__is_going_to_the_bottom)
        if (is_moving_in_diagonal):

            if self.__is_going_to_the_left and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self.position.x -= self.__move_speed / sqrt(2)
            if self.__is_going_to_the_right and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self.position.x += self.__move_speed / sqrt(2)
            if self.__is_going_to_the_top and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self.position.y -= self.__move_speed / sqrt(2)
            if self.__is_going_to_the_bottom and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self.position.y += self.__move_speed / sqrt(2)
        else:
            if self.__is_going_to_the_left:
                self.position.x -= self.__move_speed
            if self.__is_going_to_the_right:
                self.position.x += self.__move_speed
            if self.__is_going_to_the_top:
                self.position.y -= self.__move_speed
            if self.__is_going_to_the_bottom:
                self.position.y += self.__move_speed

    def __handle_detect_aoe_position(self, event: pygame.event.Event):
        if (event.type == pygame.MOUSEMOTION):
            print("AOE with Mouse")
        else:
            if (event.type == pygame.JOYAXISMOTION and event.axis == 2 and event.value < 0.003906369212927641):
                print("AOE with JOY" + str(event.value))
            elif (event.type == pygame.JOYAXISMOTION and event.axis == 2 and event.value == 0.003906369212927641):
                print("Cancel AOE on 2")
            elif (event.type == pygame.JOYAXISMOTION and event.axis == 2 and event.value > 0.003906369212927641):
                print("AOE with JOY" + str(event.value))
            
            if (event.type == pygame.JOYAXISMOTION and event.axis == 3 and event.value < 0.003906369212927641):
                print("AOE with JOY" + str(event.value))
            elif (event.type == pygame.JOYAXISMOTION and event.axis == 3 and event.value == 0.003906369212927641):
                print("Cancel AOE on 3")
            elif (event.type == pygame.JOYAXISMOTION and event.axis == 3 and event.value > 0.003906369212927641):
                print("AOE with JOY" + str(event.value))
           
    def __handle_attack_ations(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
            new_projectil: Projectil = Projectil(True, 10.0, 5.0, self.previous_position.copy(), self.position.copy(), 5)
            self.trigged_projectils.append(new_projectil)
        self.__handle_detect_aoe_position(event)
    

    def handle(self, event: pygame.event.Event):
        if event is not None:
            if self.is_selected():
                self.__handle_detect_moves_direction(event)
                    
        self.__handle_apply_moves()
        if event is not None:
            if self.is_selected():
                self.__handle_attack_ations(event)
        
        for projectil in self.trigged_projectils:
            projectil.handle(event)
            if (projectil.to_position.x < 0 or projectil.to_position.x > constants.WINDOW_WIDTH) or (projectil.to_position.y < 0 or projectil.to_position.y > constants.WINDOW_HEIGHT):
                self.trigged_projectils.remove(projectil)
                del projectil

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
                # other.previous_position = other.position.copy()
                other.position.x -= direction_x * \
                    (min_distance - distance)
                other.position.y -= direction_y * \
                    (min_distance - distance)
            else:
                # self.previous_position = self.position.copy()
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
