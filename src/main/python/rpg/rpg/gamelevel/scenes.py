from abc import ABC
from math import cos, pi, radians, sin, sqrt
from random import uniform

import pygame
import rpg.constants
from rpg.characters import Character, Enemy, Projectil
from rpg.configuration import Configuration
from rpg.gameapi import Draw, InputEventHandler
from rpg.gamedesign.difficulty_system import Difficulty
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.fight_system import Fight
from rpg.gamedesign.interval_system import Range
from rpg.gamedesign.message_system import MessageBroker
from rpg.gamengine import GameGenerator
from rpg.gameplay.breeds import BreedFactory, BreedType
from rpg.gameplay.classes import ClassFactory, ClassType
from rpg.gameplay.genders import Gender
from rpg.gameplay.player import Player
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry, Position
from rpg.ui.components import (CharacterComponent, EnemyComponent,
                               ProjectilComponent)
from rpg.ui.graphics import (ActionPanel, ExperiencePanel, GroupPanel,
                             MessagePanel, SpellDetailPopup)


class Scene(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, player: Player) -> None:
        self.__player: Player = player
        self.__width: int = width
        self.__height: int = height
        self._background_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
    
    @property
    def width(self) -> Player:
        return self.__width
    @property
    def height(self) -> Player:
        return self.__height
    @property
    def player(self) -> Player:
        return self.__player
    
    def draw(self, master: pygame.Surface):
        master.blit(self._background_texture, (0,0))

class MainMenuScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        self.__options: dict[str, callable] = {}
        self.__options["continue"] = self.__continue_game
        self.__options["new game"] = self.__create_new_game
        self.__options["options"] = self.__configure_options
        self.__options["help"] = self.__show_help
        self.__options["exit"] = self.__quit_game
        
        self.__background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__buttons: list[pygame.Rect] = []
        self.__button_border_size: int = 5
        self.__button_font_size: int = 22
        self.__button_font: pygame.font.Font = pygame.font.Font(None, self.__button_font_size)
        self.__button_font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__button_border_color: pygame.Color = pygame.Color(255, 0, 0)
        self.__unselected_button_background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__selected_button_background_color: pygame.Color = self.__button_border_color
        self.__selected_option: str = list(self.__options.keys())[0]
        self.__on_continue_game_event_listener: callable = None
        self.__on_create_new_game_event_listener: callable = None
        self.__on_configure_options_event_listener: callable = None
        self.__on_show_help_event_listener: callable = None
        self.__on_exit_game_event_listener: callable = None
    
    def set_event_listener_on_continue_game(self, callback: callable):
        self.__on_continue_game_event_listener = callback
    
    def set_event_listener_on_create_new_game(self, callback: callable):
        self.__on_create_new_game_event_listener = callback
    
    def set_event_listener_on_configure_options(self, callback: callable):
        self.__on_configure_options_event_listener = callback
    
    def set_event_listener_on_show_help(self, callback: callable):
        self.__on_show_help_event_listener = callback
    
    def set_event_listener_on_exit_game(self, callback: callable):
        self.__on_exit_game_event_listener = callback
    
    def __continue_game(self):
        if (self.__on_continue_game_event_listener is not None):
            self.__on_continue_game_event_listener()
    
    def __create_new_game(self):
        if (self.__on_create_new_game_event_listener is not None):
            self.__on_create_new_game_event_listener()
    
    def __configure_options(self):
        if (self.__on_configure_options_event_listener is not None):
            self.__on_configure_options_event_listener()
    
    def __show_help(self):
        if (self.__on_show_help_event_listener is not None):
            self.__on_show_help_event_listener()
    
    def __quit_game(self):
        if (self.__on_exit_game_event_listener is not None):
            self.__on_exit_game_event_listener()
    
    def __select_next_option(self):
        options: list[str] = list(self.__options.keys())
        index: int = options.index(self.__selected_option)
        if (index+1 <= len(options)-1):
            self.__selected_option = options[index+1]
        else:
            self.__selected_option = options[0]
    
    def __select_previous_option(self):
        options: list[str] = list(self.__options.keys())
        index: int = options.index(self.__selected_option)
        if (index-1 >= 0):
            self.__selected_option = options[index-1]
        else:
            self.__selected_option = options[-1]
    
    def __launch_option(self):
        callback: callable = self.__options.get(self.__selected_option)
        if (callback is not None):
            callback()
    
    def __handle_keyboard_event(self, event: pygame.event.Event):
        if (event is not None):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                self.__select_next_option()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                self.__select_previous_option()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self.__launch_option()
                
    def __handle_gamepad_event(self, event: pygame.event.Event):
        if (event is not None):
            if(event.type == pygame.JOYHATMOTION and event.value == (0,1)):
                self.__select_previous_option()
            elif(event.type == pygame.JOYHATMOTION and event.value == (0,-1)):
                self.__select_next_option()
            elif (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
                self.__launch_option()
    
    def handle(self, event: pygame.event.Event):
        if (event is not None):
            self.__handle_keyboard_event(event)
            self.__handle_gamepad_event(event)
            
    def draw(self, master: pygame.Surface):
        self._background_texture.fill(self.__background_color)
        
        self.__buttons.clear()
        buttons_texts: list[str] = list(self.__options.keys())
        button_space_height: int = 20
        
        button_width: int = 200
        button_height: int = 50
        buttons_panel: pygame.Surface = pygame.Surface((button_width, ((button_height * len(buttons_texts)) + button_space_height * (len(buttons_texts)-1))))
        # position: Position = Position(self.__button_margin_width, self.__button_margin_height)
        button_position_y: int = 0
        button_border_size: int = 5
        for text in buttons_texts:
            button: pygame.Surface = pygame.Surface((button_width, button_height))
            button_border: pygame.Surface = button.copy()
            button_background: pygame.Surface = pygame.Surface((button_width - (button_border_size*2), button_height - (button_border_size*2)))
            if (text == self.__selected_option):
                button_background.fill(self.__selected_button_background_color)
            else:
                button_background.fill(self.__unselected_button_background_color)
            label: pygame.Surface = self.__button_font.render(text.title(), True, self.__button_font_color)
            label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
            button_background.blit(label, (label_position_x, label_position_y))
            button_border.fill(self.__button_border_color)
            button_border.blit(button_background, (self.__button_border_size, self.__button_border_size))
            button.blit(button_border, (0,0))
            # buttons_panel.blit(self.__button_texture, (0, 0))
            buttons_panel.blit(button, (0, button_position_y))
            button_position_y += (button_height + button_space_height)
            
        self._background_texture.blit(buttons_panel, ((self.width/2)-(buttons_panel.get_width()/2), (self.height/2)-(buttons_panel.get_height()/2)))
        super().draw(master)

class PauseMenuScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)

    def handle(self, event: pygame.event.Event):
        return super().handle(event)
    
    def draw(self, master: pygame.Surface):
        super().draw(master)

