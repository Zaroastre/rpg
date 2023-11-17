class Breed:
    def __init__(self) -> None:
        self.__life: Life = Life(100, 100)
    
    @property
    def life(self) -> Life:
        return self.__life

class Human(Breed):
    def __init__(self) -> None:
        super().__init__()
