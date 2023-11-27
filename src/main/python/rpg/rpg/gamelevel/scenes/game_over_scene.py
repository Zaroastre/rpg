import pygame
from rpg.gamelevel.scenes.scenes import Scene
from rpg.gameplay.player import Player

class GameOverScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        self.__options: dict[str, callable] = {}
        self.__options["Play again"] = self.__play_again
        self.__options["Go to Menu"] = self.__go_to_menu
        
        self.__font_size: int = 100
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255,0,0)
        
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
        self.__on_play_again_event_listener: callable = None
        self.__on_go_to_menu_event_listener: callable = None
    
    def set_event_listener_on_play_again(self, callback: callable):
        self.__on_play_again_event_listener = callback
    
    def set_event_listener_on_go_to_menu(self, callback: callable):
        self.__on_go_to_menu_event_listener = callback
    
    def __play_again(self):
        if (self.__on_play_again_event_listener is not None):
            self.__on_play_again_event_listener()
            
    def __go_to_menu(self):
        if (self.__on_go_to_menu_event_listener is not None):
            self.__on_go_to_menu_event_listener()
    
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
            buttons_panel.blit(button, (0, button_position_y))
            button_position_y += (button_height + button_space_height)
        label: pygame.Surface = self.__font.render("Game Over".upper(), True, self.__font_color)
        self._background_texture.blit(label, ((self.width/2)-(label.get_width()/2), (self.height/3)-(label.get_height()/2)))
        self._background_texture.blit(buttons_panel, ((self.width/2)-(buttons_panel.get_width()/2), (self.height/2)-(buttons_panel.get_height()/2)))
        super().draw(master)
