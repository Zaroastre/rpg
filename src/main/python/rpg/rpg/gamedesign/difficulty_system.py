from enum import Enum
from rpg.utils import Color
from rpg.gamedesign.progression_system import Level

class DifficultyValue:
    def __init__(self, name: str, color: Color) -> None:
        self.__name: str = name
        self.__color: Color = color
    @property
    def name(self) -> str:
        return self.__name
    @property
    def color(self) -> Color:
        return self.__color

class Difficulty(Enum):
    GREY: DifficultyValue = DifficultyValue("GREY", Color(128, 128, 128))
    GREEN: DifficultyValue = DifficultyValue("GREEN", Color(0, 255, 0))
    YELLOW: DifficultyValue = DifficultyValue("YELLOW", Color(255, 255, 0))
    ORANGE: DifficultyValue = DifficultyValue("ORANGE", Color(255, 165, 0))
    RED: DifficultyValue = DifficultyValue("RED", Color(255, 0, 0))
    SKULL: DifficultyValue = DifficultyValue("SKULL", Color(34,34,34))
    
    @staticmethod
    def compute(level: Level, target_level: Level):
        difficulty: Difficulty = None
        level_delta: int = target_level.value - level.value
        if (level_delta >= 11):
            difficulty = Difficulty.SKULL
        elif (6 <= level_delta <= 10):
            difficulty = Difficulty.RED
        elif (4 <= level_delta <= 5):
            difficulty = Difficulty.ORANGE
        elif (level_delta >= 3):
            difficulty = Difficulty.YELLOW
        elif (-2 <= level_delta <= 2):
            difficulty = Difficulty.GREEN
        else:
            difficulty = Difficulty.GREY
        return difficulty