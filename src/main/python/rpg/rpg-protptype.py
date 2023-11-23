import pygame

import rpg.constants
from rpg.characters import Character, Enemy
from rpg.gamedesign.interval_system import Range
from rpg.gamengine import GameGenerator
from rpg.math.geometry import Geometry
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.ui.components import CharacterComponent, EnemyComponent
from rpg.ui.graphics import ActionPanel, ExperiencePanel, GroupPanel, SpellDetailPopup
from rpg.configuration import Configuration
from rpg.gameplay.player import Player
from rpg.gamelevel.scenes import Scene, MainMenuScene, CharacterCreationScreen, GameScene

pygame.init()
pygame.joystick.init()

class App:
    """Class that represents the program.
    """

    def __init__(self) -> None:
        print("Starting application...")
        print("Creating window...")
        self.__configuration: Configuration = Configuration()
        self.__window: pygame.Surface
        if (self.__configuration.fullscreen):
            self.__window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__window = pygame.display.set_mode((self.__configuration.window_width, self.__configuration.window_height))
        pygame.display.set_caption("World Of Nemesys")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running: bool = True
        self.__player: Player = Player()
        self.__scene: Scene = MainMenuScene(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_event_listener_on_create_new_game(self.__replace_scene_by_create_new_game_scene)
        self.__scene.set_event_listener_on_continue_game(self.__replace_scene_by_continue_game_scene)
        self.__joystick: pygame.joystick.Joystick = None
        self.__player_characters: list[Character] = []
        
    def __replace_scene_by_create_new_game_scene(self):
        self.__scene = CharacterCreationScreen(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_event_listener_on_play(self.__replace_scene_by_game_scene)
        self.__scene.set_event_listener_on_back(self.__replace_scene_by_main_menu_scene)
    
    def __replace_scene_by_game_scene(self, friends: list[Character]):
        self.__player_characters = friends
        self.__player.set_character(friends[0])
        self.__replace_scene_by_continue_game_scene()
    
    def __replace_scene_by_main_menu_scene(self):
        self.__scene = MainMenuScene(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_event_listener_on_create_new_game(self.__replace_scene_by_create_new_game_scene)
        self.__scene.set_event_listener_on_continue_game(self.__replace_scene_by_continue_game_scene)

    def __replace_scene_by_continue_game_scene(self):
        self.__scene = GameScene(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_friends_group(self.__player_characters)
        
    def __handle(self):
        events: list[pygame.event.Event] = pygame.event.get()
        if (len(events) > 0):
            for event in events:
                if (event.type == pygame.JOYDEVICEADDED):
                    self.__joystick = pygame.joystick.Joystick(event.device_index)
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.__scene.handle(event)
        else:
            self.__scene.handle(None)
    
    def __draw(self):
        self.__window.fill(rpg.constants.BACKGROUND_COLOR)
        self.__scene.draw(self.__window)

    def run(self):
        while (self.is_running):
            self.__handle()
            self.__draw()
            pygame.display.flip()
            self.clock.tick(self.__configuration.frames_per_second)
        pygame.quit()

    @staticmethod
    def main():
        app: App = App()
        app.run()

if (__name__ == "__main__"):
    App.main()