class CharacterCreationScreen(Scene):
    __GENDER_KEY: str = "gender"
    __FACTION_KEY: str = "faction"
    __BREED_KEY: str = "breed"
    __CLASS_KEY: str = "class"
    __NAME_KEY: str = "name"
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        self.__button_font_size: int = 22
        self.__button_character_selector_font_size: int = 50
        self.__button_font: pygame.font.Font = pygame.font.Font(None, self.__button_font_size)
        self.__button_character_selector_font: pygame.font.Font = pygame.font.Font(None, self.__button_character_selector_font_size)
        self.__button_font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__button_border_color: pygame.Color = pygame.Color(255, 0, 0)
        self.__unselected_button_background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__selected_button_background_color: pygame.Color = self.__button_border_color
        self.__maximum_character: int = 5
        self.__characters_configurations: list[dict[str, object]] = []
        for _ in range(self.__maximum_character):
            self.__characters_configurations.append(None)
        self.__selected_slot_index: int = 0
        self.__hover_slot_index: int = 0
        
        self.__selected_gender_index: int = 0
        self.__selected_faction_index: int = 0
        self.__selected_breed_index: int = 0
        self.__selected_class_index: int = 0
        
        selected_configuration: dict[str, object] = {}
        selected_configuration[CharacterCreationScreen.__BREED_KEY]=None
        selected_configuration[CharacterCreationScreen.__CLASS_KEY]=None
        selected_configuration[CharacterCreationScreen.__GENDER_KEY]=None
        selected_configuration[CharacterCreationScreen.__NAME_KEY]=None
        selected_configuration[CharacterCreationScreen.__FACTION_KEY]=None
        self.__characters_configurations[self.__selected_slot_index] = selected_configuration
        self.__is_selecting_gender: bool = False
        self.__is_selecting_faction: bool = False
        self.__is_selecting_breed: bool = False
        self.__is_selecting_class: bool = False
        self.__is_selecting_slot: bool = True
        self.__is_selecting_back: bool = False
        self.__is_selecting_play: bool = False
        
        self.__on_back_event_listener: callable = None
        self.__on_play_event_listener: callable = None

    def set_event_listener_on_back(self, callback: callable):
        self.__on_back_event_listener = callback
    
    def set_event_listener_on_play(self, callback: callable):
        self.__on_play_event_listener = callback
    
    
    def __select_next_character(self):
        if (self.__is_selecting_slot):
            if (self.__hover_slot_index+1 < self.__maximum_character):
                self.__hover_slot_index += 1
            else:
                self.__is_selecting_play = True
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_breed = False
                self.__is_selecting_class = False
                self.__is_selecting_faction = False
                self.__is_selecting_gender = False
    def __select_next_gender(self):
        if (self.__is_selecting_gender):
            if (self.__selected_gender_index+1 < len(Gender)):
                self.__selected_gender_index += 1
            else:
                self.__is_selecting_gender = False
                self.__is_selecting_class = True
                
                
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_breed = False
                self.__is_selecting_faction = False
    def __select_previous_gender(self):
        if (self.__is_selecting_gender):
            if (self.__selected_gender_index-1 >= 0):
                self.__selected_gender_index -= 1
            else:
                self.__is_selecting_gender = False
                self.__is_selecting_breed = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_class = False
                self.__is_selecting_faction = False

    def __select_next_faction(self):
        if (self.__is_selecting_faction):
            if (self.__selected_faction_index+1 < len(Faction)):
                self.__selected_faction_index += 1
            else:
                self.__is_selecting_gender = False
                self.__is_selecting_class = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_breed = False
                self.__is_selecting_faction = False
    def __select_previous_faction(self):
        if (self.__is_selecting_faction):
            if (self.__selected_faction_index-1 >= 0):
                self.__selected_faction_index -= 1
            else:
                self.__is_selecting_gender = False
                self.__is_selecting_breed = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_class = False
                self.__is_selecting_faction = False
    
    def __select_next_breed(self):
        if (self.__is_selecting_breed):
            if (self.__selected_breed_index+1 < len(BreedType)):
                self.__selected_breed_index += 1
            else:
                self.__is_selecting_breed = False
                self.__is_selecting_back = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_class = False
                self.__is_selecting_faction = False
                self.__is_selecting_gender = False
    def __select_previous_breed(self):
        if (self.__is_selecting_breed):
            if (self.__selected_breed_index-1 >= 0):
                self.__selected_breed_index -= 1
            else:
                self.__is_selecting_breed = False
                self.__is_selecting_faction = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_class = False
                self.__is_selecting_gender = False


    def __select_next_class(self):
        if (self.__is_selecting_class):
            if (self.__selected_class_index+1 < len(ClassType)):
                self.__selected_class_index += 1
            else:
                self.__is_selecting_class = False
                self.__is_selecting_play = True
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_breed = False
                self.__is_selecting_faction = False
                self.__is_selecting_gender = False
    def __select_previous_class(self):
        if (self.__is_selecting_class):
            if (self.__selected_class_index-1 >= 0):
                self.__selected_class_index -= 1
            else:
                self.__is_selecting_class = False
                self.__is_selecting_faction = True
                self.__is_selecting_play = False
                self.__is_selecting_slot = False
                self.__is_selecting_back = False
                self.__is_selecting_breed = False
                self.__is_selecting_gender = False

    def __select_previous_character(self):
        if (self.__is_selecting_slot):
            if (self.__hover_slot_index-1 >= 0):
                self.__hover_slot_index -= 1
            else:
                self.__is_selecting_slot = False
                self.__is_selecting_back = True
                self.__is_selecting_play = False
                self.__is_selecting_breed = False
                self.__is_selecting_class = False
                self.__is_selecting_faction = False
                self.__is_selecting_gender = False

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                if (self.__is_selecting_back):
                    self.__is_selecting_back = False
                    self.__is_selecting_slot = True
                elif(self.__is_selecting_breed):
                    self.__is_selecting_breed = False
                    self.__is_selecting_class = True
                else:
                    self.__select_next_character()
                    self.__select_next_gender()
                    self.__select_next_faction()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                if (self.__is_selecting_play):
                    self.__is_selecting_play = False
                    self.__is_selecting_slot = True
                elif(self.__is_selecting_class):
                    self.__is_selecting_class = False
                    self.__is_selecting_breed = True
                else:
                    self.__select_previous_character()
                    self.__select_previous_gender()
                    self.__select_previous_faction()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                if (self.__is_selecting_play):
                    self.__is_selecting_play = False
                    self.__is_selecting_class = True
                    self.__selected_class_index = len(list(ClassType))-1
                elif (self.__is_selecting_faction):
                    self.__is_selecting_faction = False
                    self.__is_selecting_gender = True
                elif (self.__is_selecting_back):
                    self.__is_selecting_back = False
                    self.__is_selecting_breed = True
                    self.__selected_breed_index = len(list(BreedType))-1
                elif (self.__is_selecting_slot):
                    self.__is_selecting_slot = False
                    self.__is_selecting_faction = True
                else:
                    self.__select_previous_breed()
                    self.__select_previous_class()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                if (self.__is_selecting_gender):
                    self.__is_selecting_gender = False
                    self.__is_selecting_faction = True
                elif (self.__is_selecting_faction):
                    self.__is_selecting_faction = False
                    self.__is_selecting_slot = True
                else:
                    self.__select_next_breed()
                    self.__select_next_class()

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                if (self.__is_selecting_gender):
                    self.__characters_configurations[self.__selected_slot_index][CharacterCreationScreen.__GENDER_KEY] = list(Gender)[self.__selected_gender_index]
                elif (self.__is_selecting_faction):
                    self.__characters_configurations[self.__selected_slot_index][CharacterCreationScreen.__FACTION_KEY] = list(Faction)[self.__selected_faction_index]
                elif (self.__is_selecting_class):
                    self.__characters_configurations[self.__selected_slot_index][CharacterCreationScreen.__CLASS_KEY] = list(ClassType)[self.__selected_class_index]
                elif (self.__is_selecting_breed):
                    self.__characters_configurations[self.__selected_slot_index][CharacterCreationScreen.__BREED_KEY] = list(BreedType)[self.__selected_breed_index]
                elif (self.__is_selecting_play):
                    characters: list[Character] = []
                    for configuration in self.__characters_configurations:
                        if (configuration is not None):
                            name: str = configuration.get(CharacterCreationScreen.__NAME_KEY)
                            faction: Faction = configuration.get(CharacterCreationScreen.__FACTION_KEY)
                            breed: BreedType = configuration.get(CharacterCreationScreen.__BREED_KEY)
                            gender: Gender = configuration.get(CharacterCreationScreen.__GENDER_KEY)
                            character_class: ClassType = configuration.get(CharacterCreationScreen.__CLASS_KEY)
                            
                            if (faction is not None):
                                if (breed is not None):
                                    if (gender is not None):
                                        if (character_class is not None):
                                            if (name is None):
                                                name = GameGenerator.generate_random_name(gender)
                                            
                                            character: Character = GameGenerator.create_friend(name, BreedFactory.create(breed), ClassFactory.create(character_class), gender, faction)
                                            characters.append(character)
                    if (len(characters) > 0):
                        if (self.__on_play_event_listener is not None):
                            self.__on_play_event_listener(characters)
                elif (self.__is_selecting_back):
                    if (self.__on_back_event_listener is not None):
                        self.__on_back_event_listener()
                elif (self.__is_selecting_slot):
                    self.__selected_slot_index = self.__hover_slot_index
                    if (self.__characters_configurations[self.__selected_slot_index] is None):
                        selected_configuration: dict[str, object] = {}
                        selected_configuration[CharacterCreationScreen.__BREED_KEY]=None
                        selected_configuration[CharacterCreationScreen.__CLASS_KEY]=None
                        selected_configuration[CharacterCreationScreen.__GENDER_KEY]=None
                        selected_configuration[CharacterCreationScreen.__NAME_KEY]=None
                        selected_configuration[CharacterCreationScreen.__FACTION_KEY]=None
                        self.__characters_configurations[self.__selected_slot_index] = selected_configuration
    def __draw_genders_buttons(self, master: pygame.Surface):
        space_between_each_buttons: int = 50
        button_width: int = 100
        button_height: int = 50
        genders: list[Gender] = list(Gender)
        buttons_panel: pygame.Surface = pygame.Surface((((button_width*len(genders))+space_between_each_buttons), button_height))
        button_position_x: int = 0
        for index, gender in enumerate(genders):
            button: pygame.Surface = pygame.Surface((button_width, button_height))
            button_border_size: int = 5
            button_border: pygame.Surface = button.copy()
            button_border.fill(self.__button_border_color)
            button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
            label: pygame.Surface = self.__button_font.render(gender.name.capitalize(), True, self.__button_font_color)
            label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
            if (self.__is_selecting_gender):
                if (index == self.__selected_gender_index):
                    button_background.fill(self.__selected_button_background_color)
            configuration: dict[str, object] = self.__characters_configurations[self.__selected_slot_index]
            if (configuration is not None and configuration.get(CharacterCreationScreen.__GENDER_KEY) is gender):
                button_background.fill(pygame.Color(255,150,0))
            button_background.blit(label, (label_position_x, label_position_y))
            button_border.blit(button_background, (button_border_size, button_border_size))
            button.blit(button_border, (0,0))
            buttons_panel.blit(button, (button_position_x, 0))
            button_position_x += (button_width + space_between_each_buttons)
        self._background_texture.blit(buttons_panel, (((self.width/2)-(buttons_panel.get_width()/2)), 0))

    def __draw_factions_buttons(self, master: pygame.Surface):
        space_between_each_buttons: int = 50
        button_width: int = 100
        button_height: int = 50
        factions: list[Faction] = list(Faction)
        buttons_panel: pygame.Surface = pygame.Surface((((button_width*len(factions))+(space_between_each_buttons*(len(factions)-1))), button_height))
        button_position_x: int = 0
        for index, faction in enumerate(factions):
            button: pygame.Surface = pygame.Surface((button_width, button_height))
            button_border_size: int = 5
            button_border: pygame.Surface = button.copy()
            button_border.fill(self.__button_border_color)
            button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
            label: pygame.Surface = self.__button_font.render(faction.name.capitalize(), True, self.__button_font_color)
            label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
            if (self.__is_selecting_faction):
                if (index == self.__selected_faction_index):
                    button_background.fill(self.__selected_button_background_color)
            configuration: dict[str, object] = self.__characters_configurations[self.__selected_slot_index]
            if (configuration is not None and configuration.get(CharacterCreationScreen.__FACTION_KEY) is faction):
                button_background.fill(pygame.Color(255,150,0))
            button_background.blit(label, (label_position_x, label_position_y))
            button_border.blit(button_background, (button_border_size, button_border_size))
            button.blit(button_border, (0,0))
            buttons_panel.blit(button, (button_position_x, 0))
            button_position_x += (button_width + space_between_each_buttons)
        self._background_texture.blit(buttons_panel, (((self.width/2)-(buttons_panel.get_width()/2)), 100))

    def __draw_breeds_buttons(self, master: pygame.Surface):
        space_between_each_buttons: int = 10
        button_width: int = 120
        button_height: int = 50
        breeds: list[BreedType] = list(BreedType)
        buttons_panel: pygame.Surface = pygame.Surface((button_width, ((button_height*len(breeds))+(space_between_each_buttons*(len(breeds)-1)))))
        button_position_y: int = 0
        for index, breed in enumerate(breeds):
            button: pygame.Surface = pygame.Surface((button_width, button_height))
            button_border_size: int = 5
            button_border: pygame.Surface = button.copy()
            button_border.fill(self.__button_border_color)
            button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
            text: str = breed.name.replace("_", " ").title()
            label: pygame.Surface = self.__button_font.render(text, True, self.__button_font_color)
            label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
            if (self.__is_selecting_breed):
                if (index == self.__selected_breed_index):
                    button_background.fill(self.__selected_button_background_color)
            configuration: dict[str, object] = self.__characters_configurations[self.__selected_slot_index]
            if (configuration is not None and configuration.get(CharacterCreationScreen.__BREED_KEY) is breed):
                button_background.fill(pygame.Color(255,150,0))
            button_background.blit(label, (label_position_x, label_position_y))
            button_border.blit(button_background, (button_border_size, button_border_size))
            button.blit(button_border, (0,0))
            buttons_panel.blit(button, (0, button_position_y))
            button_position_y += (button_height + space_between_each_buttons)
        self._background_texture.blit(buttons_panel, (0, (self.height/2)-(buttons_panel.get_height()/2)))

    def __draw_classes_buttons(self, master: pygame.Surface):
        space_between_each_buttons: int = 10
        button_width: int = 120
        button_height: int = 50
        classes: list[ClassType] = list(ClassType)
        buttons_panel: pygame.Surface = pygame.Surface((button_width, ((button_height*len(classes))+(space_between_each_buttons*(len(classes)-1)))))
        button_position_y: int = 0
        for index, class_type in enumerate(classes):
            button: pygame.Surface = pygame.Surface((button_width, button_height))
            button_border_size: int = 5
            button_border: pygame.Surface = button.copy()
            button_border.fill(self.__button_border_color)
            button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
            text: str = class_type.name.replace("_", " ").title()
            label: pygame.Surface = self.__button_font.render(text, True, class_type.value.color)
            label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
            if (self.__is_selecting_class):
                if (index == self.__selected_class_index):
                    button_background.fill(self.__selected_button_background_color)
            configuration: dict[str, object] = self.__characters_configurations[self.__selected_slot_index]
            if (configuration is not None and configuration.get(CharacterCreationScreen.__CLASS_KEY) is class_type):
                button_background.fill(pygame.Color(255,150,0))
            button_background.blit(label, (label_position_x, label_position_y))
            button_border.blit(button_background, (button_border_size, button_border_size))
            button.blit(button_border, (0,0))
            buttons_panel.blit(button, (0, button_position_y))
            button_position_y += (button_height + space_between_each_buttons)
        self._background_texture.blit(buttons_panel, (self.width-buttons_panel.get_width(), (self.height/2)-(buttons_panel.get_height()/2)))
      
    def __draw_characters_slots_buttons(self, master: pygame.Surface):
        space_between_each_buttons: int = 50
        button_size: int = 50
        buttons_panel: pygame.Surface = pygame.Surface((((button_size*self.__maximum_character)+(space_between_each_buttons*(self.__maximum_character-1))), button_size))
        button_position_x: int = 0
        for index in range(self.__maximum_character):
            button: pygame.Surface = pygame.Surface((button_size, button_size))
            button_border_size: int = 5 if self.__characters_configurations[index] is not None else 2
            button_border: pygame.Surface = button.copy()
            button_border.fill(self.__button_border_color)
            button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
            if (index != self.__hover_slot_index):
                if (self.__characters_configurations[index] is None):
                    label: pygame.Surface = self.__button_font.render("0/1", True, self.__button_font_color)
                    label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
                    label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
                    button_background.blit(label, (label_position_x, label_position_y))
                else:
                    button_background.fill(pygame.Color(255,150,0))
            else:
                if (self.__is_selecting_slot):
                    button_background.fill(pygame.Color(255,0,0))
                if (self.__characters_configurations[index] is None):
                    label: pygame.Surface = self.__button_font.render("1/1", True, self.__button_font_color)
                    label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
                    label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
                    button_background.blit(label, (label_position_x, label_position_y))
            button_border.blit(button_background, (button_border_size, button_border_size))
            button.blit(button_border, (0,0))
            buttons_panel.blit(button, (button_position_x, 0))
            button_position_x += (button_size + space_between_each_buttons)
        self._background_texture.blit(buttons_panel, (((self.width/2)-(buttons_panel.get_width()/2)), (self.height - buttons_panel.get_height())))
    
    def __draw_back_button(self, master: pygame.Surface):
        button: pygame.Surface = pygame.Surface((100, 50))
        button_border_size: int = 5
        button_border: pygame.Surface = button.copy()
        button_border.fill(self.__button_border_color)
        button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
        label: pygame.Surface = self.__button_font.render("Back", True, self.__button_font_color)
        label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
        label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
        if (self.__is_selecting_back):
            button_background.fill(self.__selected_button_background_color)
        else:
            button_background.fill(self.__unselected_button_background_color)
        button_background.blit(label, (label_position_x, label_position_y))
        button_border.blit(button_background, (button_border_size, button_border_size))
        button.blit(button_border, (0,0))
        self._background_texture.blit(button, (0, self.height - button.get_height()))
    
    def __draw_play_button(self, master: pygame.Surface):
        button: pygame.Surface = pygame.Surface((100, 50))
        button_border_size: int = 5
        button_border: pygame.Surface = button.copy()
        button_border.fill(self.__button_border_color)
        button_background: pygame.Surface = pygame.Surface((button.get_width()-(button_border_size*2), button.get_height()-(button_border_size*2)))
        label: pygame.Surface = self.__button_font.render("Play", True, self.__button_font_color)
        label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
        label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
        if (self.__is_selecting_play):
            button_background.fill(self.__selected_button_background_color)
        else:
            button_background.fill(self.__unselected_button_background_color)
        button_background.blit(label, (label_position_x, label_position_y))
        button_border.blit(button_background, (button_border_size, button_border_size))
        button.blit(button_border, (0,0))
        self._background_texture.blit(button, ((self.width-button.get_width()), (self.height - button.get_height())))
        
    def draw(self, master: pygame.Surface):
        self.__draw_genders_buttons(master)
        self.__draw_factions_buttons(master)
        self.__draw_breeds_buttons(master)
        self.__draw_classes_buttons(master)
        self.__draw_characters_slots_buttons(master)
        self.__draw_back_button(master)
        self.__draw_play_button(master)
        super().draw(master)

class GameScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        
        self.__action_panel: ActionPanel = ActionPanel(rpg.constants.ACTION_PANEL_WIDTH, rpg.constants.ACTION_PANEL_HEIGHT, rpg.constants.ACTION_PANEL_POSITION)
        self.__experience_panel: ExperiencePanel = ExperiencePanel(rpg.constants.EXPERIENCE_PANEL_WIDTH, rpg.constants.EXPERIENCE_PANEL_HEIGHT, rpg.constants.EXPERIENCE_PANEL_POSITION)
        self.__friends_group: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__friends_group, width=rpg.constants.GROUP_PANEL_WIDTH, height=rpg.constants.GROUP_PANEL_HEIGHT, position=rpg.constants.GROUP_PANEL_POSITION)
        self.__message_panel: MessagePanel = MessagePanel(width=rpg.constants.MESSAGE_PANEL_WIDTH, height=rpg.constants.MESSAGE_PANEL_HEIGHT, position=rpg.constants.MESSAGE_PANEL_POSITION)

        self.__friends_sprites: list[CharacterComponent] = []
        self.__enemies_sprites: list[EnemyComponent] = []
        
        self.__spell_detail_popup: SpellDetailPopup = None
        self.__message_broker: MessageBroker = MessageBroker()
        
        self.__fights: dict[Character, Fight] = {}
        
        self.__generate_enemies()
        self.__initialize_events_listeners()
        

    def set_friends_group(self, friends: list[Character]):
        if (len(friends) > 0):
            player: Character = friends[0]
            player.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            player.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            player.select()
            player.threat.increase(20.0)
            self.__friends_group.add_member(player)
            self.player.set_character(player)
            self.__friends_sprites.append(CharacterComponent(player))
            for friend in friends:
                if (friend is not player):
                    self.__friends_group.add_member(friend)
                    self.__friends_sprites.append(CharacterComponent(friend))

    def __initialize_events_listeners(self):
        self.__action_panel.on_spell_slot_hover(self.__handle_on_spell_slot_hover)
        self.__action_panel.on_spell_slot_press(self.__handle_on_spell_slot_press)
        self.__action_panel.on_spell_slot_release(self.__handle_on_spell_slot_release)
        self.__action_panel.on_spell_slot_leave(self.__handle_on_spell_slot_leave)
    
    def __handle_on_spell_slot_hover(self, spell: Spell):
        if (spell is not None):
            self.__spell_detail_popup = SpellDetailPopup(spell, self.player.character.character_class, rpg.constants.SPELL_POPUP_WIDTH, rpg.constants.SPELL_POPUP_HEIGHT, rpg.constants.SPELL_POPUP_POSITION)
    
    def __handle_on_spell_slot_press(self):
        if (self.__spell_detail_popup is not None):
            pass
    
    def __handle_on_spell_slot_release(self):
        if (self.__spell_detail_popup is not None):
            pass

    def __handle_on_spell_slot_leave(self):
        self.__spell_detail_popup = None

    def __generate_enemies(self):
        for _ in range(Range(10, 10).random()):
            enemy: Enemy = GameGenerator.generate_random_enemy()
            enemy.threat.increase(50.0)
            enemy.zone_radius = 200
            enemy.set_default_position(Position(Range(0, rpg.constants.WINDOW_WIDTH).random(), Range(0, rpg.constants.WINDOW_HEIGHT).random()))
            level: int = Range(1, 20).random()
            while (enemy.level.value < level):
                enemy.level.up()
            self.__enemies_sprites.append(EnemyComponent(enemy))

    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.get_position().x < (rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x)):
            character.get_position().x = rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x
        if (character.get_position().x > self.width):
            character.get_position().x = self.width
        if (character.get_position().y < 0):
            character.get_position().y = 0
        if (character.get_position().y > self.height):
            character.get_position().y = self.height

    def __handle_interaction_and_moves_for_friends(self):
        for friend in self.__friends_group.members:
            others: list[Character] = [other for other in self.__friends_group.members if other is not friend]
            others += [other.character for other in self.__enemies_sprites]
            for other in others:
                if friend.is_touching(other):
                    friend.avoid_collision_with_other(other)
            if friend.is_touching(self.player.character):
                friend.avoid_collision_with_other(self.player.character)
            else:
                friend.follow(self.player.character)
            self.__prevent_character_to_disapear_from_scene(friend)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        enemy.is_in_fight_mode = False
        if Geometry.compute_distance(enemy.get_position(), enemy.zone_center) > 1:
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.zone_center.x - enemy.get_position().x
            direction_y = enemy.zone_center.y - enemy.get_position().y
            direction_length = Geometry.compute_distance(enemy.get_position(), enemy.zone_center)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa position initiale
            enemy.get_position().x += direction_x * enemy.move_speed
            enemy.get_position().y += direction_y * enemy.move_speed

    def __move_enemy_to_the_patrol_position(self, enemy: Enemy):
        enemy.is_in_fight_mode = False
        if (Geometry.compute_distance(enemy.get_position(), enemy.patrol_destination) > 1):
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.patrol_destination.x - enemy.get_position().x
            direction_y = enemy.patrol_destination.y - enemy.get_position().y
            direction_length = Geometry.compute_distance(enemy.get_position(), enemy.patrol_destination)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa destination de patrouillage
            enemy.get_position().x += (direction_x * (enemy.move_speed/2))
            enemy.get_position().y += (direction_y * (enemy.move_speed/2))

    def __prepare_enemy_to_fight(self, enemy: Enemy, target: Character):
        target.is_in_fight_mode = True
        distance_between_enemy_and_zone_center = Geometry.compute_distance(enemy.get_position(), enemy.zone_center)
        if distance_between_enemy_and_zone_center < enemy.zone_radius:
            enemy.follow(target)

    def __recruit_member(self, member: Character):
        if (not self.__friends_group.is_full()):
            self.__friends_group.add_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.player.character)):
            self.__recruit_member(member)

    def __draw_hud(self, master: pygame.Surface):
        self.__group_panel.draw(master)
        self.__action_panel.draw(master)
        self.__experience_panel.draw(master)
        self.__message_panel.draw(master)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.draw(master)

    def __draw_scene(self, master: pygame.Surface):
        for hero_sprite in self.__friends_sprites:
            hero_sprite.draw(master)
        for vilain_sprite in self.__enemies_sprites:
            vilain_sprite.draw(master)

    def __handle_projectif_hit(self):
        for friend_sprite in self.__friends_sprites:
            for projectil_sprite in friend_sprite.projectils:
                for vilain_sprite in self.__enemies_sprites:
                    if (vilain_sprite.character.is_touching(projectil_sprite.projectil)):
                        self.__message_broker.add_debug_message(f"[ENEMY] {vilain_sprite.character.name} was killed.")
                        vilain_sprite.character.life.loose(projectil_sprite.projectil.payload)
                        if (projectil_sprite.projectil in friend_sprite.character.trigged_projectils):
                            friend_sprite.character.trigged_projectils.remove(projectil_sprite.projectil)
                            friend_sprite.projectils.remove(projectil_sprite)
                        if (vilain_sprite.character.life.is_dead()):
                            if (vilain_sprite in self.__enemies_sprites):
                                self.__enemies_sprites.remove(vilain_sprite)
                            win_experience: int = (vilain_sprite.character.level.value*5) + 45
                            friend_sprite.character.level.gain(win_experience)



    def __handle_enemy_actions(self, enemy_sprite: EnemyComponent):
        threated_distances: dict[Character, float] = {}
        for friend in self.__friends_group.members:
            enemy_is_already_threatened: bool = enemy_sprite.character.threat.is_threatened
            if (enemy_sprite.character.is_feel_threatened(friend)):
                if (not enemy_is_already_threatened):
                    self.__message_broker.add_debug_message(f"Enemy {enemy_sprite.character.name} is feel threatened by {friend.name}.")
                threated_distances[friend] = Geometry.compute_distance(friend.get_position(), enemy_sprite.character.get_position())
        most_threatening_friend: Character = None
        if (threated_distances):
            most_threatening_friend = min(threated_distances, key=threated_distances.get)

        if (most_threatening_friend is not None):
            new_fight: Fight = None
            if (enemy_sprite.character not in list(self.__fights.keys())):
                new_fight: Fight = Fight(enemy_sprite.character, most_threatening_friend)
                self.__fights[enemy_sprite.character] = new_fight
            if (enemy_sprite.character.is_patrolling):
                enemy_sprite.character.stop_patrolling()
            if (not most_threatening_friend.is_in_fight_mode):
                most_threatening_friend.is_in_fight_mode = True
            self.__prepare_enemy_to_fight(enemy_sprite.character, most_threatening_friend)
            if (new_fight is not None):
                if (not new_fight.is_alive()):
                    new_fight.start()
            if (enemy_sprite.character.is_touching(most_threatening_friend)):
                enemy_sprite.character.attack(most_threatening_friend)
                if (len(enemy_sprite.character.trigged_projectils) > 0):
                    projectil: Projectil = enemy_sprite.character.trigged_projectils[-1]
                    projectil.to_position = most_threatening_friend.get_position().copy()
                    projectil_sprite: ProjectilComponent = ProjectilComponent(projectil)
                    enemy_sprite.projectils.append(projectil_sprite)
                
        else:
            if (enemy_sprite.character in list(self.__fights.keys())):
                existing_fight: Fight = self.__fights[enemy_sprite.character]
                existing_fight.stop()
            enemy_sprite.projectils.clear()
            enemy_sprite.character.trigged_projectils.clear()
            if (not enemy_sprite.character.is_patrolling):
                if (not enemy_sprite.character.is_arrived_to_default_position()):
                    self.__move_enemy_to_the_default_observation_position(enemy_sprite.character)
                else:
                    self.__message_broker.add_debug_message(f"[ENEMY] {enemy_sprite.character.name} start patrol.")
                    enemy_sprite.character.generate_patrol_path()
                    enemy_sprite.character.patrol()
            else:                            
                if (not enemy_sprite.character.is_arrived_to_patrol_destination()):
                    self.__move_enemy_to_the_patrol_position(enemy_sprite.character)
                else:
                    enemy_sprite.character.generate_patrol_path()

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            # HANDLE YOUR GAME HERE
            for hero_sprite in self.__friends_sprites:
                hero_sprite.handle(event)
            for vilain_sprite in self.__enemies_sprites:
                vilain_sprite.handle(event)
                difficulty: Difficulty = Difficulty.compute(self.player.character.level, vilain_sprite.character.level)
                vilain_sprite.set_difficulty_color(difficulty.value.color.to_tuple())
                            
            # self.__friends_group.handle(event)
            self.__group_panel.handle(event)
            self.__action_panel.handle(event)
            self.__experience_panel.handle(event)
            if (self.__spell_detail_popup is not None):
                self.__spell_detail_popup.handle(event)
            self.__message_panel.handle(event)
        else:
            self.__handle_projectif_hit()
            # self.__friends_group.handle(None)
            self.__group_panel.handle(None)
            self.__action_panel.handle(None)
            self.__experience_panel.handle(None)
            if (self.__spell_detail_popup is not None):
                self.__spell_detail_popup.handle(None)
            for component in self.__friends_sprites:
                component.handle(None)
                
            for component in self.__enemies_sprites:
                component.handle(None)
            self.__message_panel.handle(None)
        
        self.player.set_character([character for character in self.__friends_group.members if character.is_selected()][0])
        self.__action_panel.set_character(self.player.character)
        self.__action_panel.set_spells_wheel(self.player.spells_wheel)
        self.__initialize_events_listeners()
        self.__experience_panel.set_character(self.player.character)
        if (self.player.character.is_moving):
            for member in self.__friends_group.members:
                self.__recruit_member_if_is_touching(member)

        self.__handle_interaction_and_moves_for_friends()

        self.player.character.is_in_fight_mode = False
        for vilain_sprite in self.__enemies_sprites:
            self.__handle_enemy_actions(vilain_sprite)

    def draw(self, master: pygame.Surface):
        self.__draw_scene(master)
        self.__draw_hud(master)

class BuildingInteriorScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)

    def handle(self, event: pygame.event.Event):
        return super().handle(event)
    
    def draw(self, master: pygame.Surface):
        super().draw(master)
