from math import sqrt

import pygame
import rpg.constants
from rpg.characters import Character, Enemy, Projectil
from rpg.gameapi import Draw, InputEventHandler
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry, Position


class ProjectilSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    HEALTH_COLOR: pygame.Color = pygame.Color(0, 200, 0)
    DAMAGE_COLOR: pygame.Color = pygame.Color(200, 0, 0)
    def __init__(self, projectil: Projectil) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__projectil: Projectil = projectil
        self.__rect: pygame.Rect = pygame.Rect(0,0,0,0)

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
    @property
    def projectil(self) -> Projectil:
        return self.__projectil

    def handle(self, event: pygame.event.Event):
        self.__projectil.to_position = Geometry.compute_new_point_using_speed(self.__projectil.from_position, self.__projectil.to_position, self.__projectil.move_speed)
    
    def draw(self, master: pygame.Surface):
        self.__rect = pygame.draw.circle(master, self.__projectil.color, (self.__projectil.to_position.x, self.__projectil.to_position.y), self.__projectil.radius)

class CharacterSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    MENACE_AREA_COLOR: pygame.Color = pygame.Color(255, 255, 0, a=100)
    ZONING_AREA_COLOR: pygame.Color = pygame.Color(255,200, 0)
    def __init__(self, character: Character) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__is_going_to_the_left: bool = False
        self.__is_going_to_the_bottom: bool = False
        self.__is_going_to_the_right: bool = False
        self.__is_going_to_the_top: bool = False
        self.__character: Character = character
        self.__is_selected: bool = False
        self.image = pygame.Surface([self.character.radius*2, self.character.radius*2], pygame.SRCALPHA)
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 20
        self.__texture_color: pygame.Color = self.character.character_class.class_type.value.color
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self._title: pygame.Surface = self.__font.render(
            self.character.name[0], True, self.__font_color)
        self.__projectils_components: list[ProjectilSprite] = []

    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    @property
    def character(self) -> Character:
        return self.__character

    @property
    def projectils(self) -> list[ProjectilSprite]:
        return self.__projectils_components

    @property
    def hitbox(self) -> pygame.Rect:
        return self.__hitbox
    
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
        
        
    def __move_player(self):
        self.character.move(self.__is_going_to_the_top, self.__is_going_to_the_bottom, self.__is_going_to_the_left, self.__is_going_to_the_right, self.character.move_speed)

    def __handle_detect_aoe_position(self, event: pygame.event.Event):
        if (event.type == pygame.MOUSEMOTION):
            # print("AOE with Mouse")
            pass
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
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_1) or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
            self.character.attack()
            trigged_projectil: Projectil = self.character.trigged_projectils[-1]
            self.__projectils_components.append(ProjectilSprite(trigged_projectil))
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_2) or (event.type == pygame.JOYBUTTONDOWN and event.button == 3):
            self.character.attack()
            trigged_projectil: Projectil = self.character.trigged_projectils[-1]
            self.__projectils_components.append(ProjectilSprite(trigged_projectil))
        self.__handle_detect_aoe_position(event)
    
    def __freeze_player_on_place(self):
        self.__is_going_to_the_bottom = False
        self.__is_going_to_the_top = False
        self.__is_going_to_the_left = False
        self.__is_going_to_the_right = False
        self.character.is_moving = False

    def __prevent_projectil_to_disapear_from_screen(self, projectil_sprite: ProjectilSprite):
        if (projectil_sprite.projectil.to_position.x < 0 or projectil_sprite.projectil.to_position.x > rpg.constants.WINDOW_WIDTH) or (projectil_sprite.projectil.to_position.y < 0 or projectil_sprite.projectil.to_position.y > rpg.constants.WINDOW_HEIGHT):
            self.character.trigged_projectils.remove(projectil_sprite.projectil)
            # del projectil_sprite.projectil
            self.__projectils_components.remove(projectil_sprite)
            del projectil_sprite

    def handle(self, event: pygame.event.Event):
        if event is not None:
            if self.character.is_selected():
                if (self.character.life.is_alive()):
                    self.__handle_detect_moves_direction(event)
                else:
                    self.__freeze_player_on_place()
        if (self.character.life.is_alive()):
            self.__move_player()
        if event is not None:
            if self.character.is_selected():
                if (self.character.life.is_alive()):
                    self.__handle_attack_ations(event)
        
        for projectil_sprite in self.__projectils_components:
            projectil_sprite.handle(event)
            self.__prevent_projectil_to_disapear_from_screen(projectil_sprite)

    def draw(self, master: pygame.Surface):
        # pygame.draw.circle(master, CharacterSprite.MENACE_AREA_COLOR, (self.character.current_position.x,self.character.current_position.y), self.character.threat.level, 2)
        if (self.character.is_selected()):
            corner_size: int = 10
            border_size: int = 5
            panel: pygame.Surface = pygame.Surface((((self.character.radius*2)+(border_size*4)), ((self.character.radius*2)+(border_size*4))))
            horizontal_rect: pygame.Surface = pygame.Surface((panel.get_width(), (panel.get_height()-(corner_size*2))))
            vertical_rect: pygame.Surface = pygame.Surface(((panel.get_width()-(corner_size*2)), panel.get_height()))
            background: pygame.Surface = pygame.Surface(((panel.get_width()-(border_size*2)), (panel.get_height()-(border_size*2))))
            vertical_rect.fill(pygame.Color(0,0,0))
            horizontal_rect.fill(pygame.Color(0,0,0))
            panel.fill(pygame.Color(255,0,0))
            panel.blit(background, (border_size, border_size))
            panel.blit(vertical_rect, (corner_size, 0))
            panel.blit(horizontal_rect, (0, corner_size))
            master.blit(panel, ((self.character.current_position.x - (panel.get_width()/2)),(self.character.current_position.y - (panel.get_height()/2))))
        
        if (self.character.zone_center is not None):
            pygame.draw.circle(master, CharacterSprite.ZONING_AREA_COLOR, (self.character.zone_center.x,self.character.zone_center.y), self.character.zone_radius, 1)
        self.image.fill(pygame.Color(0,0,0,0))
        self.__hitbox = pygame.draw.circle(
            self.image, self.__texture_color, (self.character.radius, self.character.radius), self.character.radius)
        self.__hitbox = master.blit(self.image, (self.character.current_position.x-self.character.radius, self.character.current_position.y-self.character.radius))
        master.blit(self._title, (self.character.current_position.x-(self.character.radius/2), self.character.current_position.y-(self.character.radius/2)))
        for projectil in self.character.trigged_projectils:
            projectil_component: ProjectilSprite = ProjectilSprite(projectil)
            projectil_component.draw(master)

