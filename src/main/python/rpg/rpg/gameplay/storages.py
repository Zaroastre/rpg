from rpg.objects import Object
from rpg.gameplay.qualities import QualityType

class Slot:
    def __init__(self) -> None:
        self.__object: Object = None
    @property
    def object(self) -> Object:
        return self.__object

    @property
    def is_empty(self)->bool:
        return self.__object is None

    def set(self, object_to_add: Object):
        if (self.__object is None):
            self.__object = object_to_add
    
    def clear(self):
        self.__object = None
      
class Storage(Object):
    def __init__(self, name: str, capacity: int, quality: QualityType) -> None:
        super().__init__(name, None, quality)
        self.__maximum_capacity: int = capacity
        self.__slots: list[Slot] = []
        for _ in range(self.__maximum_capacity):
            self.__slots.append(Slot())
    
    @property
    def capacity(self) -> int:
        return self.__maximum_capacity
    
    @property
    def objects(self) -> list[Object]:
        return [slot.object for slot in self.__slots if not slot.is_empty]
    
    def add(self, object_to_add: Object):
        if (object_to_add is not None):
            for slot in self.__slots:
                if (slot.is_empty):
                    slot.set(object_to_add)
                    break

    def remove(self, object_to_remove: Object):
        if (object_to_remove is not None):
            for slot in self.__slots:
                if (slot.object == object_to_remove):
                    slot.clear()
                    break

    def clear(self):
        for slot in self.__slots:
            slot.clear()

class LittleSatchel(Storage):
    def __init__(self) -> None:
        super().__init__("Little Satchel", 5, QualityType.POOR)

class LargeSatchel(Storage):
    def __init__(self) -> None:
        super().__init__("Large Satchel", 10, QualityType.COMMON)

class HandBag(Storage):
    def __init__(self) -> None:
        super().__init__("Hand Bag", 20, QualityType.UNCOMMON)

class BackBag(Storage):
    def __init__(self) -> None:
        super().__init__("Back Bag", 40, QualityType.RARE)
    