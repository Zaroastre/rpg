class Experience:
    def __init__(self, maximum: int, current: int = 0) -> None:
        self.__maximum: int = maximum
        self.__current: int = current if current is not None and current >= 0 else maximum

    @property
    def maximum(self) -> int:
        return self.__maximum
    @property
    def current(self) -> int:
        return self.__current
    
    def gain(self, experience: int):
        if (experience >= 0):
            self.__current += experience
    
    def reset_current_experience(self):
        self.__current = 0
            
class Level:
    def __init__(self, level: int, maximum_experience: int) -> None:
        self.__value: int = level
        self.__experience: Experience = Experience(maximum=maximum_experience)
    
    @property
    def value(self) -> int:
        return self.__value
    
    @property
    def experience(self) -> Experience:
        return self.__experience
    
    def up(self):
        self.__value += 1
        self.__reset_current_experience()
    
    def __reset_current_experience(self):
        self.__experience.reset_current_experience()
    
    def gain(self, experience: int):
        if (experience >= 0):
            self.__experience.gain(experience)
            if (self.__experience.current >= self.__experience.maximum):
                delta: int = self.__experience.current - self.__experience.maximum
                self.up()
                self.__experience.gain(delta)

class Rank:
    def __init__(self, maximum: int) -> None:
        if (maximum is None or maximum <= 0):
            raise ValueError()
        self.__current: int = 0
        self.__maximum: int = maximum
    @property
    def current(self) -> int:
        return self.__current
    @property
    def maximum(self) -> int:
        return self.__maximum
    
    def up(self):
        if (self.__current + 1 <= self.__maximum):
            self.__current += 1
    
    def reset(self):
        self.__current = 0
