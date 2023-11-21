import pygame
import rpg.constants
from rpg.characters import Character
from rpg.classes import Class
from rpg.gameapi import Draw, InputEventHandler
from rpg.math.geometry import Position
from rpg.spells import Spell
from rpg.teams import Group
from rpg.ui.components import CharacterComponent, GroupComponent


class SpellDetailPopup(InputEventHandler, Draw):
    def __init__(self, spell: Spell, character_class: Class, width: int, height: int, position: Position) -> None:
        self.__spell: Spell = spell
        self.__character_class: Class = character_class
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__font_size: int = 22
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(200, 200, 200)
        self.__spell_name: pygame.Surface = self.__font.render(
            self.__spell.name, True, self.__font_color)
        self.__spell_damage: pygame.Surface = self.__font.render(
            f"Range: {str(self.__spell.magical_effect_minimum)} - {str(self.__spell.magical_effect_maximum)}", True, self.__font_color)
        self.__spell_detail: pygame.Surface = self.__font.render(
            self.__spell.description, True, self.__font_color)
        self.__spell_incantation_duration: pygame.Surface = self.__font.render(
            f"Incantation: {str(self.__spell.incantation_duration)}", True, self.__font_color)
        self.__spell_cooldown: pygame.Surface = self.__font.render(
            f"Cooldown: {str(self.__spell.cooldown)}", True, self.__font_color)
        self.__spell_resource: pygame.Surface = self.__font.render(
            f"{self.__character_class.resource.resource_type.name.capitalize()}: {str(self.__spell.resource_usage)}", True, self.__font_color)
        self.__spell_duration: pygame.Surface = self.__font.render(
            f"Duration: {str(self.__spell.resource_usage)}", True, self.__font_color)
    
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(30,30,30))
        self.__texture.blit(self.__spell_name, (0,0))
        self.__texture.blit(self.__spell_damage, (0,self.__font_size))
        self.__texture.blit(self.__spell_resource, (0,self.__font_size*2))
        self.__texture.blit(self.__spell_duration, (0,self.__font_size*3))
        self.__texture.blit(self.__spell_incantation_duration, (0,self.__font_size*4))
        self.__texture.blit(self.__spell_cooldown, (0,(self.__font_size*5)))
        self.__texture.blit(self.__spell_detail, (0,self.__font_size*6))
        master.blit(self.__texture, (self.__position.x, self.__position.y))

class MemberPanel(InputEventHandler, Draw):
    def __init__(self, member: Character, width: int, height: int, position: Position) -> None:
        self.__member: Character = member
        self.__position: Position = position
        self.__font_size: int = 22
        self.__height: int = height
        self.__width: int = width
        self.__avatar_picture_radius: float = height
        self.__texture: pygame.Surface = pygame.Surface([self.__width, self.__avatar_picture_radius*2], pygame.SRCALPHA)
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__title: pygame.Surface = self.__font.render(
            self.__member.name + f"({self.__member.character_class.class_type.name})", True, self.__font_color)
        self.__current_life_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))
        self.__current_resource_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))
        self.__current_menace_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))
        self.__life_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))
        self.__resource_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))
        self.__menace_bar: pygame.Surface = pygame.Surface(((self.__width-self.__avatar_picture_radius), 10))

    @property
    def height(self) -> float:
        return self.__avatar_picture_radius*2

    def handle(self, event: pygame.event.Event):
        self.__current_life_bar = pygame.Surface((self.__width-self.__avatar_picture_radius, 10))
        self.__current_resource_bar = pygame.Surface((150, 10))
        self.__current_menace_bar = pygame.Surface(((self.__member.threat.level*(self.__width-self.__avatar_picture_radius))/100, 10))

    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(20,20,20))
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

        master.blit(self.__texture, (self.__position.x, self.__position.y))

class GroupPanel(InputEventHandler, Draw):
    def __init__(self, group: Group, width: int, height: int, position: Position) -> None:
        self.__group_component: GroupComponent = GroupComponent(group)
        self.__members_panels: list[MemberPanel] = []
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position



    def handle(self, event: pygame.event.Event):
        self.__group_component.handle(event)
        self.__members_panels.clear()
        member_panel_position: Position = Position(0, 0)
        for member in self.__group_component.group.members:
            member_panel: MemberPanel = MemberPanel(member=member, width=rpg.constants.MEMBER_PANEL_WIDTH, height=rpg.constants.MEMBER_PANEL_HEIGHT, position=member_panel_position.copy())
            self.__members_panels.append(member_panel)
            member_panel_position.y += member_panel.height
            member_panel.handle(event)
        self.__texture = pygame.Surface((self.__texture.get_width(), member_panel_position.y))
    
    def draw(self, master: pygame.Surface):
        self.__group_component.draw(master)
        self.__texture.fill(pygame.Color(10,10,10, 0))
        for member_panel in self.__members_panels:
            member_panel.draw(self.__texture)
        master.blit(self.__texture, (self.__position.x,self.__position.y))

