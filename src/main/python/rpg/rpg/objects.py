from rpg.gameplay.qualities import QualityType

class Object:
    def __init__(self, name: str, description: str=None, quality: QualityType=QualityType.POOR) -> None:
        self.__name: str = name
        self.__description: str = description
        self.__quality: QualityType = quality
    @property
    def name(self) -> str:
        return self.__name
    @property
    def description(self) -> str:
        return self.__description
    @property
    def quality(self) -> QualityType:
        return self.__quality