from threading import Thread
from time import sleep
from datetime import datetime
from abc import abstractmethod
from math import sqrt
from colorama import Fore, init
import functools
import logging
from random import randint

init(autoreset=True)

def log(function):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(function.__name__)
        logger.setLevel(logging.INFO)

        # Configuration du format du message de log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Configuration du gestionnaire de log vers la console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Ajout du message de log
        logger.info(f"Calling function {function.__name__} with arguments {args} and keyword arguments {kwargs}")

        # Appel de la fonction d'origine
        result = function(*args, **kwargs)

        # Ajout du message de log après l'appel de la fonction
        logger.info(f"Function {function.__name__} returned {result}")

        return result

class Life:
    """Class that represent the life of a game entity like a player or a NPC.
    """
    def __init__(self, maximum_life_points: int) -> None:
        self.__current: int = maximum_life_points
        self.__maximum: int = maximum_life_points

    @property
    def current(self) -> int:
        """Current life points left.

        Returns:
            int: Life points left.
        """
        return self.__current
    @property
    def maximum(self) -> int:
        """Maximum life points.

        Returns:
            int: Life points
        """
        return self.__maximum
    
    def is_alive(self) -> bool:
        """Check is the life is alive.

        Returns:
            bool: True if alive, else False if dead.
        """
        return self.__current > 0

    def is_dead(self) -> bool:
        """Check is the life is dead.

        Returns:
            bool: True if dead, else False if alive.
        """
        return not self.is_alive()

    def die(self):
        """Set life points to 0.
        """
        self.__current = 0

    def loose(self, points: int):
        """Loose life points.

        Args:
            points (int): Life points to loose.
        """
        if (points > 0):
            self.__current -= points
            if (self.__current <= 0):
                self.die()

    def heal(self, points: int):
        """Win life points.

        Args:
            points (int): Life points to win.
        """
        if (points > 0):
            self.__current += points
            if (self.__current > self.__maximum):
                self.__current = self.__maximum

class CharactersRegistry:
    characters: list[Character] = []

class Spell:
    """Interface that represents a spell.
    """
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int) -> None:
        self.__minimum_effect: int = minimum_effect
        self.__maximum_effect: int = maximum_effect
        self.__cooldown_in_ms: int = cooldown_in_ms

    @property
    def minimum_effect(self) -> int:
       return self.__minimum_effect
    @property
    def maximum_effect(self) -> int:
       return self.__maximum_effect
    @property
    def cooldown_in_ms(self) -> int:
       return self.__cooldown_in_ms


    @abstractmethod
    def cast(self, target: Character):
        """Cast the spell on the target.

        Args:
            target (Life): The target that must be impected by the spell effect.
        """
        raise NotImplementedError()
    
    def cancel(self):
        """Cancel the spell effect.
        """
        pass

