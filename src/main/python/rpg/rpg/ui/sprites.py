from math import sqrt

import pygame
from pygame.event import Event
import rpg.constants
from rpg.characters import Character, Enemy, Projectil
from rpg.gameapi import Draw, InputEventHandler
from rpg.gameplay.teams import Group
from rpg.gameplay.breeds import BreedType
from rpg.gameplay.genders import Gender
from rpg.gameplay.physiology import Morphology
from rpg.math.geometry import Geometry, Position
from rpg.gameplay.physiology import Skeleton, Joint

class AvatarRulerSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    def __init__(self, size: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__size: int = size
        self.__width: int = 20
        self.__thickness: int = 2
        self.__font_size: int = 22
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__ruler_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__breed_ruler_color: pygame.Color = pygame.Color(0, 255, 0)
        self.__min_size_label: pygame.Surface = self.__font.render(str(0), True, self.__font_color)
        self.__max_size_label: pygame.Surface = self.__font.render(str(self.__size), True, self.__font_color)
        self.image = pygame.Surface((self.__width+(self.__thickness*2)+self.__max_size_label.get_width(), self.__size+(self.__thickness*2)+self.__max_size_label.get_height()), pygame.SRCALPHA)        
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.__breed_type: BreedType|None = None
        self.__gender: Gender|None = None
        
    
    def set_breed(self, breed_type: BreedType):
        self.__breed_type = breed_type
        
    def set_gender(self, gender: Gender):
        self.__gender = gender

    def __draw_default_rule(self, master: pygame.Surface):
        start_x: int = self.__max_size_label.get_width()+(self.__width/2)
        stop_x: int = self.__max_size_label.get_width()+(self.__width/2)
        start_y: int = 0+(self.__max_size_label.get_height()/2)
        stop_y: int = self.__size+(self.__max_size_label.get_height()/2)
        vertical_line: pygame.Rect = pygame.draw.line(self.image, self.__ruler_color, (start_x, start_y), (stop_x, stop_y), self.__thickness)
        start_x = self.__max_size_label.get_width()
        stop_x = self.__max_size_label.get_width()+self.__width
        start_y = (self.__max_size_label.get_height()/2)
        stop_y = (self.__max_size_label.get_height()/2)
        top_horizontal_line: pygame.Rect = pygame.draw.line(self.image, self.__ruler_color, (start_x, start_y), (stop_x, stop_y), self.__thickness)
        start_y = self.__size+(self.__max_size_label.get_height()/2)
        stop_y = self.__size+(self.__max_size_label.get_height()/2)
        bottom_horizontal_line: pygame.Rect = pygame.draw.line(self.image, self.__ruler_color, (start_x, start_y), (stop_x, stop_y), self.__thickness)
        self.image.blit(self.__max_size_label, (0, 0))
        self.image.blit(self.__min_size_label, (0, self.__size))

    def __draw_specific_rule_for_breed(self, master: pygame.Surface):
        if ((self.__breed_type is not None) and (self.__gender is not None)):
            min_size: int = 0
            max_size: int = self.__size
            morphology: Morphology|None = self.__breed_type.value.get_morphology(self.__gender)

            if (morphology is not None):
                min_size = morphology.size.minimum
                max_size = morphology.size.maximum

            origin_y_for_smaller_size: int = self.offset.y + self.__size

            x: int = self.offset.x
            min_x: int = x-5
            max_x: int = x+5
            min_y: int = origin_y_for_smaller_size-min_size
            max_y: int = origin_y_for_smaller_size-max_size

            pygame.draw.line(master, pygame.Color(0,255,0), (x, min_y), (x, max_y), 4) # Bas en Haut
            pygame.draw.line(master, pygame.Color(0,255,0), (min_x, min_y), (max_x, min_y), 2)
            pygame.draw.line(master, pygame.Color(0,255,0), (min_x, max_y), (max_x, max_y), 2)
            
            min_size_label: pygame.Surface = self.__font.render(str(min_size), True, self.__font_color)
            max_size_label: pygame.Surface = self.__font.render(str(max_size), True, self.__font_color)
            
            master.blit(min_size_label, (x+10+10, min_y-(min_size_label.get_height()/2)))
            master.blit(max_size_label, (x+10+10, max_y-(max_size_label.get_height()/2)))

    def draw(self, master: pygame.Surface):
        self.__draw_default_rule(master)
        self.__draw_specific_rule_for_breed(master)
        master.blit(self.image, self.offset)

class JointSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    def __init__(self, joint: Joint, sprites_group: pygame.sprite.Group) -> None:
        pygame.sprite.Sprite.__init__(self, sprites_group)
        self.__joint: Joint = joint
        self.image = pygame.Surface((self.__joint.radius*2, self.__joint.radius*2), pygame.SRCALPHA)        
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.__hitbox: pygame.Rect = None
        self.offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.__must_display_rotation_circle: bool = False
        self.__texture_color: pygame.Color = pygame.Color(200, 200, 200)
        self.__radius_rotation_color: pygame.Color = pygame.Color(200, 200, 200)

    @property
    def joint(self) -> Joint:
        return self.__joint
    
    def handle(self, event: Event):
        mouse_position: tuple[int, int] = pygame.mouse.get_pos()
        is_mouse_hover: bool = self.rect.collidepoint(mouse_position)
        if (self.rect is not None):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (is_mouse_hover):
                    self.__joint.select()
            if (event.type == pygame.MOUSEBUTTONUP):
                if (self.__joint.is_selected()):
                    self.__joint.unselect()
            self.__must_display_rotation_circle = self.__joint.is_selected()
        if (is_mouse_hover):
            self.__must_display_rotation_circle = True

    def draw(self, master: pygame.Surface):
        self.rect = pygame.draw.circle(master, self.__texture_color, [self.joint.position.x+self.offset.x, self.joint.position.y+self.offset.y], 5)
        if (self.__must_display_rotation_circle):
            if (self.joint.parent is not None and self.joint.parent.parent is not None):
                pygame.draw.circle(master, self.__radius_rotation_color, [self.joint.parent.position.x+self.offset.x, self.joint.parent.position.y+self.offset.y], 20, 2)

class SkeletonSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    def __init__(self, skeleton: Skeleton, sprites_group: pygame.sprite.Group) -> None:
        pygame.sprite.Sprite.__init__(self, sprites_group)
        self.__joints_sprites: list[JointSprite] = []
        self.image = pygame.Surface((skeleton.size, skeleton.size), pygame.SRCALPHA)        
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.__hitbox: pygame.Rect = None
        self.offset: pygame.math.Vector2 = pygame.math.Vector2()
        for joint in skeleton.joints:
            joint_sprite: JointSprite = JointSprite(joint, pygame.sprite.Group())
            joint_sprite.offset = self.offset
            self.__joints_sprites.append(joint_sprite)

    @property
    def joints_sprites(self) -> list[JointSprite]:
        return self.__joints_sprites
    
    def handle(self, event: pygame.event.Event):
        if event is not None:
            for joints_sprite in self.__joints_sprites:
                joints_sprite.handle(event)
    
    def draw(self, master: pygame.Surface):
        vertical_offset = self.offset.y # - max(joint_sprite.joint.position.y for joint_sprite in self.__joints_sprites)
        horizontal_offset = self.offset.x
        
        for joint_sprite in self.__joints_sprites:
            if (joint_sprite.joint.parent is not None):
                pygame.draw.line(master, (255,255,255), (joint_sprite.joint.position.x+self.offset.x, joint_sprite.joint.position.y+self.offset.y), (joint_sprite.joint.parent.position.x+self.offset.x, joint_sprite.joint.parent.position.y+self.offset.y), 5)
            joint_sprite.offset.x = horizontal_offset
            joint_sprite.offset.y = vertical_offset
            joint_sprite.draw(master)

class ProjectilSprite(pygame.sprite.Sprite, InputEventHandler, Draw):
    HEALTH_COLOR: pygame.Color = pygame.Color(0, 200, 0)
    DAMAGE_COLOR: pygame.Color = pygame.Color(200, 0, 0)
    def __init__(self, projectil: Projectil, sprites_group: pygame.sprite.Group) -> None:
        pygame.sprite.Sprite.__init__(self, sprites_group)
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
        self.image = pygame.Surface((self.character.radius*2, self.character.radius*2), pygame.SRCALPHA, 32).convert_alpha()      
        self.rect = pygame.Rect(self.character.current_position.x-self.character.radius, self.character.current_position.y-self.character.radius, self.image.get_width(), self.image.get_height())
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
    # @property
    # def image(self) -> pygame.Surface:
    #     pass
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
            self.__projectils_components.append(ProjectilSprite(trigged_projectil, self.groups()[0]))
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_2) or (event.type == pygame.JOYBUTTONDOWN and event.button == 3):
            self.character.attack()
            trigged_projectil: Projectil = self.character.trigged_projectils[-1]
            self.__projectils_components.append(ProjectilSprite(trigged_projectil, self.groups()[0]))
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
        # offset_position = sprite.rect.topleft - self.offset
        # pygame.draw.circle(master, CharacterSprite.MENACE_AREA_COLOR, (self.character.current_position.x,self.character.current_position.y), self.character.threat.level, 2)
        if (self.character.zone_center is not None):
            pygame.draw.circle(master, CharacterSprite.ZONING_AREA_COLOR, (self.character.zone_center.x,self.character.zone_center.y), self.character.zone_radius, 1)
        # self.image.fill(pygame.Color(0,0,0,0))
        self.__hitbox = pygame.draw.circle(
            self.image, self.__texture_color, (self.character.radius, self.character.radius), self.character.radius)
        self.rect = master.blit(self.image, (self.character.current_position.x-self.character.radius, self.character.current_position.y-self.character.radius))
        master.blit(self._title, (self.character.current_position.x-(self.character.radius/2), self.character.current_position.y-(self.character.radius/2)))
        for projectil in self.character.trigged_projectils:
            projectil_component: ProjectilSprite = ProjectilSprite(projectil, self.groups()[0])
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
        self.rect = master.blit(self.image, (self.character.current_position.x-self.character.radius, self.character.current_position.y-self.character.radius))
        lifebar: pygame.Surface = pygame.Surface((50, 10))
        lifebar.fill(pygame.Color(100,0,0))
        lifeleft: pygame.Surface = pygame.Surface((((self.character.life.current *lifebar.get_width())/self.character.life.maximum), lifebar.get_height()))
        lifeleft.fill(pygame.Color(255,0,0))
        lifebar.blit(lifeleft, (0,0))
        master.blit(lifebar, (self.character.current_position.x-(lifebar.get_width()/2), self.character.current_position.y+self.character.radius+lifebar.get_height()))
        for projectil in self.character.trigged_projectils:
            projectil_component: ProjectilSprite = ProjectilSprite(projectil, self.groups()[0])
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
