from abc import abstractmethod
from random import randint
from enum import Enum
from pathlib import Path

class Distance(Enum):
    IN_CONTACT=1
    NEAR=5
    FAR=10
    TOO_FAR=20

class Power(Enum):
    FULL=100
    VERY_HIGH=90
    HIGH=80
    HALF=50
    LOW=20
    VERY_LOW=10
    EMPTY=0

class Action(Enum):
    CAST_SPEEL=1
    FIGHT_WITH_WAND=2
    FIGHT_WITH_WEAPON=3
    DEFAULT_FIGHT=4

class SpellType(Enum):
    INSTANT_CAST_FOR_INSTANT_DAMAGE=1
    INSTANT_CAST_FOR_PERIODIC_DAMAGE=2
    INCANTATION_CAST_FOR_INSTANT_DAMAGE=3
    INCANTATION_CAST_FOR_PERIODIC_DAMAGE=4
    INSTANT_CAST_FOR_PERIODIC_DAMAGE_ON_AREA=5
    INSTANT_CAST_FOR_INSTANT_DAMAGE_ON_AREA=6
    INCANTATION_CAST_FOR_PERIODIC_DAMAGE_ON_AREA=7
    INCANTATION_CAST_FOR_INSTANT_DAMAGE_ON_AREA=8

class Threat(Enum):
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    MANY=5

class Simulator:
    @abstractmethod
    def simulate(self):
        raise NotImplementedError()

class FightSimulator(Simulator):
    def __init__(self) -> None:
        self.__data: dict[str, list[str]] = {}
        self.__data["distance"] = list(v.name for v in Distance)
        self.__data["power"] = list(v.name for v in Power)
        self.__data["has_weapon"] = [True, False]
        self.__data["has_wand"] = [True, False]
        self.__data["action"] = list(v.name for v in Action)
        self.__data["spell"] = list(v.name for v in SpellType)
        self.__data["attackers"] = list(v.name for v in Threat)
    
    def __simulate_far_attack(self, distance: Distance):
        has_weapon: bool = self.__data.get("has_weapon")[randint(0, len(self.__data.get("has_weapon"))-1)]
        has_wand: bool = self.__data.get("has_wand")[randint(0, len(self.__data.get("has_wand"))-1)]
        power_left: Power = Power[self.__data.get("power")[randint(0, len(self.__data.get("power"))-1)]]
        attackers: Threat = Threat[self.__data.get("attackers")[randint(0, len(self.__data.get("attackers"))-1)]]
        simulation: tuple|None = None
        if (power_left in [Power.FULL, Power.HIGH, Power.MEDIUM]):
            spell: SpellType
            if (attackers == Threat.ONE):
                one_target_spells = list(spell for spell in self.__data.get("spell") if "area" not in spell.lower())
                spell = SpellType[one_target_spells[randint(0, len(one_target_spells)-1)]]
            else:
                spell = SpellType[self.__data.get("spell")[randint(0, len(self.__data.get("spell"))-1)]]
            simulation = (distance, power_left, has_weapon, has_wand, Action.CAST_SPEEL, None, attackers)
        else:
            if (has_wand):
                simulation = (distance, power_left, has_weapon, has_wand, Action.FIGHT_WITH_WAND, None, attackers)
        return simulation
    
    def __simulate_near_attack(self, distance: Distance) -> tuple|None:
        has_weapon: bool = self.__data.get("has_weapon")[randint(0, len(self.__data.get("has_weapon"))-1)]
        has_wand: bool = self.__data.get("has_wand")[randint(0, len(self.__data.get("has_wand"))-1)]
        power_left: Power = Power[self.__data.get("power")[randint(0, len(self.__data.get("power"))-1)]]
        attackers: Threat = Threat[self.__data.get("attackers")[randint(0, len(self.__data.get("attackers"))-1)]]
        simulation: tuple|None = None
        if (power_left in [Power.FULL, Power.HIGH, Power.MEDIUM]):
            spell: SpellType
            if (attackers == Threat.ONE):
                one_target_spells = list(spell for spell in self.__data.get("spell") if "area" not in spell.lower())
                spell = SpellType[one_target_spells[randint(0, len(one_target_spells)-1)]]
            else:
                spell = SpellType[self.__data.get("spell")[randint(0, len(self.__data.get("spell"))-1)]]
            simulation = (distance, power_left, has_weapon, has_wand, Action.CAST_SPEEL, spell, attackers)
        else:
            if (has_wand):
                simulation = (distance, power_left, has_weapon, has_wand, Action.FIGHT_WITH_WAND, None, attackers)
        return simulation

    def __simulate_in_contact_attack(self, distance: Distance) -> tuple|None:
        has_weapon: bool = self.__data.get("has_weapon")[randint(0, len(self.__data.get("has_weapon"))-1)]
        has_wand: bool = self.__data.get("has_wand")[randint(0, len(self.__data.get("has_wand"))-1)]
        power_left: Power = Power[self.__data.get("power")[randint(0, len(self.__data.get("power"))-1)]]
        attackers: Threat = Threat[self.__data.get("attackers")[randint(0, len(self.__data.get("attackers"))-1)]]
        simulation: tuple|None = None
        if (has_weapon):
            simulation = (distance, power_left, has_weapon, has_wand, Action.FIGHT_WITH_WEAPON, None, attackers)
        else:
            simulation = (distance, power_left, has_weapon, has_wand, Action.DEFAULT_FIGHT, None, attackers)
        return simulation
    
    def simulate(self):
        total_simulation: int = 1_000_000
        simulations_data_file: Path = Path("./ia-magic-fight.csv")
        with open(simulations_data_file, 'w') as file:
            # file.write("")
            file.write(",".join(list(self.__data.keys())))
            for _ in range(total_simulation):
                random_distance: Distance = Distance[self.__data.get("distance")[randint(0, len(self.__data.get("distance"))-1)]]
                simulation: tuple = None
                match(random_distance):
                    case Distance.FAR:
                        simulation = self.__simulate_far_attack(random_distance)
                    case Distance.NEAR:
                        simulation = self.__simulate_near_attack(random_distance)
                    case Distance.FAR:
                        simulation = self.__simulate_in_contact_attack(random_distance)
                if (simulation is not None):
                    file.write("\n")
                    spell = 0 if simulation[5] is None else simulation[5].value
                    simulation_as_numeric: list[str] = [
                        str(simulation[0].value),
                        str(simulation[1].value),
                        str(int(simulation[2])),
                        str(int(simulation[3])),
                        str(simulation[4].value),
                        str(spell),
                        str(simulation[6].value)
                    ]
                    file.write(",".join(list(simulation_as_numeric)))
class Program:
    @staticmethod
    def main():
        simulator: Simulator = FightSimulator()
        simulator.simulate()

if (__name__ == "__main__"):
    Program.main()