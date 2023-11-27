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
    

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
