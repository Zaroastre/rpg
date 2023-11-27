import pygame
from rpg.gamelevel.scenes.scenes import Scene
from rpg.gameplay.player import Player


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
