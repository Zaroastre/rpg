from abc import ABC

from rpg.characters import Character

class Team(ABC):
    def __init__(self, leader: Character, max_capacity: int) -> None:
        self._leader: Character = leader
        self._max_capacity: int = max_capacity
    
    @property
    def leader(self) -> Character:
        return self._leader

    @property
    def capacity(self) -> int:
        return self._max_capacity

class Group(Team):
    def __init__(self, max_capacity: int, leader: Character=None) -> None:
        super().__init__(leader, max_capacity=max_capacity)
        self.__members: list[Character] = []
        if (leader is not None):
            self.__members.append(self._leader)

    @property
    def members(self) -> list[Character]:
        return self.__members

    def add_member(self, new_member: Character):
        if (len(self.__members) < self._max_capacity):
            if (len(self.__members) == 0):
                self._leader = new_member
            self.__members.append(new_member)

    def is_full(self) -> bool:
        return len(self.__members) == self._max_capacity

    def remove_member(self, member_to_remove: Character):
        if (member_to_remove in self.__members):
            self.__members.remove(member_to_remove)
            if (self._leader == member_to_remove):
                self._leader = None
            if (len(self.__members) > 0):
                self._leader = self.__members[0]


class Raid(Team):
    def __init__(self, leader: Character) -> None:
        super().__init__(leader, max_capacity=40)
        self.__groups: list[Group] = []
