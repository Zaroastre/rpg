import pygame

import rpg.constants
from rpg.characters import Character
from rpg.configuration import Configuration
from rpg.gameplay.player import Player
from rpg.gamelevel.scenes.scenes import Scene
from rpg.gamelevel.scenes.characters_creator_scene import CharacterCreationScreen
from rpg.gamelevel.scenes.game_over_scene import GameOverScene
from rpg.gamelevel.scenes.main_menu_scene import MainMenuScene
from rpg.gamelevel.scenes.game_scene import GameScene
from rpg.gamedesign.backup_system import GameLoader, GameSaverThread
from rpg.artificial_intelligency.registry import ArtificialIntelligencyRegistry
from rpg.artificial_intelligency.sentinel_ai import SentinelAI


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
        self.__scene.set_event_listener_on_exit_game(self.__exit)
        self.__joystick: pygame.joystick.Joystick = None
        self.__player_characters: list[Character] = []
        self.__game_loader: GameLoader = GameLoader()
        self.__backup_thread: GameSaverThread = GameSaverThread(10, self.__game_loader)
        self.__ai_registry: ArtificialIntelligencyRegistry = ArtificialIntelligencyRegistry()
        self.__ai_registry.sentinel_ai = SentinelAI()
    
    def __exit(self):
        pygame.quit()
        exit(0)
    
    def __replace_scene_by_create_new_game_scene(self):
        self.__scene = CharacterCreationScreen(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_event_listener_on_play(self.__replace_scene_by_game_scene)
        self.__scene.set_event_listener_on_back(self.__replace_scene_by_main_menu_scene)
    
    def __replace_scene_by_game_scene(self, friends: list[Character]):
        if (len(friends) > 0):
            self.__player_characters = friends
            self.__player.set_character(friends[0])
            for member in friends:
                self.__player.group.add_member(member)
            self.__game_loader.save(self.__player)
        self.__replace_scene_by_continue_game_scene()
    
    def __replace_scene_by_main_menu_scene(self):
        self.__scene = MainMenuScene(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_event_listener_on_create_new_game(self.__replace_scene_by_create_new_game_scene)
        self.__scene.set_event_listener_on_continue_game(self.__replace_scene_by_continue_game_scene)

    def __replace_scene_by_continue_game_scene(self):
        player: Player = self.__game_loader.load()
        self.__player = player
        self.__backup_thread.set_player(player)
        for member in player.group.members:
            self.__player_characters.append(member)
        self.__scene = GameScene(width=self.__window.get_width(), height=self.__window.get_height(), player=self.__player)
        self.__scene.set_friends_group(self.__player_characters)
        self.__scene.set_ai_registry(self.__ai_registry)
        self.__scene.set_event_listener_on_game_over(self.__replace_scene_by_game_over_scene)
    
    def __replace_scene_by_game_over_scene(self):
        player: Player = self.__game_loader.load()
        self.__player = player
        self.__backup_thread.set_player(player)
        self.__scene = GameOverScene(width=self.__window.get_width(), height=self.__window.get_height(), player=player)
        self.__scene.set_event_listener_on_go_to_menu(self.__replace_scene_by_main_menu_scene)
        self.__scene.set_event_listener_on_play_again(self.__replace_scene_by_continue_game_scene)

    
    def __handle(self):
        events: list[pygame.event.Event] = pygame.event.get()
        if (len(events) > 0):
            for event in events:
                if (event.type == pygame.JOYDEVICEADDED):
                    self.__joystick = pygame.joystick.Joystick(event.device_index)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    self.__backup_thread.shutdown()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod == pygame.KMOD_ALT):
                    self.is_running = False
                    self.__backup_thread.shutdown()
                self.__scene.handle(event)
        else:
            self.__scene.handle(None)
    
    def __draw(self):
        self.__window.fill(rpg.constants.BACKGROUND_COLOR.to_tuple())
        self.__scene.draw(self.__window)

    def run(self):
        player: Player = self.__game_loader.load()
        if player is not None:
            self.__backup_thread.set_player(player)
            self.__player = player
        self.__backup_thread.start()
        while (self.is_running):
            self.__handle()
            self.__draw()
            pygame.display.flip()
            self.clock.tick(self.__configuration.frames_per_second)
        pygame.quit()
        self.__backup_thread.shutdown()

    @staticmethod
    def main():
        app: App = App()
        app.run()

if (__name__ == "__main__"):
    App.main()
