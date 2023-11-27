class Threat:
    def __init__(self, level: int = 0) -> None:
        self.__level: int = level
        self.__is_threatened: bool = False

    @property
    def level(self) -> int:
        return self.__level
    @property
    def is_threatened(self) -> bool:
        return self.__is_threatened
    
    def increase(self, points: int):
        if (points is not None and points >= 0):
            self.__level += points

    def decrease(self, points: int):
        if (points is not None and points >= 0):
            self.__level -= points
        if (self.__level < 0):
            self.__level = 0
