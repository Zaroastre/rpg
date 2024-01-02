from typing import TypeVar
T = TypeVar('T')

class NoSuchElementException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Optional:
    """
    A container object which may or may not contain a non-null value. If a value is present, isPresent() will return true and get() will return the value.
    
    Additional methods that depend on the presence or absence of a contained value are provided, such as orElse() (return a default value if value not present) and ifPresent() (execute a block of code if the value is present).
    
    This is a value-based class; use of identity-sensitive operations (including reference equality (==), identity hash code, or synchronization) on instances of Optional may have unpredictable results and should be avoided.
    """
    def __init__(self, value: T|None) -> None:
        self.__value: T|None = value
    
    def is_present(self) -> bool:
        """
        Return true if there is a value present, otherwise false.
        """
        return self.__value is not None

    def get(self) -> T:
        """
        If a value is present in this Optional, returns the value, otherwise throws NoSuchElementException.
        """
        if (self.__value is None):
            raise NoSuchElementException()
        return self.__value

    def if_present(self, callback: callable):
        """
        If a value is present, invoke the specified consumer with the value, otherwise do nothing.
        """
        if (self.__value is not None):
            callback()

    def or_else(self, other: T):
        """
        Return the value if present, otherwise return other.
        """
        return self.__value if self.__value is not None else other

    @staticmethod
    def of(value: T):
        """
        Returns an Optional with the specified present non-null value.
        """
        return Optional(value)

    @staticmethod
    def of_nullable(value: T|None):
        """
        Returns an Optional describing the specified value, if non-null, otherwise returns an empty Optional.
        """
        return Optional(value)

    @staticmethod
    def empty():
        """
        Returns an empty Optional instance.
        """
        return Optional(None)


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
