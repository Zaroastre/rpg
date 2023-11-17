class ResourceTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
    
    @property
    def name(self) -> str:
        return self.__name

class RessourceType:
    QI: ResourceTypeValue = ResourceTypeValue(name="QI")
    MANA: ResourceTypeValue = ResourceTypeValue(name="MANA")
    RAGE: ResourceTypeValue = ResourceTypeValue(name="RAGE")
    ENERGY: ResourceTypeValue = ResourceTypeValue(name="ENERGY")
    RUNE: ResourceTypeValue = ResourceTypeValue(name="RUNE")

class Resource:
    def __init__(self, resource_type: RessourceType) -> None:
        self.__maximum: int
        self.__current: int
        self.__boost: list[int] = []
        self.__type: RessourceType = resource_type

class Mana(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.MANA)
