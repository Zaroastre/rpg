import pygame
import rpg.constants
from rpg.characters import Character
from rpg.gameplay.classes import Class
from rpg.gameapi import Draw, InputEventHandler
from rpg.math.geometry import Position
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.gameplay.storages import Storage
from rpg.ui.components import CharacterComponent, GroupComponent
from rpg.gamedesign.spells_system import SpellsSet, SpellsWheel
from rpg.gamedesign.message_system import MessageBroker

class SpellDetailPopup(InputEventHandler, Draw):
    def __init__(self, spell: Spell, character_class: Class, width: int, height: int, position: Position) -> None:
        self.__spell: Spell = spell
        self.__character_class: Class = character_class
        self.__border_size: int = 2
        self.__position: Position = position
        self.__background_texture: pygame.Surface = pygame.Surface([width-(self.__border_size*2), height-(self.__border_size*2)], pygame.SRCALPHA)
        self.__border_texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__background_color: pygame.Color = pygame.Color(50, 50, 50)
        self.__border_color: pygame.Color = pygame.Color(200, 200, 200)
        
        self.__title_font_size: int = 25
        self.__text_font_size: int = 20
        self.__title_font: pygame.font.Font = pygame.font.Font(None, self.__title_font_size)
        self.__text_font: pygame.font.Font = pygame.font.Font(None, self.__text_font_size)
        self.__text_font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__description_font_color: pygame.Color = pygame.Color(255, 200, 0)
        
        self.__spell_name: pygame.Surface = self.__title_font.render(self.__spell.name, True, self.__text_font_color)
        self.__spell_damage: pygame.Surface = self.__text_font.render(
            f"Range: {str(self.__spell.magical_effect_minimum)} - {str(self.__spell.magical_effect_maximum)}", True, self.__text_font_color)
        self.__spell_detail: pygame.Surface = self.__text_font.render(
            self.__spell.description, True, self.__description_font_color)
        self.__spell_incantation_duration: pygame.Surface = self.__text_font.render(
            f"Incantation: {str(self.__spell.incantation_duration)}", True, self.__text_font_color)
        self.__spell_cooldown: pygame.Surface = self.__text_font.render(
            f"Cooldown: {str(self.__spell.cooldown)}", True, self.__text_font_color)
        self.__spell_resource: pygame.Surface = self.__text_font.render(
            f"{self.__character_class.resource.resource_type.name.capitalize()}: {str(self.__spell.resource_usage)}", True, self.__text_font_color)
        self.__spell_duration: pygame.Surface = self.__text_font.render(
            f"Duration: {str(self.__spell.effect_duration)}", True, self.__text_font_color)
    
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        self.__background_texture.fill(self.__background_color)
        self.__border_texture.fill(self.__border_color)
        self.__background_texture.blit(self.__spell_name, (0,0))
        self.__background_texture.blit(self.__spell_damage, (0,self.__text_font_size))
        self.__background_texture.blit(self.__spell_resource, (0,self.__text_font_size*2))
        self.__background_texture.blit(self.__spell_duration, (0,self.__text_font_size*3))
        self.__background_texture.blit(self.__spell_incantation_duration, (0,self.__text_font_size*4))
        self.__background_texture.blit(self.__spell_cooldown, (0,(self.__text_font_size*5)))
        self.__background_texture.blit(self.__spell_detail, (0,self.__text_font_size*6))
        self.__border_texture.blit(self.__background_texture, (self.__border_size, self.__border_size))
        master.blit(self.__border_texture, (self.__position.x, self.__position.y))


