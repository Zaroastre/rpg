class Optional:
    pass

class Map:
    pass

class Set:
    pass

class List:
    pass

class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 255) -> None:
        self.__red: int = red
        self.__green: int = green
        self.__blue: int = blue
        self.__alpha: int = alpha
    @property
    def red(self) -> int:
        return self.__red
    @property
    def green(self) -> int:
        return self.__green
    @property
    def blue(self) -> int:
        return self.__blue
    @property
    def alpha(self) -> int:
        return self.__alpha
    def to_tuple(self) -> tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)