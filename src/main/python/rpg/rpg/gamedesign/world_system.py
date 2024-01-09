from rpg.gamedesign.faction_system import Faction

class City:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__faction: Faction|None = None
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

    def build(self) -> City:
        return City(self.__name)

    def region(self):
        return self.__region_builder


class RegionBuilder:
    def __init__(self, name: str, continent_builder=None) -> None:
        self.__continent_builder: ContinentBuilder|None = continent_builder
        self.__name: str = name
        self.__cities: list[City] = []

    def city(self, name: str):
        return CityBuilder(name, self)

    def build(self) -> Region:
        return Region(self.__name, self.__cities)

    def continent(self):
        return self.__continent_builder

class ContinentBuilder:
    def __init__(self, name: str, world_builder = None) -> None:
        self.__world_builder: WorldBuilder|None = world_builder
        self.__name: str = name
        self.__regions: list[City] = []

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

    def continent(self, name: str):
        return ContinentBuilder(name, self)

    def build(self) -> World:
        return World(self.__continents)
    

world_builder = WorldBuilder("Azeroth")
world_builder.continent("Eastern Kingdoms")\
        .region("Elwynn Forest")\
        .continent()\
        .region("Duskwood")\
        .continent()\
        .region("Redridge Mountains")\
        .continent()\
        .region("Stranglethorn Vale")\
        .continent()\
        .region("Westfall")\
        .continent()\
        .region("Deadwind Pass")\
        .continent()\
        .region("Swamp of Sorrows")\
        .continent()\
        .region("Burning Steppes")\
        .continent()\
        .region("The Hinterlands")\
        .continent()\
        .region("Searing Gorge")\
        .continent()\
        .region("Eastern Plaguelands")\
        .continent()\
        .region("Hillsbrad Foothills")\
        .continent()\
        .region("Silverpine Forest")\
        .continent()\
        .region("Tirisfal Glades")\
        .continent()\
        .region("Arathi Highlands")\
        .continent()\
    .world()
    
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
        .continent()\
    .world()
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
        .continent()\
    .world()
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
        .continent()\
    .world()
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
        .continent()\
    .world()
world_builder.continent("Zandalar")\
        .region("Zuldazar")\
        .continent()\
        .region("Nazmir")\
        .continent()\
        .region("Vol'dun")\
        .continent()\
    .world()
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
        .continent()\
    .world()\
    .build()
