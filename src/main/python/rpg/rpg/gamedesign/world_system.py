class City:
    def __init__(self, name: str) -> None:
        self.__name: str = name
    @property
    def name(self) -> str:
        return self.__name

class Region:
    def __init__(self, name: str, cities: list[City]) -> None:
        self.__name: str = name
        self.__cities: list[City] = cities
    @property
    def name(self) -> str:
        return self.__name
    @property
    def cities(self) -> list[City]:
        return self.__cities.copy()

class Continent:
    def __init__(self, name: str, regions: list[Region]) -> None:
        self.__name: str = name
        self.__regions: list[Region] = regions
    @property
    def name(self) -> str:
        return self.__name
    @property
    def regions(self) -> list[Region]:
        return self.__regions.copy()

class World:
    def __init__(self, continents: list[Continent]) -> None:
        self.__continents: list[Continent] = continents
    @property
    def continents(self) -> list[Continent]:
        return self.__continents.copy()

class Map:
    def __init__(self, world: World) -> None:
        self.__world: world

    @property
    def workd(self) -> World:
        return self.__world

class Radar:
    def __init__(self, world_map: Map) -> None:
        self.__map: Map = world_map
    
    @property
    def world_map(self) -> Map:
        return self.__map