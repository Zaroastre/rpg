from json import load

class Configuration:
    __HUD_CONFIGURATION_FILE: str = "resources/hud.config.json"
    __WINDOW_CONFIGURATION_FILE: str = "resources/window.config.json"
    def __init__(self) -> None:
        self.__hud_configuration: dict[str, object] = {}
        self.__window_configuration: dict[str, object] = {}
        self.__load()
    
    def __load(self):
        with open(Configuration.__HUD_CONFIGURATION_FILE, 'r') as file:
            configuration_from_file: dict[str, object] = load(file)
            self.__hud_configuration = configuration_from_file.copy()
    
        with open(Configuration.__WINDOW_CONFIGURATION_FILE, 'r') as file:
            configuration_from_file: dict[str, object] = load(file)
            self.__window_configuration = configuration_from_file.copy()
    
    @property
    def frames_per_second(self) -> int:
        return int(self.__window_configuration.get("frames_per_second"))
    @property
    def window_width(self) -> int:
        return int(self.__window_configuration.get("window").get("width"))
    @property
    def window_height(self) -> int:
        return int(self.__window_configuration.get("window").get("height"))
    @property
    def fullscreen(self) -> bool:
        return self.__window_configuration.get("window").get("fullscreen")