class LifeGauge(InputEventHandler, Draw):
    def __init__(self, character: Character, width: int, height: int, position: Position) -> None:
        self.__character: Character = character
        self.__height: int = height
        self.__width: int = width
        self.__position: Position = position
        self.__background_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.__background_color: pygame.Color = pygame.Color(30,30,30)
        self.__current_value_texture: pygame.Surface = self.__background_texture.copy()
        self.__font_size: int = 18
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__percent_label: pygame.Surface = self.__font.render(
            str((self.__character.life.current * 100) / self.__character.life.maximum), True, self.__font_color)
        self.__total_label: pygame.Surface = self.__font.render(str(self.__character.life.current if self.__character.life.current < 1000 else str(str(self.__character.life.current/1000)+"k")), True, self.__font_color)


    def handle(self, event: pygame.event.Event):
        percent: float = round((self.__character.life.current * 100) / self.__character.life.maximum, 2)
        self.__percent_label = self.__font.render(f"{str(percent)}%", True, self.__font_color)
        total: str = str(self.__character.life.current) if self.__character.life.current < 1000 else str(str(self.__character.life.current/1000)+"k")
        self.__total_label = self.__font.render(total, True, self.__font_color)
        self.__current_value_texture = pygame.Surface((int((percent*self.__width)/100), self.__height))
    
    def draw(self, master: pygame.Surface):
        margin: int = 5
        self.__background_texture.fill(self.__background_color)
        self.__current_value_texture.fill(self.__character.character_class.class_type.value.color)
        self.__background_texture.blit(self.__current_value_texture, (0,0))
        middle_height: int = (self.__height/2) - (self.__total_label.get_height()/2)
        self.__background_texture.blit(self.__percent_label, (0+margin, middle_height))
        self.__background_texture.blit(self.__total_label, (self.__width-self.__total_label.get_width()-margin, middle_height))
        master.blit(self.__background_texture, (self.__position.x, self.__position.y))

class PowerGauge(InputEventHandler, Draw):
    def __init__(self, character: Character, width: int, height: int, position: Position) -> None:
        self.__character: Character = character
        self.__height: int = height
        self.__width: int = width
        self.__position: Position = position
        self.__background_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.__background_color: pygame.Color = pygame.Color(30,30,30)
        self.__current_value_texture: pygame.Surface = self.__background_texture.copy()
        self.__font_size: int = 18
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__percent_label: pygame.Surface = self.__font.render(
            str((self.__character.character_class.resource.current * 100) / self.__character.character_class.resource.maximum), True, self.__font_color)
        self.__total_label: pygame.Surface = self.__font.render(str(self.__character.character_class.resource.current if self.__character.character_class.resource.current < 1000 else str(str(self.__character.character_class.resource.current/1000)+"k")), True, self.__font_color)


    def handle(self, event: pygame.event.Event):
        percent: float = round((self.__character.character_class.resource.current * 100) / self.__character.character_class.resource.maximum, 2)
        self.__percent_label = self.__font.render(f"{str(percent)}%", True, self.__font_color)
        total: str = str(self.__character.character_class.resource.current) if self.__character.character_class.resource.current < 1000 else str(str(self.__character.character_class.resource.current/1000)+"k")
        self.__total_label = self.__font.render(total, True, self.__font_color)
        self.__current_value_texture = pygame.Surface((int((percent*self.__width)/100), self.__height))
    
    def draw(self, master: pygame.Surface):
        margin: int = 5
        self.__background_texture.fill(self.__background_color)
        self.__current_value_texture.fill(self.__character.character_class.resource.resource_type.value.color)
        self.__background_texture.blit(self.__current_value_texture, (0,0))
        middle_height: int = (self.__height/2) - (self.__total_label.get_height()/2)
        self.__background_texture.blit(self.__percent_label, (0+margin, middle_height))
        self.__background_texture.blit(self.__total_label, (self.__width-self.__total_label.get_width()-margin, middle_height))
        master.blit(self.__background_texture, (self.__position.x, self.__position.y))

