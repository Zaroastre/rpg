import pygame

from rpg.geometry import Position
from rpg.characters import Character, Group
from rpg.gameapi import InputEventHandler, Draw

import rpg.constants

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


class CharacterComponent(pygame.sprite.Sprite, InputEventHandler, Draw):
    MENACE_AREA_COLOR: pygame.Color = pygame.Color(255, 255, 0, a=100)
    ZONING_AREA_COLOR: pygame.Color = pygame.Color(255,200, 0)
    def __init__(self, character: Character) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__character: Character = character
        self.__is_selected: bool = False
        self._texture = pygame.Surface([self.__character.radius*2, self.__character.radius*2], pygame.SRCALPHA)
        self._hitbox: pygame.Rect = None
        self.__font_size: int = 20
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self._title: pygame.Surface = self.__font.render(
            self.__character.name[0], True, self.__font_color)
    
    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False


    @property
    def hitbox(self) -> pygame.Rect:
        return self._hitbox
    
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
        self.__character.is_moving = self.__is_going_to_the_bottom or self.__is_going_to_the_left or self.__is_going_to_the_right or self.__is_going_to_the_top
        
    def __handle_apply_moves(self):
        if (self.__character.previous_position != self.__character.position):
            self.__character.previous_position = self.__character.position.copy()
        is_moving_in_diagonal = (self.__is_going_to_the_left or self.__is_going_to_the_right) and \
                                (self.__is_going_to_the_top or self.__is_going_to_the_bottom)
        if (is_moving_in_diagonal):

            if self.__is_going_to_the_left and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self.__character.position.x -= self.__move_speed / sqrt(2)
            if self.__is_going_to_the_right and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self.__character.position.x += self.__move_speed / sqrt(2)
            if self.__is_going_to_the_top and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self.__character.position.y -= self.__move_speed / sqrt(2)
            if self.__is_going_to_the_bottom and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self.__character.position.y += self.__move_speed / sqrt(2)
        else:
            if self.__is_going_to_the_left:
                self.__character.position.x -= self.__move_speed
            if self.__is_going_to_the_right:
                self.__character.position.x += self.__move_speed
            if self.__is_going_to_the_top:
                self.__character.position.y -= self.__move_speed
            if self.__is_going_to_the_bottom:
                self.__character.position.y += self.__move_speed

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
            # new_projectil: Projectil = Projectil(True, 10.0, 5.0, self.previous_position.copy(), self.position.copy(), 5)
            # self.trigged_projectils.append(new_projectil)
            pass
        self.__handle_detect_aoe_position(event)
    

    def handle(self, event: pygame.event.Event):
        if event is not None:
            if self.is_selected():
                self.__handle_detect_moves_direction(event)
                    
        self.__handle_apply_moves()
        if event is not None:
            if self.is_selected():
                self.__handle_attack_ations(event)
        
        for projectil in self.__character.trigged_projectils:
            projectil.handle(event)
            if (projectil.to_position.x < 0 or projectil.to_position.x > rpg.constants.WINDOW_WIDTH) or (projectil.to_position.y < 0 or projectil.to_position.y > rpg.constants.WINDOW_HEIGHT):
                self.__character.trigged_projectils.remove(projectil)
                del projectil

    def draw(self, master: pygame.Surface):
        pygame.draw.circle(master, CharacterComponent.MENACE_AREA_COLOR, (self.__character.position.x,self.__character.position.y), self.__character.menace, 2)
        if (self.__character.zone_center is not None):
            pygame.draw.circle(master, CharacterComponent.ZONING_AREA_COLOR, (self.__character.zone_center.x,self.__character.zone_center.y), self.__character.zone_radius, 1)
        self._texture.fill(pygame.Color(0,0,0,0))
        point_color: pygame.Color
        if (self.is_selected()):
            point_color = pygame.Color(50,150,50)
        else:
            point_color = pygame.Color(0,150,250)
        self._hitbox = pygame.draw.circle(
            self._texture, point_color, (self.__character.radius, self.__character.radius), self.__character.radius)
        self._hitbox = master.blit(self._texture, (self.__character.position.x-self.__character.radius, self.__character.position.y-self.__character.radius))
        master.blit(self._title, (self.__character.position.x-(self.__character.radius/2), self.__character.position.y-(self.__character.radius/2)))
        for projectil in self.__character.trigged_projectils:
            projectil.draw(master)

