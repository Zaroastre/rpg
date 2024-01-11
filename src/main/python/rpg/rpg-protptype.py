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
from rpg.gamedesign.faction_system import Faction
from rpg.gamedesign.backup_system import GameLoader, GameSaverThread
from rpg.gamedesign.world_system import World, WorldBuilder, ContinentBuilder, RegionBuilder
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
        self.__world: World = self.__create_world()
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
    
    def __create_world(self) -> World:
        # https://wowpedia.fandom.com/wiki/Zone
        world_builder: WorldBuilder = WorldBuilder("Azeroth")
        continent_builder: ContinentBuilder = world_builder.continent("Eastern Kingdoms")\
            .region("Gilneas")\
                .with_minimal_recommanded_level(1)\
                .city("Duskhaven").faction(Faction.ALLIANCE).region()\
                .city("Stormglen").faction(Faction.ALLIANCE).region()\
                .city("Gilneas City").faction(Faction.ALLIANCE).is_capital(True).region()\
            .continent()
        continent_builder.region("Ghostlands")\
                .with_minimal_recommanded_level(1)\
                .city("Tranquillien").faction(Faction.HORDE).region()\
                .city("Hatchet Hills").faction(Faction.NEUTRAL).region()\
            .continent()
        continent_builder.region("Loch Modan")\
                .with_minimal_recommanded_level(5)\
                .city("Thelsamar").faction(Faction.ALLIANCE).region()\
                .city("Farstrider Lodge").faction(Faction.ALLIANCE).region()\
            .continent()
        continent_builder.region("Eversong Woods")\
                .with_minimal_recommanded_level(1)\
                .city("Sunstrider Isle").faction(Faction.HORDE).region()\
                .city("Falconwing Square").faction(Faction.HORDE).region()\
                .city("Fairbreeze Village").faction(Faction.HORDE).region()\
                .city("Silvermoon City").faction(Faction.HORDE).is_capital(True).region()\
            .continent()
        continent_builder.region("Elwynn Forest")\
                .with_minimal_recommanded_level(1)\
                .city("Northshire").faction(Faction.ALLIANCE).region()\
                .city("Goldshire").faction(Faction.ALLIANCE).region()\
                .city("Stormwind City").faction(Faction.ALLIANCE).is_capital(True).region()\
            .continent()
        continent_builder.region("Dun Morogh")\
                .with_minimal_recommanded_level(1)\
                .city("Coldridge Valley").faction(Faction.ALLIANCE).region()\
                .city("New Tinkertown").faction(Faction.ALLIANCE).region()\
                .city("Kharanos").faction(Faction.ALLIANCE).region()\
                .city("Ironforge").faction(Faction.ALLIANCE).is_capital(True).region()\
            .continent()
        continent_builder.region("Duskwood")\
                .with_minimal_recommanded_level(10)\
                .city("Darkshire,").faction(Faction.ALLIANCE).region()\
                .city("Raven Hill").faction(Faction.ALLIANCE).region()\
            .continent()
        continent_builder.region("Redridge Mountains")\
                .with_minimal_recommanded_level(7)\
                .city("Lakeshire").faction(Faction.ALLIANCE).region()\
                .city("Shalewind Canyon").faction(Faction.ALLIANCE).region()\
            .continent()
        continent_builder.region("Stranglethorn Vale")\
            .continent()
        continent_builder.region("Westfall")\
                .with_minimal_recommanded_level(5)\
                .city("Sentinel Hill").faction(Faction.ALLIANCE).region()\
                .city("Moonbrook").faction(Faction.ALLIANCE).region()\
            .continent()
        continent_builder.region("Deadwind Pass")\
                .with_minimal_recommanded_level(10)\
                .city("Karazhan").faction(Faction.NEUTRAL).region()\
            .continent()
        continent_builder.region("Swamp of Sorrows")\
                .with_minimal_recommanded_level(15)\
                .city("The Harborage").faction(Faction.ALLIANCE).region()\
                .city("Stonard").faction(Faction.HORDE).region()\
                .city("Bogpaddle").faction(Faction.NEUTRAL).region()\
            .continent()
        continent_builder.region("Blasted Lands")\
                .with_minimal_recommanded_level(15)\
                .city("Nethergarde Keep").faction(Faction.ALLIANCE).region()\
                .city("Surwich").faction(Faction.ALLIANCE).region()\
                .city("Dreadmaul Hold").faction(Faction.HORDE).region()\
                .city("Sunveil Excursion").faction(Faction.HORDE).region()\
            .continent()

        continent_builder.region("Isle of Quel'Danas")\
                .with_minimal_recommanded_level(30)\
                .city("Sun's Reach").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("Kelp'thar Forest")\
                .with_minimal_recommanded_level(30)\
                .city("Seafarer's Tomb").faction(Faction.ALLIANCE).region()\
                .city("Legion's Fate").faction(Faction.HORDE).region()\
                .city("Deepmist Grotto").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("Shimmering Expanse")\
                .with_minimal_recommanded_level(30)\
                .city("Tranquil Wash").faction(Faction.ALLIANCE).region()\
                .city("Legion's Rest").faction(Faction.HORDE).region()\
                .city("Silver Tide Hollow").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("Abyssal Depths")\
                .with_minimal_recommanded_level(30)\
                .city("Darkbreak Cove").faction(Faction.ALLIANCE).region()\
                .city("Tenebrous Cavern").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("Twilight Highlands ")\
                .with_minimal_recommanded_level(30)\
                .city("Highbank").faction(Faction.ALLIANCE).region()\
                .city("Firebeard's Patrol").faction(Faction.ALLIANCE).region()\
                .city("Victor's Point").faction(Faction.ALLIANCE).region()\
                .city("Thundermar").faction(Faction.ALLIANCE).region()\
                .city("Kirthaven").faction(Faction.ALLIANCE).region()\
                .city("Dragonmaw Port").faction(Faction.HORDE).region()\
                .city("Krazzworks").faction(Faction.HORDE).region()\
                .city("Bloodgulch").faction(Faction.HORDE).region()\
                .city("Crushblow").faction(Faction.HORDE).region()\
                .city("The Gullet").faction(Faction.HORDE).region()\
            .continent()
            
        continent_builder.region("Tol Barad Peninsula")\
                .with_minimal_recommanded_level(30)\
                .city("Baradin Base Camp").faction(Faction.ALLIANCE).region()\
                .city("Hellscream's Grasp").faction(Faction.HORDE).region()\
            .continent()
            
        continent_builder.region("Tol Barad")\
                .with_minimal_recommanded_level(30)\
                .city("Baradin Hold").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("Burning Steppes")\
                .with_minimal_recommanded_level(15)\
                .city("Morgan's Vigil").faction(Faction.ALLIANCE).region()\
                .city("Flame Crest").faction(Faction.HORDE).region()\
            .continent()

        continent_builder.region("The Hinterlands")\
                .with_minimal_recommanded_level(10)\
                .city("Aerie Peak").faction(Faction.ALLIANCE).region()\
                .city("Stormfeather Outpost").faction(Faction.ALLIANCE).region()\
                .city("Hiri'watha Research Station").faction(Faction.HORDE).region()\
                .city("Revantusk Village").faction(Faction.HORDE).region()\
            .continent()

        continent_builder.region("Searing Gorge")\
                .with_minimal_recommanded_level(15)\
                .city("Iron Summit").faction(Faction.NEUTRAL).region()\
                .city("Thorium Point").faction(Faction.NEUTRAL).region()\
            .continent()

        continent_builder.region("Eastern Plaguelands")\
                .with_minimal_recommanded_level(15)\
                .city("Light's Hope Chapel").faction(Faction.NEUTRAL).region()\
                .city("Acherus: The Ebon Hold").faction(Faction.NEUTRAL).region()\
            .continent()
        continent_builder.region("Hillsbrad Foothills")\
                .with_minimal_recommanded_level(7)\
                .city("Sludge Fields").faction(Faction.HORDE).region()\
                .city("Tarren Mill").faction(Faction.HORDE).region()\
                .city("Eastpoint Tower").faction(Faction.HORDE).region()\
            .continent()
        continent_builder.region("Silverpine Forest")\
                .with_minimal_recommanded_level(5)\
                .city("Forsaken Rear Guard").faction(Faction.HORDE).region()\
                .city("The Sepulcher").faction(Faction.HORDE).region()\
            .continent()
        continent_builder.region("Tirisfal Glades")\
                .with_minimal_recommanded_level(1)\
                .city("Deathknell").faction(Faction.HORDE).region()\
                .city("Brill").faction(Faction.HORDE).region()\
                .city("The Bulwark").faction(Faction.HORDE).region()\
                .city("Undercity").faction(Faction.HORDE).is_capital(True).region()\
            .continent()
        
        continent_builder.region("Wetlands")\
                .with_minimal_recommanded_level(10)\
                .city("Greenwarden's Grove").faction(Faction.ALLIANCE).region()\
                .city("Swiftgear Station").faction(Faction.ALLIANCE).region()\
                .city("Menethil Harbor").faction(Faction.ALLIANCE).region()\
            .continent()
            
        continent_builder.region("Plaguelands: The Scarlet Enclave")\
                .with_minimal_recommanded_level(5)\
                .city("Light's Hope Chapel").faction(Faction.NEUTRAL).region()\
                .city("Acherus: The Ebon Hold").faction(Faction.NEUTRAL).region()\
            .continent()
        
        continent_builder.region("Arathi Highlands")\
                .with_minimal_recommanded_level(10)\
                .city("Refuge Pointe").faction(Faction.ALLIANCE).region()\
                .city("Hammerfall").faction(Faction.HORDE).region()\
                .continent()
        
        continent_builder.region("Northern Stranglethorn")\
                .with_minimal_recommanded_level(10)\
                .city("Fort Livingston").faction(Faction.ALLIANCE).region()\
                .city("Grom'gol Base Camp").faction(Faction.HORDE).region()\
                .continent()
        
        continent_builder.region("Western Plaguelands")\
                .with_minimal_recommanded_level(15)\
                .city("Chillwind Camp").faction(Faction.ALLIANCE).region()\
                .city("Andorhal").faction(Faction.HORDE).region()\
                .continent()
                
        continent_builder.region("Badlands")\
                .with_minimal_recommanded_level(15)\
                .city("Dragon's Mouth").faction(Faction.ALLIANCE).region()\
                .city("New Kargath").faction(Faction.HORDE).region()\
                .city("Fuselight").faction(Faction.NEUTRAL).region()\
            .continent()
            
        continent_builder.region("The Cape of Stranglethorn")\
                .with_minimal_recommanded_level(10)\
                .city("Explorers' League Digsite, ").faction(Faction.ALLIANCE).region()\
                .city("Hardwrench Hideaway").faction(Faction.HORDE).region()\
                .city("Booty Bay").faction(Faction.NEUTRAL).region()\
                .continent().world()
            
        world_builder.continent("Kalimdor")\
                .region("Durotar")\
                .continent()\
                .region("Mulgore")\
                .continent()\
                .region("Northern Barrens")\
                .continent()\
                .region("Southern Barrens")\
                .continent()\
                .region("Stonetalon Mountains")\
                .continent()\
                .region("Ashenvale")\
                .continent()\
                .region("Azshara")\
                .continent()\
                .region("Desolace")\
                .continent()\
                .region("Dustwallow Marsh")\
                .continent()\
                .region("Felwood")\
                .continent()\
                .region("Feralas")\
                .continent()\
                .region("Silithus")\
                .continent()\
                .region("Tanaris")\
                .continent()\
                .region("Thousand Needles")\
                .continent()\
                .region("Un'Goro Crater")\
                .continent()\
                .region("Winterspring")\
                .continent().world()
        world_builder.continent("Northrend")\
                .region("Borean Tundra")\
                .continent()\
                .region("Howling Fjord")\
                .continent()\
                .region("Dragonblight")\
                .continent()\
                .region("Grizzly Hills")\
                .continent()\
                .region("Zul'Drak")\
                .continent()\
                .region("Sholazar Basin")\
                .continent()\
                .region("Crystalsong Forest")\
                .continent()\
                .region("The Storm Peaks")\
                .continent()\
                .region("Icecrown")\
                .continent().world()
        world_builder.continent("Pandaria")\
                .region("The Jade Forest")\
                .continent()\
                .region("Valley of the Four Winds")\
                .continent()\
                .region("Krasarang Wilds")\
                .continent()\
                .region("Kun-Lai Summit")\
                .continent()\
                .region("Townlong Steppes")\
                .continent()\
                .region("Dread Wastes")\
                .continent()\
                .region("Vale of Eternal Blossoms")\
                .continent().world()
        world_builder.continent("Broken Isles")\
                .region("Azsuna")\
                .continent()\
                .region("Val'sharah")\
                .continent()\
                .region("Highmountain")\
                .continent()\
                .region("Stormheim")\
                .continent()\
                .region("Suramar")\
                .continent()\
                .region("The Broken Shore")\
                .continent().world()
        world_builder.continent("Zandalar")\
                .region("Zuldazar")\
                .continent()\
                .region("Nazmir")\
                .continent()\
                .region("Vol'dun")\
                .continent().world()
        world_builder.continent("Draenor").world()
        world_builder.continent("Outland").world()
        world_builder.continent("Argus").world()
        world_builder.continent("Vashj'ir").world()

        world_builder.continent("Kul Tiras")\
                .region("Tiragarde Sound")\
                .continent()\
                .region("Drustvar")\
                .continent()\
                .region("Stormsong Valley")\
                .continent().world()
        world: World = world_builder.build()
        for continent in world.continents:
            print("Contient: " + continent.name)
            for region in continent.regions:
                print("\tRegion: " + region.name + " " + str(region.minimal_recommanded_level))
                for city in region.cities:
                    print("\t\tCity: " + city.name)
                    
        return world

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