class ThreatGauge(InputEventHandler, Draw):
    def __init__(self, character: Character, width: int, height: int, position: Position) -> None:
        self.__character: Character = character
        self.__height: int = height
        self.__width: int = width
        self.__position: Position = position
        self.__background_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.__background_color: pygame.Color = pygame.Color(30,30,30)
        self.__current_value_texture: pygame.Surface = self.__background_texture.copy()
        self.__value_color: pygame.Color = pygame.Color(150,0,0)
        self.__font_size: int = 18
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__percent_label: pygame.Surface = self.__font.render(
            str((self.__character.threat.level * 100) / 100), True, self.__font_color)
        self.__total_label: pygame.Surface = self.__font.render(str(self.__character.threat.level if self.__character.threat.level < 1000 else str(str(self.__character.threat.level/1000)+"k")), True, self.__font_color)


    def handle(self, event: pygame.event.Event):
        percent: float = round((self.__character.threat.level * 100) / 100, 2)
        self.__percent_label = self.__font.render(f"{str(percent)}%", True, self.__font_color)
        total: str = str(self.__character.threat.level) if self.__character.threat.level < 1000 else str(str(self.__character.threat.level/1000)+"k")
        self.__total_label = self.__font.render(total, True, self.__font_color)
        self.__current_value_texture = pygame.Surface((int((percent*self.__width)/100), self.__height))
    
    def draw(self, master: pygame.Surface):
        margin: int = 5
        self.__background_texture.fill(self.__background_color)
        self.__current_value_texture.fill(self.__value_color)
        self.__background_texture.blit(self.__current_value_texture, (0,0))
        middle_height: int = (self.__height/2) - (self.__total_label.get_height()/2)
        self.__background_texture.blit(self.__percent_label, (0+margin, middle_height))
        self.__background_texture.blit(self.__total_label, (self.__width-self.__total_label.get_width()-margin, middle_height))
        master.blit(self.__background_texture, (self.__position.x, self.__position.y))

class Avatar(InputEventHandler, Draw):
    def __init__(self, character: Character, width: int, height: int, position: Position) -> None:
        self.__character: Character = character
        self.__height: int = height
        self.__width: int = width
        self.__position: Position = position
        self.__border_size: int = 5
        self.__background_texture: pygame.Surface = pygame.Surface((self.__width-(self.__border_size*2), self.__height-(self.__border_size*2)))
        self.__background_color: pygame.Color = pygame.Color(30,30,30)
        self.__border_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.__unselected_border_color: pygame.Color = pygame.Color(50,50,50)
        self.__selected_border_color: pygame.Color = pygame.Color(150,255,0)
        

    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        self.__background_texture.fill(self.__background_color)
        if (self.__character.is_selected()):
            self.__border_texture.fill(self.__selected_border_color)
        else:
            self.__border_texture.fill(self.__unselected_border_color)
        self.__border_texture.blit(self.__background_texture, (self.__border_size, self.__border_size))
        master.blit(self.__border_texture, (self.__position.x, self.__position.y))

class FightModeLed(InputEventHandler, Draw):
    def __init__(self, character: Character, radius: float, position: Position) -> None:
        self.__character: Character = character
        self.__height: float = radius*2
        self.__width: float = radius*2
        self.__radius: float = radius
        self.__position: Position = position
        self.__border_size: int = 2
        self.__texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.__border_color: pygame.Color = pygame.Color(75,75,75)
        self.__fight_mode_enabled_background_color: pygame.Color = pygame.Color(255,0,0)
        self.__fight_mode_disabled_background_color: pygame.Color = pygame.Color(100,100,100)
        
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        if (self.__character.is_in_fight_mode):
            pygame.draw.circle(self.__texture, self.__fight_mode_enabled_background_color, (self.__radius, self.__radius), self.__radius)
        else:
            pygame.draw.circle(self.__texture, self.__fight_mode_disabled_background_color, (self.__radius, self.__radius), self.__radius)
        pygame.draw.circle(self.__texture, self.__border_color, (self.__radius, self.__radius), self.__radius, self.__border_size)
        master.blit(self.__texture, (self.__position.x, self.__position.y))

