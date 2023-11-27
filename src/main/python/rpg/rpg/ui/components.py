from math import sqrt

import pygame
import rpg.constants
from rpg.characters import Character, Enemy, Projectil
from rpg.gameapi import Draw, InputEventHandler
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry, Position


class ProjectilComponent(pygame.sprite.Sprite, InputEventHandler, Draw):
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

class CharacterComponent(pygame.sprite.Sprite, InputEventHandler, Draw):
    MENACE_AREA_COLOR: pygame.Color = pygame.Color(255, 255, 0, a=100)
    ZONING_AREA_COLOR: pygame.Color = pygame.Color(255,200, 0)
    def __init__(self, character: Character) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__is_going_to_the_left: bool = False
        self.__is_going_to_the_bottom: bool = False
        self.__is_going_to_the_right: bool = False
        self.__is_going_to_the_top: bool = False
        self._character: Character = character
        self.__is_selected: bool = False
        self._texture = pygame.Surface([self._character.radius*2, self._character.radius*2], pygame.SRCALPHA)
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 20
        self.__texture_color: pygame.Color = self._character.character_class.class_type.value.color
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self._title: pygame.Surface = self.__font.render(
            self._character.name[0], True, self.__font_color)
        self.__projectils_components: list[ProjectilComponent] = []
    
    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    @property
    def character(self) -> Character:
        return self._character

    @property
    def projectils(self) -> list[ProjectilComponent]:
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
        self._character.is_moving = self.__is_going_to_the_bottom or self.__is_going_to_the_left or self.__is_going_to_the_right or self.__is_going_to_the_top
        
        
    def __move_player(self):
        if (self._character.previous_position != self._character.get_position()):
            self._character.previous_position = self._character.get_position().copy()
        is_moving_in_diagonal = (self.__is_going_to_the_left or self.__is_going_to_the_right) and \
                                (self.__is_going_to_the_top or self.__is_going_to_the_bottom)
        if (is_moving_in_diagonal):

            if self.__is_going_to_the_left and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self._character.get_position().x -= self._character.move_speed / sqrt(2)
            if self.__is_going_to_the_right and (self.__is_going_to_the_top or self.__is_going_to_the_bottom):
                self._character.get_position().x += self._character.move_speed / sqrt(2)
            if self.__is_going_to_the_top and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self._character.get_position().y -= self._character.move_speed / sqrt(2)
            if self.__is_going_to_the_bottom and (self.__is_going_to_the_left or self.__is_going_to_the_right):
                self._character.get_position().y += self._character.move_speed / sqrt(2)
        else:
            if self.__is_going_to_the_left:
                self._character.get_position().x -= self._character.move_speed
            if self.__is_going_to_the_right:
                self._character.get_position().x += self._character.move_speed
            if self.__is_going_to_the_top:
                self._character.get_position().y -= self._character.move_speed
            if self.__is_going_to_the_bottom:
                self._character.get_position().y += self._character.move_speed

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
            self._character.attack()
            trigged_projectil: Projectil = self._character.trigged_projectils[-1]
            self.__projectils_components.append(ProjectilComponent(trigged_projectil))
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_2) or (event.type == pygame.JOYBUTTONDOWN and event.button == 3):
            self._character.attack()
            trigged_projectil: Projectil = self._character.trigged_projectils[-1]
            self.__projectils_components.append(ProjectilComponent(trigged_projectil))
        self.__handle_detect_aoe_position(event)
    
    def __freeze_player_on_place(self):
        self.__is_going_to_the_bottom = False
        self.__is_going_to_the_top = False
        self.__is_going_to_the_left = False
        self.__is_going_to_the_right = False
        self.character.is_moving = False

    def __prevent_projectil_to_disapear_from_screen(self, projectil_sprite: ProjectilComponent):
        if (projectil_sprite.projectil.to_position.x < 0 or projectil_sprite.projectil.to_position.x > rpg.constants.WINDOW_WIDTH) or (projectil_sprite.projectil.to_position.y < 0 or projectil_sprite.projectil.to_position.y > rpg.constants.WINDOW_HEIGHT):
            self._character.trigged_projectils.remove(projectil_sprite.projectil)
            # del projectil_sprite.projectil
            self.__projectils_components.remove(projectil_sprite)
            del projectil_sprite

    def handle(self, event: pygame.event.Event):
        if event is not None:
            if self._character.is_selected():
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
        # pygame.draw.circle(master, CharacterComponent.MENACE_AREA_COLOR, (self._character.get_position().x,self._character.get_position().y), self._character.threat.level, 2)
        if (self._character.zone_center is not None):
            pygame.draw.circle(master, CharacterComponent.ZONING_AREA_COLOR, (self._character.zone_center.x,self._character.zone_center.y), self._character.zone_radius, 1)
        self._texture.fill(pygame.Color(0,0,0,0))
        self.__hitbox = pygame.draw.circle(
            self._texture, self.__texture_color, (self._character.radius, self._character.radius), self._character.radius)
        self.__hitbox = master.blit(self._texture, (self._character.get_position().x-self._character.radius, self._character.get_position().y-self._character.radius))
        master.blit(self._title, (self._character.get_position().x-(self._character.radius/2), self._character.get_position().y-(self._character.radius/2)))
        for projectil in self._character.trigged_projectils:
            projectil_component: ProjectilComponent = ProjectilComponent(projectil)
            projectil_component.draw(master)

class EnemyComponent(CharacterComponent):
    def __init__(self, enemy: Enemy) -> None:
        super().__init__(enemy)
        self.__dificulty_color: pygame.Color = pygame.Color(255,150,0)
    @property
    def character(self) -> Enemy:
        return super().character
    def draw(self, master: pygame.Surface):
        pygame.draw.circle(master, self.character.character_class.class_type.value.color, (self._character.get_position().x,self._character.get_position().y), self._character.aggro_area_radius, 2)
        self._texture.fill(pygame.Color(0,0,0,0))
        self._hitbox = pygame.draw.circle(
            self._texture, self.__dificulty_color, (self._character.radius, self._character.radius), self._character.radius)
        self._hitbox = master.blit(self._texture, (self._character.get_position().x-self._character.radius, self._character.get_position().y-self._character.radius))
        lifebar: pygame.Surface = pygame.Surface((50, 10))
        lifebar.fill(pygame.Color(100,0,0))
        lifeleft: pygame.Surface = pygame.Surface((((self.character.life.current *lifebar.get_width())/self.character.life.maximum), lifebar.get_height()))
        lifeleft.fill(pygame.Color(255,0,0))
        lifebar.blit(lifeleft, (0,0))
        master.blit(lifebar, (self.character.get_position().x-(lifebar.get_width()/2), self.character.get_position().y+self.character.radius+lifebar.get_height()))
        for projectil in self._character.trigged_projectils:
            projectil_component: ProjectilComponent = ProjectilComponent(projectil)
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
