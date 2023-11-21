from random import randint

class Range:
    def __init__(self, minimum: int, maximum: int) -> None:
        self.__minimum: int = minimum
        self.__maximum: int = maximum
    @property
    def minimum(self) -> int:
        return self.__minimum
    @property
    def maximum(self) -> int:
        return self.__maximum
    def random(self) -> int:
        return randint(self.minimum, self.maximum)