class MemberPanel(InputEventHandler, Draw):
    def __init__(self, member: Character, width: int, height: int, position: Position) -> None:
        self.__member: Character = member
        self.__position: Position = position
        self.__font_size: int = 22
        self.__height: int = height
        self.__width: int = width
        self.__avatar_picture_radius: float = height
        self.__gauge_width: int = (self.__width - (self.__avatar_picture_radius*2))
        self.__texture: pygame.Surface = pygame.Surface([self.__width, self.__avatar_picture_radius*2], pygame.SRCALPHA)
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__pseudo_label: pygame.Surface = self.__font.render(
            self.__member.name, True, self.__font_color)
        
        self.__level_label: pygame.Surface = self.__font.render(
            str(self.__member.level.value), True, self.__font_color)
        
        life_gauge_position: Position = Position(self.__avatar_picture_radius*2,self.__pseudo_label.get_height())
        power_gauge_position: Position = Position(self.__avatar_picture_radius*2, life_gauge_position.y+30)
        threat_gauge_position: Position = Position(self.__avatar_picture_radius*2, power_gauge_position.y+15)
        
        self.__life_gauge: LifeGauge = LifeGauge(self.__member, self.__gauge_width, 30, life_gauge_position)
        self.__power_gauge: PowerGauge = PowerGauge(self.__member, self.__gauge_width, 15, power_gauge_position)
        self.__threat_gauge: ThreatGauge = ThreatGauge(self.__member, self.__gauge_width, 15, threat_gauge_position)
        
        self.__avatar: Avatar = Avatar(self.__member, self.__height*2, self.__height*2, Position(0,0))
        self.__fight_mode_led: FightModeLed = FightModeLed(self.__member, 10, Position(self.__height-10,self.__height+15))
    
    @property
    def height(self) -> float:
        return self.__avatar_picture_radius*2

    def handle(self, event: pygame.event.Event):
        self.__avatar.handle(event)
        self.__fight_mode_led.handle(event)
        self.__life_gauge.handle(event)
        self.__power_gauge.handle(event)
        self.__threat_gauge.handle(event)

    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(20,20,20))
        self.__texture.blit(self.__pseudo_label, (self.height, 0))
        self.__texture.blit(self.__level_label, (self.__width-(self.__level_label.get_width()), 0))

        self.__avatar.draw(self.__texture)
        self.__fight_mode_led.draw(self.__texture)
        self.__life_gauge.draw(self.__texture)
        self.__power_gauge.draw(self.__texture)
        self.__threat_gauge.draw(self.__texture)
        if (self.__member.target is not None):
            pygame.draw.line(master, pygame.Color(255,255,255), (self.__position.x+self.__texture.get_width(), self.__position.y+(self.__texture.get_height()/2)), (self.__member.target.get_position().x, self.__member.target.get_position().y))
        
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
            member_panel_position.y += member_panel.height+10
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

class SpellWheelPanel(InputEventHandler, Draw):
    def __init__(self, spells_wheel: SpellsWheel, width: int, height: int, position: Position) -> None:
        self.__spells_wheel: SpellsWheel = spells_wheel
        self.__width: int = width
        self.__height: int = height
        self.__texture: pygame.Surface = pygame.Surface([self.__width, self.__height], pygame.SRCALPHA)
        self.__labels: list[pygame.Surface] = []
        self.__position: Position = position
        self.__background_color: pygame.Color = pygame.Color(30,30,30)
        self.__font_size: int = 22
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__select_font_color: pygame.Color = pygame.Color(0, 255, 0)
        self.__unselected_font_color: pygame.Color = pygame.Color(150, 150, 150)

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            if (event.type == pygame.JOYHATMOTION and event.value == (1,0)):
                self.__spells_wheel.select_next_set()
            elif (event.type == pygame.JOYHATMOTION and event.value == (-1,0)):
                self.__spells_wheel.select_previous_set()
            elif (event.type == pygame.JOYHATMOTION and event.value == (0,1)):
                self.__spells_wheel.select_previous_set()
            elif (event.type == pygame.JOYHATMOTION and event.value == (0,-1)):
                self.__spells_wheel.select_next_set()
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS):
                self.__spells_wheel.select_next_set()
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHTPAREN):
                self.__spells_wheel.select_previous_set()
        self.__labels.clear()
        for index, spell_set in enumerate(self.__spells_wheel.sets):
            label: pygame.Surface
            if (spell_set.is_selected):
                label = self.__font.render(str(index+1), True, self.__select_font_color)
            else:
                label = self.__font.render(str(index+1), True, self.__unselected_font_color)
            self.__labels.append(label)

    def draw(self, master: pygame.Surface):
        self.__texture.fill(self.__background_color)
        y: int = 0
        for label in self.__labels:
            self.__texture.blit(label, ((self.__width/2)-(label.get_width()/2), y))
            y += label.get_height()+5
        master.blit(self.__texture, (self.__position.x, self.__position.y))
    
