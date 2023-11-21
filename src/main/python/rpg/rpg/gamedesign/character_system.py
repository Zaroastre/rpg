class Life:
    def __init__(self, maximum: int, left: int = None) -> None:
        self.__maximum: int = maximum
        self.__current: int = left if left is not None else max
        self.__boost: list[int] = []
        
    @property
    def maximum(self) -> int:
        return self.__maximum

    @property
    def actual(self) -> int:
        return self.__current
    
    def loose(self, points: int):
        self.__current -= points
        if (self.__current <= 0):
            self.die()

    def die(self):
        self.__current = 0

    def is_dead(self) -> bool:
        return self.__current <= 0
    
    def heal(self, points: int):
        self.__current += points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum
    
    def is_alive(self) -> bool:
        return not self.is_dead()
    
    def win_boost(self, boost_points: int):
        self.__maximum += boost_points
        self.__current += boost_points
    
    def loose_boost(self, boost_points: int):
        self.__maximum -= boost_points
        if (self.__current > self.__maximum):
            self.__current = self.__maximum


class AbstractCharacter:
    def __init__(self) -> None:
        self.__life: Life = Life(100, 100)
    
    @property
    def life(self) -> Life:
        return self.__life