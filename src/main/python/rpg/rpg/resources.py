from abc import ABC
from enum import Enum

class ResourceTypeValue:
    def __init__(self, name: str) -> None:
        self.__name: str = name
    
    @property
    def name(self) -> str:
        return self.__name

class RessourceType(Enum):
    QI: ResourceTypeValue = ResourceTypeValue(name="QI")
    MANA: ResourceTypeValue = ResourceTypeValue(name="MANA")
    RAGE: ResourceTypeValue = ResourceTypeValue(name="RAGE")
    ENERGY: ResourceTypeValue = ResourceTypeValue(name="ENERGY")
    RUNE: ResourceTypeValue = ResourceTypeValue(name="RUNE")

class Resource(ABC):
    def __init__(self, resource_type: RessourceType, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else maximum
        self.__boost: list[int] = []
        self.__type: RessourceType = resource_type

    @property
    def maximum(self) -> int:
        return self.__maximum
    @property
    def current(self) -> int:
        return self.__current
    @property
    def boosts(self) -> list[int]:
        return self.__boost
    @property
    def resource_type(self) -> RessourceType:
        return self.__type

class Mana(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.MANA, 100)

class Rage(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.RAGE, 100, 0)
        
class Qi(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.QI, 100)
        
class Energy(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.ENERGY, 100)
        
class Rune(Resource):
    def __init__(self) -> None:
        super().__init__(RessourceType.RUNE, 10)