from rpg.resources import Resource, Mana

class Class:
    def __init__(self, resource: Resource) -> None:
        self.__resource: Resource = resource
    
    @property
    def resource(self) -> Resource:
        return self.__resource

class Paladin(Class):
    def __init__(self) -> None:
        super().__init__(Mana())