class SpellPanel(InputEventHandler, Draw):
    def __init__(self, spell: Spell, width: int, height: int, position: Position) -> None:
        self.__spell: Spell = spell
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__font_size: int = 22
        self.__hitbox: pygame.Rect = None
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__title: pygame.Surface = self.__font.render(
            self.__spell.name, True, self.__font_color)
        self.__on_hover_event_listener = None
        self.__on_press_event_listener = None
        self.__on_release_event_listener = None
        self.__on_leave_event_listener = None
        self.__is_mouse_hover: bool = False
    
    def on_hover(self, callback):
        self.__on_hover_event_listener = callback
    def on_press(self, callback):
        self.__on_press_event_listener = callback
    def on_release(self, callback):
        self.__on_release_event_listener = callback
    def on_leave(self, callback):
        self.__on_leave_event_listener = callback
    
    def handle(self, event: pygame.event.Event):
        if (event is not None):
            if (event.type == pygame.MOUSEMOTION):
                if (self.__hitbox is not None):
                    new_mouse_position: tuple[int, int] = pygame.mouse.get_pos()
                    is_hover = self.__hitbox.collidepoint(new_mouse_position)
                    if (is_hover and not self.__is_mouse_hover):
                        if (self.__on_hover_event_listener is not None):
                            self.__on_hover_event_listener(self.__spell)
                    elif (not is_hover and self.__is_mouse_hover):
                        if (self.__on_leave_event_listener is not None):
                            self.__on_leave_event_listener()
                    self.__is_mouse_hover = is_hover
            
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(250,250,250))
        self.__texture.blit(self.__title, (0, 0))
        self.__hitbox = master.blit(self.__texture, (self.__position.x, self.__position.y))

class SlotPanel(InputEventHandler, Draw):
    pass

class ActionPanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.__character: Character = None
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__spells_panels: list[SpellPanel] = []
    
    def on_spell_slot_hover(self, callback):
        for spell_panel in self.__spells_panels:
            spell_panel.on_hover(callback)
    def on_spell_slot_press(self, callback):
        for spell_panel in self.__spells_panels:
            spell_panel.on_press(callback)
    def on_spell_slot_release(self, callback):
        for spell_panel in self.__spells_panels:
            spell_panel.on_release(callback)
    def on_spell_slot_leave(self, callback):
        for spell_panel in self.__spells_panels:
            spell_panel.on_leave(callback)
    
    def set_character(self, character: Character):
        if (character is not None):
            if (character is not self.__character):
                self.__character = character
                self.__spells_panels.clear()
                position: Position = Position(5, 5)
                spell_panel_side_size: int = self.__texture.get_height()-10
                for spell in self.__character.character_class.spells_book.spells:
                    spell_panel: SpellPanel = SpellPanel(spell,width=spell_panel_side_size, height=spell_panel_side_size, position=position)
                    self.__spells_panels.append(spell_panel)
                    position = position.copy()
                    position.x += spell_panel_side_size+10
                
    
    def handle(self, event: pygame.event.Event):
        for spell_panel in self.__spells_panels:
            spell_panel.handle(event)
    
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(50,50,50))
        for spell_panel in self.__spells_panels:
            spell_panel.draw(self.__texture)
        master.blit(self.__texture, (self.__position.x, self.__position.y))

class ExperiencePanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.__character: Character = None
        self.__experience_bar: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__current_experience_bar: pygame.Surface = pygame.Surface((150, 10))
    
    def set_character(self, character: Character):
        if (character is not None):
            if (character is not self.__character):
                self.__character = character
                
    def handle(self, event: pygame.event.Event):
        if (self.__character is not None):
            self.__current_experience_bar = pygame.Surface(((self.__character.level.experience.current*self.__experience_bar.get_width())/100, 10))
    
    def draw(self, master: pygame.Surface):
        self.__experience_bar.fill(pygame.Color(0,0,100))
        self.__current_experience_bar.fill(pygame.Color(0,150,200))
        self.__experience_bar.blit(self.__current_experience_bar, (0,0))
        master.blit(self.__experience_bar, (self.__position.x, self.__position.y))
