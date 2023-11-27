from abc import ABC
from math import cos, pi, radians, sin, sqrt
from random import uniform

import pygame
from rpg.characters import Character
from rpg.gamedesign.faction_system import Faction
from rpg.gamelevel.scenes.scenes import Scene
from rpg.gamengine import GameGenerator
from rpg.gameplay.breeds import BreedFactory, BreedType
from rpg.gameplay.classes import ClassFactory, ClassType
from rpg.gameplay.genders import Gender
from rpg.gameplay.player import Player


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