class DamageSpell(Spell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
    
    @property
    def damage(self) -> int:
        return randint(self.minimum_effect, self.maximum_effect)

    def cast(self, target: Character):
        target.suffer_damage(self.damage)

class DirectDamageSpell(DamageSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)

    def cast(self, target: Character):
        super().cast(target)

    @staticmethod
    def of_rank(rank: int) -> 'DirectDamageSpell':
        return DirectDamageSpell(rank, rank*2, 1_000)

class PeriodicDamageThread(Thread):
    """Class that represents a periodic spell effect causing damages.
    """
    def __init__(self, target: Character, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, interval_is_ms: int, duration_is_ms: int):
        super().__init__()
        self.__target: Character = target
        self.__minimum_effect: int = minimum_effect
        self.__maximum_effect: int = maximum_effect
        self.__cooldown_in_ms: int = cooldown_in_ms
        self.__interval_is_ms: int = interval_is_ms
        self.__duration_is_ms: int = duration_is_ms
        self.__must_apply_effect: bool = False


    def run(self):
        self.__must_apply_effect = True
        cast_time_in_ms: datetime = datetime.now().timestamp() * 1000
        while (self.__must_apply_effect):
            points: int = randint(self.__minimum_effect, self.__maximum_effect)
            self.__target.suffer_damage(points)
            sleep(self.__interval_is_ms/1000)
            now_in_ms = datetime.now().timestamp() * 1000
            self.__must_apply_effect = (now_in_ms < (cast_time_in_ms + self.__duration_is_ms))
        print(self.__target.life.current)

    def terminate(self):
        self.__must_apply_effect = False

class PeriodicDamageSpell(DirectDamageSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, interval_is_ms: int, duration_is_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
        self.__damage_thread: PeriodicDamageThread|None = None
        self.__interval_is_ms: int = interval_is_ms
        self.__duration_is_ms: int = duration_is_ms

    def cast(self, target: Character):
        if ((self.__damage_thread is None) or (not self.__damage_thread.is_alive())):
            self.__damage_thread = PeriodicDamageThread(target, self.minimum_effect, self.maximum_effect, self.cooldown_in_ms, self.__interval_is_ms, self.__duration_is_ms)
            self.__damage_thread.start()
    
    def cancel(self):
        if (self.__damage_thread is not None):
            self.__damage_thread.terminate()

    @staticmethod
    def of_rank(rank: int) -> 'PeriodicDamageSpell':
        return PeriodicDamageSpell(rank, rank*2, 1_000, 200, 5_000)
class AreaSpell:
    @abstractmethod
    def apply_effect_on_area(self, position: Position):
        raise NotADirectoryError()

class AreaDirectDamageSpell(DirectDamageSpell, AreaSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, radius_effect_in_meter: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
        self.__radius_effect_in_meter: int = radius_effect_in_meter

    def apply_effect_on_area(self, position: Position):
        for character in CharactersRegistry.characters:
            if (Geometry.is_point_in_circle(character.tracker.position, position, self.__radius_effect_in_meter)):
                self.cast(character)

    @staticmethod
    def of_rank(rank: int) -> 'AreaDirectDamageSpell':
        return AreaDirectDamageSpell(rank, rank*2, 1_000, 100)

class AreaPeriodicDamageSpell(PeriodicDamageSpell, AreaSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, radius_effect_in_meter: int, interval_is_ms: int, duration_is_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms, interval_is_ms, duration_is_ms)
        self.__radius_effect_in_meter: int = radius_effect_in_meter

    def apply_effect_on_area(self, position: Position):
        for character in CharactersRegistry.characters:
            if (Geometry.is_point_in_circle(character.tracker.position, position, self.__radius_effect_in_meter)):
                self.cast(character)

    @staticmethod
    def of_rank(rank: int) -> 'AreaPeriodicDamageSpell':
        return AreaPeriodicDamageSpell(rank, rank*2, 1_000, 100, 250, 2_000)

class HealSpell(Spell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
    
    @property
    def heal(self) -> int:
        return randint(self.minimum_effect, self.maximum_effect)

    def cast(self, target: Character):
        target.life.heal(self.heal)

class DirectHealSpell(HealSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)

    def cast(self, target: Character):
        super().cast(target)

    @staticmethod
    def of_rank(rank: int) -> 'DirectHealSpell':
        return DirectHealSpell(rank, rank*2, 1_000)

class PeriodicHealThread(Thread):
    def __init__(self, target: Character, points: int, interval_is_ms: int, duration_is_ms: int):
        self.__target: Character = target
        self.__points: int = points
        self.__interval_is_ms: int = interval_is_ms
        self.__duration_is_ms: int = duration_is_ms
        self.__must_apply_effect: bool = False

    def run(self):
        self.__must_apply_effect = True
        cast_time_in_ms: datetime = datetime.now().timestamp() * 1000
        while (self.__must_apply_effect):
            self.__target.life.heal(self.__points)
            sleep(self.__interval_is_ms/1000)
            now_in_ms = datetime.now().timestamp() * 1000
            self.__must_apply_effect = (now_in_ms < (cast_time_in_ms + self.__duration_is_ms))

    def terminate(self):
        self.__must_apply_effect = False

class PeriodicHealSpell(DirectHealSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, interval_is_ms: int, duration_is_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
        self.__heal_thread: PeriodicHealThread|None = None
        self.__interval_is_ms: int = interval_is_ms
        self.__duration_is_ms: int = duration_is_ms

    def cast(self, target: Character):
        if ((self.__heal_thread is None) or (not self.__heal_thread.is_alive())):
            self.__heal_thread = PeriodicHealThread(target, self.heal, self.__interval_is_ms, self.__duration_is_ms)
            self.__heal_thread.start()
    
    def cancel(self):
        if (self.__heal_thread is not None):
            self.__heal_thread.terminate()

    @staticmethod
    def of_rank(rank: int) -> 'PeriodicHealSpell':
        return PeriodicHealSpell(rank, rank*2, 1_000, 200, 5_000)

class AreaDirectHealSpell(DirectHealSpell, AreaSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, radius_effect_in_meter: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms)
        self.__radius_effect_in_meter: int = radius_effect_in_meter

    def apply_effect_on_area(self, position: Position):
        for character in CharactersRegistry.characters:
            if (Geometry.is_point_in_circle(character.tracker.position, position, self.__radius_effect_in_meter)):
                self.cast(character)

    @staticmethod
    def of_rank(rank: int) -> 'AreaDirectHealSpell':
        return AreaDirectHealSpell(rank, rank*2, 1_000, 100)

class AreaPeriodicHealSpell(PeriodicHealSpell, AreaSpell):
    def __init__(self, minimum_effect: int, maximum_effect: int, cooldown_in_ms: int, radius_effect_in_meter: int, interval_is_ms: int, duration_is_ms: int) -> None:
        super().__init__(minimum_effect, maximum_effect, cooldown_in_ms, interval_is_ms, duration_is_ms)
        self.__radius_effect_in_meter: int = radius_effect_in_meter

    def apply_effect_on_area(self, position: Position):
        for character in CharactersRegistry.characters:
            if (Geometry.is_point_in_circle(character.tracker.position, position, self.__radius_effect_in_meter)):
                self.cast(character)

    @staticmethod
    def of_rank(rank: int) -> 'AreaPeriodicHealSpell':
        return AreaPeriodicHealSpell(rank, rank*2, 1_000, 100, 250, 2_000)

class AI:
    def __init__(self, character: Character) -> None:
        self.__character: Character = character
        self.__fight: Fight|None = None
    
    def fight(self, targets: list[Character]):
        if (self.__fight is None):
            self.__fight = Fight(self.__character)
            self.__fight.fight(targets)

    def wait_for_fight_ended(self):
        self.__fight.join()

def main():
    me: Character = Character("Me", 100, Position(10,10))
    you: Character = Character("You", 100, Position(50,50))

    CharactersRegistry.characters.append(me)
    CharactersRegistry.characters.append(you)

    me_as_ai: AI = AI(me)
    you_as_ai: AI = AI(you)

    me_as_ai.fight([you])
    you_as_ai.fight([me])

    me_as_ai.wait_for_fight_ended()
    you_as_ai.wait_for_fight_ended()
    print("Me: " + str(me.life.current))
    print("You: " + str(you.life.current))

if (__name__ == "__main__"):
    main()