class SpellSlot(InputEventHandler, Draw):
    def __init__(self, spell: Spell, width: int, height: int, position: Position) -> None:
        self.__spell: Spell = spell
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__font_size: int = 22
        self.__hitbox: pygame.Rect = None
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__spell_color: pygame.Color = pygame.Color(225, 225, 225)
        self.__empty_color: pygame.Color = pygame.Color(100, 100, 100)
        self.__title: pygame.Surface = None
        if (self.__spell is not None):
            self.__font.render(
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
        if (self.__spell is None):
            self.__texture.fill(self.__empty_color)
        else:
            self.__texture.fill(self.__spell_color)
        if (self.__title is not None):
            self.__texture.blit(self.__title, (0, 0))
        self.__hitbox = master.blit(self.__texture, (self.__position.x, self.__position.y))

class StorageSlot(InputEventHandler, Draw):
    def __init__(self, storage: Storage, width: int, height: int, position: Position) -> None:
        self.__storage: Storage = storage
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 22
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__storage_color: pygame.Color = pygame.Color(225, 225, 225)
        self.__empty_color: pygame.Color = pygame.Color(100, 100, 100)
        self.__title: pygame.Surface = None
        if (self.__storage is not None):
            self.__font.render(
                self.__storage.name, True, self.__font_color)
            
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
                            self.__on_hover_event_listener(self.__storage)
                    elif (not is_hover and self.__is_mouse_hover):
                        if (self.__on_leave_event_listener is not None):
                            self.__on_leave_event_listener()
                    self.__is_mouse_hover = is_hover
            
    def draw(self, master: pygame.Surface):
        if (self.__storage is None):
            self.__texture.fill(self.__empty_color)
        else:
            self.__texture.fill(self.__storage_color)
        if (self.__title is not None):
            self.__texture.blit(self.__title, (0, 0))
        self.__hitbox = master.blit(self.__texture, (self.__position.x, self.__position.y))


class ActionPanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.__character: Character = None
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__spells_panels: list[SpellPanel] = []
        self.__spells_wheel: SpellsWheel = SpellsWheel(4, 4)
        self.__spells_slots: list[SpellSlot] = []
        self.__storages_slots: list[StorageSlot] = []
        self.__spell_wheel_panel: SpellWheelPanel = SpellWheelPanel(self.__spells_wheel, 15, height, Position(0,0))
    
    def on_spell_slot_hover(self, callback):
        for slot in self.__spells_slots:
            slot.on_hover(callback)
    def on_spell_slot_press(self, callback):
        for slot in self.__spells_slots:
            slot.on_press(callback)
    def on_spell_slot_release(self, callback):
        for slot in self.__spells_slots:
            slot.on_release(callback)
    def on_spell_slot_leave(self, callback):
        for slot in self.__spells_slots:
            slot.on_leave(callback)
    
    
    def on_storage_slot_hover(self, callback):
        for slot in self.__storages_slots:
            slot.on_hover(callback)
    def on_storage_slot_press(self, callback):
        for slot in self.__storages_slots:
            slot.on_press(callback)
    def on_storage_slot_release(self, callback):
        for slot in self.__storages_slots:
            slot.on_release(callback)
    def on_storage_slot_leave(self, callback):
        for slot in self.__storages_slots:
            slot.on_leave(callback)
    
    def __update_spells_slots(self):
        position: Position = Position(5+15, 5)
        spell_panel_side_size: int = self.__texture.get_height()-10
        self.__spells_slots.clear()
        spells_set: SpellsSet = self.__spells_wheel.get_selected_set()
        for potential_spell in spells_set.list():
            slot: SpellSlot = SpellSlot(potential_spell, spell_panel_side_size, spell_panel_side_size, position)
            self.__spells_slots.append(slot)
            position = position.copy()
            position.x += spell_panel_side_size+10

    def __update_storages_slots(self):
        storage_panel_side_size: int = self.__texture.get_height()-10
        position: Position = Position((self.__texture.get_width()-(self.__texture.get_height()*(len(self.__character.storages)))), 5)
        self.__storages_slots.clear()
        for storage in self.__character.storages:
            slot: StorageSlot = StorageSlot(storage, storage_panel_side_size, storage_panel_side_size, position)
            self.__storages_slots.append(slot)
            position = position.copy()
            position.x += storage_panel_side_size+10
            
    def set_character(self, character: Character):
        if (character is not None):
            if (character is not self.__character):
                self.__character = character
                self.__update_spells_slots()
                self.__update_storages_slots()

    def set_spells_wheel(self, spells_wheel: SpellsWheel):
        if (spells_wheel is not None):
            if (spells_wheel is not self.__spells_wheel):
                self.__spells_wheel = spells_wheel
                self.__update_spells_slots()

    def handle(self, event: pygame.event.Event):
        self.__spell_wheel_panel.handle(event)
        for slot in self.__spells_slots:
            slot.handle(event)
        for slot in self.__storages_slots:
            slot.handle(event)
    
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(50,50,50))
        self.__spell_wheel_panel.draw(self.__texture)
        for slot in self.__spells_slots:
            slot.draw(self.__texture)
        for slot in self.__storages_slots:
            slot.draw(self.__texture)
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
            width: int = (self.__character.level.experience.current*self.__experience_bar.get_width())/self.__character.level.experience.maximum
            height: int = 10
            self.__current_experience_bar = pygame.Surface((width, height))
    
    def draw(self, master: pygame.Surface):
        self.__experience_bar.fill(pygame.Color(0,0,100))
        self.__current_experience_bar.fill(pygame.Color(255,0,255))
        self.__experience_bar.blit(self.__current_experience_bar, (0,0))
        master.blit(self.__experience_bar, (self.__position.x, self.__position.y))

class MessagePanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.__panel: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        self.__messages: list[str] = []
        self.__font_size: int = 20
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__total_characters_per_line: int = 0
        self.__maximum_lines: int = 0
        self.__message_broker: MessageBroker = MessageBroker()

    def __retrieve_new_messages(self):
        new_messages: list[str] = self.__message_broker.get_debug_message()
        if (new_messages is not None and len(new_messages) > 0):
            for new_message in new_messages:
                self.__messages.append(new_message)
                if (len(self.__messages) > self.__maximum_lines):
                    self.__messages.pop(0)
        new_message = self.__message_broker.get_system_message()
        if (new_messages is not None and len(new_messages) > 0):
            for new_message in new_messages:
                self.__messages.append(new_message)
                if (len(self.__messages) > self.__maximum_lines):
                    self.__messages.pop(0)

    def handle(self, event: pygame.event.Event):
        if (self.__total_characters_per_line == 0):
            message: str = "Hello World from NEMESYS and this is a very long message for testing to display a long message on the panel"
            label_text: pygame.Surface = pygame.Surface((0,0))
            while (label_text.get_width() < self.__panel.get_width()):
                label_text = self.__font.render(str(message[:self.__total_characters_per_line]), True, self.__font_color)
                self.__total_characters_per_line += 1
            self.__maximum_lines = int(self.__panel.get_height()/label_text.get_height())-1
            self.__total_characters_per_line -= 1
        self.__retrieve_new_messages()

    def draw(self, master: pygame.Surface):
        self.__panel.fill(pygame.Color(50,50,50))
        lines: list[str] = []
        max_lines: int = int(self.__panel.get_height()/self.__font_size)
        for message in self.__messages:
            line_size: int = 0
            label_text: str = ""
            for character in message:
                if (len(label_text) == self.__total_characters_per_line):
                    lines.append(label_text)
                    label_text = ""
                    line_size = 0
                line_size += self.__font_size
                label_text += character
                if (len(lines) >= max_lines):
                    lines.pop(0)
        
            lines.append(label_text)
            label_text = ""
            if (len(lines) > max_lines):
                lines.pop(0)
        line_position_y = 0
        for line in lines:
            self.__panel.blit(self.__font.render(line, True, self.__font_color), (0, line_position_y))
            line_position_y += self.__font_size
        
        master.blit(self.__panel, (self.__position.x, self.__position.y))
