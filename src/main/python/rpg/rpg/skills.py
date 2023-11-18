class Rank:
    def __init__(self, maximum: int) -> None:
        self.__current: int = 0
        self.__maximum: int = maximum
    @property
    def current(self) -> int:
        return self.__current
    @property
    def maximum(self) -> int:
        return self.__maximum

class Skill:
    def __init__(self, name: str, rank: Rank, required_skill: list[Rank] = []) -> None:
        self.__name: str = name
        self.__rank: Rank = rank
        self.__required_skills: list[Skill] = required_skill
    @property
    def name(self) -> str:
        return self.__name
    @property
    def rank(self) -> Rank:
        return self.__rank
    @property
    def required_skill(self) -> list[Rank]:
        return self.__required_skills

class SkillNode:
    def __init__(self, skill: Skill, nodes: list = []) -> None:
        self.__skill: Skill = skill
        self.__nodes: list[SkillNode] = nodes
    
    @property
    def skill(self) -> Skill:
        return self.__skill
    @property
    def nodes(self) -> list:
        return self.__nodes
    
    def contains_nodes(self) -> bool:
        return (self.nodes is not None and len(self.nodes) > 0)

class SkillsTree:
    def __init__(self, name: str, nodes: list[SkillNode]) -> None:
        self.__name: str = name
        self.__roots: list[SkillNode] = nodes
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def roots(self) -> list[SkillNode]:
        return self.__roots