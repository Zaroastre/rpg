from enum import Enum
from abc import abstractmethod

from rpg.gameplay.attributes import Attribute

class GemTypeValue:
    pass

class GemType(Enum):
    RED: GemTypeValue = GemTypeValue()
    BLUE: GemTypeValue = GemTypeValue()
    YELLOW: GemTypeValue = GemTypeValue()
    PURPLE: GemTypeValue = GemTypeValue()
    GREEN: GemTypeValue = GemTypeValue()
    ORANGE: GemTypeValue = GemTypeValue()

class Gem:
    def __init__(self, type: GemType, value: int, attribute: Attribute) -> None:
        self.__type: GemType
        self.__value: int
        self.__attribute: Attribute
    
    @property
    def type(self) -> GemType:
        return self.__type
    @property
    def value(self) -> int:
        return self.__value
    @property
    def attribute(self) -> Attribute:
        return self.__attribute

class RedGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.RED, value, attribute)
class BlueGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.BLUE, value, attribute)
class GreenGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.GREEN, value, attribute)
class YellowGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.YELLOW, value, attribute)
class PurpleGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.PURPLE, value, attribute)
class OrangeGem(Gem):
    def __init__(self, value: int, attribute: Attribute) -> None:
        super().__init__(GemType.ORANGE, value, attribute)

class GemFactory:
    @staticmethod
    def red_gem(value: int, attribute: Attribute) -> RedGem:
        return RedGem(value, attribute)
    @staticmethod
    def green_gem(value: int, attribute: Attribute) -> GreenGem:
        return GreenGem(value, attribute)
    @staticmethod
    def blue_gem(value: int, attribute: Attribute) -> BlueGem:
        return BlueGem(value, attribute)
    @staticmethod
    def purple_gem(value: int, attribute: Attribute) -> PurpleGem:
        return PurpleGem(value, attribute)
    @staticmethod
    def yellow_gem(value: int, attribute: Attribute) -> YellowGem:
        return YellowGem(value, attribute)
    @staticmethod
    def orange_gem(value: int, attribute: Attribute) -> OrangeGem:
        return OrangeGem(value, attribute)

class NoGemSpaceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class GemNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Gemable:
    @abstractmethod
    def crimp(self, gem: Gem) -> None:
        """
        Apply the gem to the object.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove(self, gem: Gem) -> None:
        """
        Delete the gem from the object.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def can_be_crimped(self) -> bool:
        raise NotImplementedError()

class GemsBox(Gemable):
    def __init__(self, maximum_capacity: int) -> None:
        self.__maximum_capacity: int = maximum_capacity
        self.__gems: list[Gem] = []
    
    @property
    def maximum_capacity(self) -> int:
        return self.__maximum_capacity

    def crimp(self, gem: Gem) -> None:
        if (gem is not None):
            if (len(self.__gems) < self.__maximum_capacity):
                self.__gems.append(gem)
            else:
                raise NoGemSpaceException()

    def remove(self, gem: Gem) -> None:
        if (gem is not None):
            if (gem in self.__gems):
                self.__gems.remove(gem)
            else:
                raise GemNotFoundException()

    def can_be_crimped(self) -> bool:
        return len(self.__gems) < self.__maximum_capacity
