from rpg.gamedesign.faction_system import Faction

class City:
    def __init__(self, name: str, is_capital: bool, faction: Faction) -> None:
        self.__name: str = name
        self.__is_capital: bool = is_capital
        self.__faction: Faction = faction
    @property
    def name(self) -> str:
        return self.__name

class Land:
    pass

class Region:
    def __init__(self, name: str, minimal_recommanded_level: int, cities: list[City]) -> None:
        self.__name: str = name
        self.__minimal_recommanded_level: int = minimal_recommanded_level
        self.__cities: list[City] = cities
        self.__land: Land = Land()
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
        self.__world: World = world

    @property
    def workd(self) -> World:
        return self.__world

class Radar:
    def __init__(self, world_map: Map) -> None:
        self.__map: Map = world_map
    
    @property
    def world_map(self) -> Map:
        return self.__map

class CityBuilder:
    def __init__(self, name: str, region_builder=None) -> None:
        self.__region_builder: RegionBuilder|None = region_builder
        self.__name: str = name
        self.__faction: Faction = Faction.NEUTRAL
        self.__is_capital: bool = False

    def is_capital(self, is_capital: bool):
        self.__is_capital = is_capital
        return self
    
    def faction(self, faction: Faction):
        self.__faction = faction
        return self

    def build(self) -> City:
        return City(self.__name, self.__is_capital, self.__faction)

    def region(self):
        city: City = self.build()
        self.__region_builder.with_city(city)
        return self.__region_builder


class RegionBuilder:
    def __init__(self, name: str, continent_builder=None) -> None:
        self.__continent_builder: ContinentBuilder|None = continent_builder
        self.__name: str = name
        self.__cities: list[City] = []
        self.__minimal_recommanded_level: int = 1

    def with_minimal_recommanded_level(self, level: int):
        self.__minimal_recommanded_level = level
        return self

    def with_city(self, city: City):
        self.__cities.append(city)
        return self

    def city(self, name: str):
        return CityBuilder(name, self)

    def build(self) -> Region:
        return Region(self.__name, self.__minimal_recommanded_level, self.__cities)

    def continent(self):
        region: Region = self.build()
        self.__continent_builder.with_region(region)
        return self.__continent_builder

class ContinentBuilder:
    def __init__(self, name: str, world_builder = None) -> None:
        self.__world_builder: WorldBuilder|None = world_builder
        self.__name: str = name
        self.__regions: list[City] = []

    def with_region(self, region: Region):
        self.__regions.append(region)
        return self
        
    def region(self, name: str):
        return RegionBuilder(name, self)

    def build(self) -> Continent:
        return Continent(self.__name, self.__regions)

    def world(self):
        return self.__world_builder


class WorldBuilder:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__continents: list[Continent] = []


    def with_continent(self, continent: Continent):
        self.__continents.append(continent)
        return self
        
    def continent(self, name: str):
        return ContinentBuilder(name, self)

    def build(self) -> World:
        return World(self.__continents)
