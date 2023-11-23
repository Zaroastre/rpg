from abc import ABC

import pygame
import rpg.constants
from rpg.characters import Character, Enemy
from rpg.configuration import Configuration
from rpg.gameapi import Draw, InputEventHandler
from rpg.gamedesign.interval_system import Range
from rpg.gamengine import GameGenerator
from rpg.gameplay.player import Player
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry, Position
from rpg.ui.components import CharacterComponent, EnemyComponent
from rpg.ui.graphics import (ActionPanel, ExperiencePanel, GroupPanel,
                             SpellDetailPopup)
from rpg.gameplay.genders import Gender
from rpg.gameplay.breeds import BreedType, BreedFactory
from rpg.gameplay.classes import ClassType, ClassFactory
from rpg.gamedesign.faction_system import Faction
from rpg.gamengine import GameGenerator


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
        self.__button_texture: pygame.Surface = pygame.Surface((200, 50))
        self.__button_border_texture: pygame.Surface = self.__button_texture.copy()
        self.__button_background_texture: pygame.Surface = pygame.Surface((self.__button_texture.get_width()-(self.__button_border_size*2), self.__button_texture.get_height()-(self.__button_border_size*2)))
        self.__button_font_size: int = 22
        self.__button_font: pygame.font.Font = pygame.font.Font(None, self.__button_font_size)
        self.__button_font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__button_border_color: pygame.Color = pygame.Color(255, 0, 0)
        self.__unselected_button_background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__selected_button_background_color: pygame.Color = self.__button_border_color
        self.__button_margin_height: int = 20
        self.__button_margin_width: int = 100
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
        position: Position = Position(self.__button_margin_width, self.__button_margin_height)
        for option in self.__options.keys():
            self.__button_border_texture.fill(self.__button_border_color)
            if (option == self.__selected_option):
                self.__button_background_texture.fill(self.__selected_button_background_color)
            else:
                self.__button_background_texture.fill(self.__unselected_button_background_color)
            label: pygame.Surface = self.__button_font.render(option.capitalize(), True, self.__button_font_color)
            label_position_x: int = (self.__button_background_texture.get_width()/2)-(label.get_width()/2)
            label_position_y: int = (self.__button_background_texture.get_height()/2)-(label.get_height()/2)
            self.__button_background_texture.blit(label, (label_position_x, label_position_y))
            self.__button_border_texture.blit(self.__button_background_texture, (self.__button_border_size, self.__button_border_size))
            button: pygame.Rect = self.__button_texture.blit(self.__button_border_texture, (0,0))
            position.y += button.height + self.__button_margin_height
            button: pygame.Rect = self._background_texture.blit(self.__button_texture, (position.x, position.y))
            self.__buttons.append(button)
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
        
        self.__background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__buttons: list[pygame.Rect] = []
        self.__selected_button_border_size: int = 5
        self.__unselected_button_border_size: int = 2
        self.__button_texture: pygame.Surface = pygame.Surface((200, 50))
        self.__button_border_texture: pygame.Surface = self.__button_texture.copy()
        self.__button_background_texture: pygame.Surface = pygame.Surface((self.__button_texture.get_width()-(self.__unselected_button_border_size*2), self.__button_texture.get_height()-(self.__unselected_button_border_size*2)))
        self.__button_font_size: int = 22
        self.__button_character_selector_font_size: int = 50
        self.__button_font: pygame.font.Font = pygame.font.Font(None, self.__button_font_size)
        self.__button_character_selector_font: pygame.font.Font = pygame.font.Font(None, self.__button_character_selector_font_size)
        self.__button_font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__button_border_color: pygame.Color = pygame.Color(255, 0, 0)
        self.__unselected_button_background_color: pygame.Color = pygame.Color(0, 0, 0)
        self.__selected_button_background_color: pygame.Color = self.__button_border_color
        self.__button_margin_height: int = 20
        self.__button_margin_width: int = 100
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
                            faction: str = configuration.get(CharacterCreationScreen.__FACTION_KEY)
                            breed: str = configuration.get(CharacterCreationScreen.__BREED_KEY)
                            gender: str = configuration.get(CharacterCreationScreen.__GENDER_KEY)
                            character_class: str = configuration.get(CharacterCreationScreen.__CLASS_KEY)
                            
                            if (faction is not None):
                                if (breed is not None):
                                    if (gender is not None):
                                        if (character_class is not None):
                                            if (name is None):
                                                name = GameGenerator.generate_random_name()
                                            
                                            character: Character = GameGenerator.create_friend(name, BreedFactory.create(breed), ClassFactory.create(character_class), gender)
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
                    label: pygame.Surface = self.__button_character_selector_font.render("+", True, self.__button_font_color)
                    label_position_x: int = (button_background.get_width()/2)-(label.get_width()/2)
                    label_position_y: int = (button_background.get_height()/2)-(label.get_height()/2)
                    button_background.blit(label, (label_position_x, label_position_y))
                else:
                    button_background.fill(pygame.Color(255,150,0))
            else:
                if (self.__is_selecting_slot):
                    button_background.fill(pygame.Color(255,0,0))
                if (self.__characters_configurations[index] is None):
                    label: pygame.Surface = self.__button_character_selector_font.render("+", True, self.__button_font_color)
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
        self.__available_friends: Group = Group(max_capacity=10)
        self.__enemies: Group = Group(max_capacity=100)
        self.__group_of_the_player: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__group_of_the_player, width=rpg.constants.GROUP_PANEL_WIDTH, height=rpg.constants.GROUP_PANEL_HEIGHT, position=rpg.constants.GROUP_PANEL_POSITION)
        self.__heroes_components: list[CharacterComponent] = []
        self.__vilains_components: list[EnemyComponent] = []
        self.__spell_detail_popup: SpellDetailPopup = None
        
        # self.__generate_player_character()
        # self.__generate_friends()
        self.__generate_enemies()
        self.__initialize_events_listeners()

    def set_friends_group(self, friends: list[Character]):
        player: Character = friends[0]
        player.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
        player.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
        player.select()
        player.level.experience.gain(50)
        player.threat.increase(20.0)
        self.__group_of_the_player.add_member(player)
        self.player.set_character(player)
        self.__heroes_components.append(CharacterComponent(player))
        for friend in friends:
            if (friend is not player):
                self.__group_of_the_player.add_member(friend)
                self.__heroes_components.append(CharacterComponent(friend))

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
        
    def __generate_friends(self):
        for _ in range(Range(4,10).random()):
            friend: Character = GameGenerator.generate_random_player()
            friend.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            friend.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            friend.threat.increase(20)
            self.__available_friends.add_member(friend)
            self.__heroes_components.append(CharacterComponent(friend))
        
    def __generate_enemies(self):
        for _ in range(Range(100, 100).random()):
            enemy: Enemy = GameGenerator.generate_random_enemy()
            enemy.threat.increase(100.0)
            enemy.zone_radius = 200
            enemy.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            enemy.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            enemy.zone_center = enemy.get_position().copy()
            self.__enemies.add_member(enemy)
            self.__vilains_components.append(EnemyComponent(enemy))

    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.get_position().x < (rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x)):
            character.get_position().x = rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x
        if (character.get_position().x > self.width):
            character.get_position().x = self.width
        if (character.get_position().y < 0):
            character.get_position().y = 0
        if (character.get_position().y > self.height):
            character.get_position().y = self.height

    def __handle_interaction_and_moves_for_friends(self, group: Group):
        for friend in group.members:
            others: list[Character] = [other for other in group.members if other is not friend]
            others += self.__available_friends.members
            others += self.__enemies.members
            for other in others:
                if friend.is_touching(other):
                    friend.avoid_collision_with_other(other)
            if friend.is_touching(self.player.character):
                friend.avoid_collision_with_other(self.player.character)
            else:
                friend.follow(self.player.character)
            self.__prevent_character_to_disapear_from_scene(friend)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        
        # if (attacking_enemy is None):
        #     self.__player.character.is_in_fight_mode = False
        
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
            enemy.get_position().x += direction_x * rpg.constants.RETURN_SPEED
            enemy.get_position().y += direction_y * rpg.constants.RETURN_SPEED

    def __prepare_enemy_to_fight(self, enemy: Enemy, target: Character):
        target.is_in_fight_mode = True
        distance_between_enemy_and_zone_center = Geometry.compute_distance(enemy.get_position(), enemy.zone_center)
        if distance_between_enemy_and_zone_center < enemy.zone_radius:
            enemy.follow(target)

    def __recruit_member(self, member: Character):
        if (not self.__group_of_the_player.is_full()):
            self.__group_of_the_player.add_member(member)
            self.__available_friends.remove_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.player.character)):
            self.__recruit_member(member)

    def __draw_hud(self, master: pygame.Surface):
        self.__group_panel.draw(master)
        self.__action_panel.draw(master)
        self.__experience_panel.draw(master)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.draw(master)

    def __draw_scene(self, master: pygame.Surface):
        # RENDER YOUR GAME HERE
        # self.__enemies.draw(self.screen)
        # self.__available_friends.draw(self.screen)
        for component in self.__heroes_components:
            component.draw(master)
        for component in self.__vilains_components:
            component.draw(master)

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            # HANDLE YOUR GAME HERE
            for component in self.__heroes_components:
                component.handle(event)
            for component in self.__vilains_components:
                component.handle(event)
            # self.__available_friends.handle(event)
            self.__group_panel.handle(event)
            self.__action_panel.handle(event)
            self.__experience_panel.handle(event)
            if (self.__spell_detail_popup is not None):
                self.__spell_detail_popup.handle(event)
        else:
            # self.__available_friends.handle(None)
            self.__group_panel.handle(None)
            self.__action_panel.handle(None)
            self.__experience_panel.handle(None)
            if (self.__spell_detail_popup is not None):
                self.__spell_detail_popup.handle(None)
            for component in self.__heroes_components:
                component.handle(None)
            for component in self.__vilains_components:
                component.handle(None)
        
        self.player.set_character([character for character in self.__group_of_the_player.members if character.is_selected()][0])
        self.__action_panel.set_character(self.player.character)
        self.__action_panel.set_spells_wheel(self.player.spells_wheel)
        self.__initialize_events_listeners()
        self.__experience_panel.set_character(self.player.character)
        if (self.player.character.is_moving):
            for member in self.__available_friends.members:
                self.__recruit_member_if_is_touching(member)

        self.__handle_interaction_and_moves_for_friends(self.__group_of_the_player)

        for enemy in self.__enemies.members:
            if (enemy.is_feel_threatened(self.player.character)):
                self.__prepare_enemy_to_fight(enemy, self.player.character)
            else:
                self.__move_enemy_to_the_default_observation_position(enemy)

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