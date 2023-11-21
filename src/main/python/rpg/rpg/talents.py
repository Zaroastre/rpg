from rpg.gamedesign.progression_system import Rank

class Talent:
    def __init__(self, name: str, rank: Rank, required_talent: list[Rank] = []) -> None:
        self.__name: str = name
        self.__rank: Rank = rank
        self.__required_talents: list[Talent] = required_talent
    @property
    def name(self) -> str:
        return self.__name
    @property
    def rank(self) -> Rank:
        return self.__rank
    @property
    def required_talent(self) -> list:
        return self.__required_talents

class TalentNode:
    def __init__(self, talent: Talent, nodes: list = []) -> None:
        self.__talent: Talent = talent
        self.__nodes: list[TalentNode] = nodes
    
    @property
    def total_points(self) -> int:
        points: int = self.__talent.rank.current
        for node in self.__nodes:
            points += node.total_points
        return points
    
    @property
    def talent(self) -> Talent:
        return self.__talent
    @property
    def nodes(self) -> list:
        return self.__nodes.copy()
    
    def contains_nodes(self) -> bool:
        return (self.nodes is not None and len(self.nodes) > 0)

class TalentsTree:
    def __init__(self, name: str, nodes: list[TalentNode]) -> None:
        self.__name: str = name
        self.__roots: list[TalentNode] = nodes
    @property
    def total_points(self) -> int:
        points: int = 0
        for node in self.__roots:
            points += node.total_points
        return points
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def roots(self) -> list[TalentNode]:
        return self.__roots.copy()

class TalentsBook:
    def __init__(self, talents_trees: list[TalentsTree]) -> None:
        self.__talents_trees: dict[str, TalentsTree] = {}
        for tree in talents_trees:
            self.__talents_trees[tree.name] = tree
    
    def list_specialities(self) -> list[str]:
        return list(self.__talents_trees.keys())
    
    def get(self, name: str) -> TalentsTree:
        if (name is None or (name not in self.list_specialities())):
            raise ValueError()
        return self.__talents_trees.get(name)

class TalentsBookFactory:
    
    @staticmethod
    def paladin() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Holy",
            nodes=[
                TalentNode(
                    talent=Talent("Spiritual Force", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Seals Of The Pure", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Healing Light", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Divine Intelect", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Unyielding Faith", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Aura Mystery", Rank(1))
                ),
                TalentNode(
                    talent=Talent("Illumination", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Improved Lay On Hands", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Improved Concentration Aura", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Improved Blessing Of Wisdom", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Blessed Hands", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Pure Of Heart", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Divine Favor", Rank(1))
                ),
                TalentNode(
                    talent=Talent("Sanctified Light", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Purifying Power", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Holy Power", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Light's Grace", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Holy Shock", Rank(1))
                ),
                TalentNode(
                    talent=Talent("Blessed Life", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Sacred Cleansing", Rank(3))
                ),
                TalentNode(
                    talent=Talent("Holy Guidance", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Divine Illumination", Rank(1))
                ),
                TalentNode(
                    talent=Talent("Judgements Of The Pure", Rank(5))
                ),
                TalentNode(
                    talent=Talent("Infusion Of Light", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Enlightened Judgements", Rank(2))
                ),
                TalentNode(
                    talent=Talent("Beacon Of Light", Rank(1))
                )
            ]
        ))
        specialities.append(TalentsTree(
            "Protection",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Retribution",
            nodes=[
            ]))
        return TalentsBook(specialities)

    @staticmethod
    def demonist() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Afflication",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Demonology",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Destruction",
            nodes=[
            ]))
        return TalentsBook(specialities)
    
    @staticmethod
    def mage() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Arcane",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Fire",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Frost",
            nodes=[
            ]))
        return TalentsBook(specialities)
    
    @staticmethod
    def priest() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Discipline",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Holy",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Shadow",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def hunter() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Beast Mastery",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Markmanship",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Survival",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def shaman() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Elemental",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Enhancement",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Restoration",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def druid() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Balance",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Feral",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Guardian",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Restoration",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def demon_hunter() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Havoc",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Vengeance",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def rogue() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Assasination",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Outlaw",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Subtlety",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def monk() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Protect",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Light",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def warrior() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Arms",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Fury",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Protection",
            nodes=[
            ]))
        return TalentsBook(specialities)
    @staticmethod
    def death_knight() -> TalentsBook:
        specialities: list[TalentsTree] = []
        specialities.append(TalentsTree(
            "Blood",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Frost",
            nodes=[
            ]))
        specialities.append(TalentsTree(
            "Unholy",
            nodes=[
            ]))
        return TalentsBook(specialities)