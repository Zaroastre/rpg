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
    def __init__(self, level: int) -> None:
        self.__value: int = level
        self.__experience: Experience = Experience(maximum=self.__compute_maximul_required_experience())
    
    def __compute_maximul_required_experience(self) -> int:
        return int(((8*self.__value) + self.__difference()) * self.__mxp() * self.__reduction_factor())
        
    def __difference(self) -> int:
        diff: int = 0
        if (self.__value <= 10):
            diff = 0
        elif (self.__value <= 20):
            diff = 1
        elif (self.__value <= 30):
            diff = 3
        elif (self.__value <= 40):
            diff = 6
        else:
            diff = 5*(self.__value-30)
        return diff
    
    def __reduction_factor(self) -> float:
        factor: float = 1.0
        if (self.__value <= 10):
            factor = 1.0
        elif (self.__value <= 30):
            factor = (1-(self.__value-10)/100)
        elif (self.__value <= 50):
            factor = 0.82
        else:
            factor = 1.0
        return factor
    
    def __mxp(self):
        return 45 + (5*self.__value)
    
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
                self.__experience = Experience(maximum=self.__compute_maximul_required_experience())
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