class EnemySprite(CharacterSprite):
    def __init__(self, enemy: Enemy) -> None:
        super().__init__(enemy)
        self.__dificulty_color: pygame.Color = pygame.Color(255,150,0)
    @property
    def character(self) -> Enemy:
        return super().character

    def draw(self, master: pygame.Surface):
        
        pygame.draw.line(master, self.character.character_class.class_type.value.color, (self.character.default_position.x, self.character.default_position.y), (self.character.current_position.x, self.character.current_position.y))
        pygame.draw.circle(master, self.character.character_class.class_type.value.color, (self.character.current_position.x,self.character.current_position.y), self.character.radius + self.character.aggro_area_radius)
        pygame.draw.circle(master, self.character.character_class.class_type.value.color, (self.character.default_position.x,self.character.default_position.y), self.character.zone_radius, 2)
        self.image.fill(pygame.Color(0,0,0,0))
        self._hitbox = pygame.draw.circle(
            self.image, self.__dificulty_color, (self.character.radius, self.character.radius), self.character.radius)
        self._hitbox = master.blit(self.image, (self.character.current_position.x-self.character.radius, self.character.current_position.y-self.character.radius))
        lifebar: pygame.Surface = pygame.Surface((50, 10))
        lifebar.fill(pygame.Color(100,0,0))
        lifeleft: pygame.Surface = pygame.Surface((((self.character.life.current *lifebar.get_width())/self.character.life.maximum), lifebar.get_height()))
        lifeleft.fill(pygame.Color(255,0,0))
        lifebar.blit(lifeleft, (0,0))
        master.blit(lifebar, (self.character.current_position.x-(lifebar.get_width()/2), self.character.current_position.y+self.character.radius+lifebar.get_height()))
        for projectil in self.character.trigged_projectils:
            projectil_component: ProjectilSprite = ProjectilSprite(projectil)
            projectil_component.draw(master)

    def set_difficulty_color(self, color: pygame.Color):
        self.__dificulty_color = color
        

class GroupComponent(pygame.sprite.Sprite, InputEventHandler, Draw):
    def __init__(self, group: Group) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__group: Group = group

    @property
    def group(self) -> Group:
        return self.__group
    
    
    def __handle_character_selection_in_group(self, event: pygame.event.Event):
        selected_members: list[Character] = [member for member in self.group.members if member.is_selected()]
        if (len(selected_members) == 1):
            previous_selected_member = selected_members[0]
            index: int = self.group.members.index(previous_selected_member)
            if (event.type == pygame.JOYBUTTONDOWN and event.button == 5):
                if (index+1 > len(self.group.members)-1):
                    index = 0
                else:
                    index += 1
            if (event.type == pygame.JOYBUTTONDOWN and event.button == 4):
                if (index == 0):
                    index = len(self.group.members)-1
                else:
                    index -= 1
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_F1):
                index=0
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F2):
                index=1
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F3):
                index=2
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F4):
                index=3
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F5):
                index=4
            previous_selected_member.unselect()
            self.group.members[index].select()

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            self.__handle_character_selection_in_group(event)
        # for member in self.group.members:
        #     member.handle(event)
        

    def draw(self, master: pygame.Surface):
        # for member in self.group.members:
        #     member.draw(master)
        pass
