from threading import Thread
from rpg.characters import Character, Enemy
from rpg.gameplay.attack_strategy import AttackStategy, AttackStategyChooser, InstantDamageSpellAttackStrategy, PeriodicDamageSpellAttackStrategy
from rpg.gamedesign.message_system import MessageBroker
from time import sleep

class Fight(Thread):
    def __init__(self, attacker: Character, target: Character) -> None:
        super().__init__()
        self.__attacker: Character = attacker
        self.__target: Character = target
        self.__must_fight: bool = False
        self.__attack_strategy_chooser: AttackStategyChooser = AttackStategyChooser(self.__attacker)
        self.__message_broker: MessageBroker = MessageBroker()
        self.__message_broker.add_debug_message(self.name + " - " + attacker.name + " will fight " + target.name)
        self.__attacker.is_in_fight_mode = True
        
    def run(self) -> None:
        self.__attacker.set_stay_in_place_mode()
        self.__target.set_stay_in_place_mode()
        self.__must_fight = True
        attack_strategy: AttackStategy = None
        self.__attacker.is_in_fight_mode = True
        while (self.__must_fight and self.__attacker.life.is_alive() and self.__target.life.is_alive()):
            attack_strategy = self.__attack_strategy_chooser.choose_best_attack_strategy(self.__target)
            self.__attacker.set_attack_strategy(attack_strategy)
            generated_threat: int = self.__attacker.attack(self.__target)
            if (isinstance(attack_strategy, InstantDamageSpellAttackStrategy)):
                self.__attacker.character_class.resource.loose(attack_strategy.spell.resource_usage)
            elif (isinstance(attack_strategy, PeriodicDamageSpellAttackStrategy)):
                self.__attacker.character_class.resource.loose(attack_strategy.spell.resource_usage)
            self.__attacker.threat.increase(generated_threat)
            attack_speed: float = self.__attacker.attack_speed
            if (self.__attacker.character_class.right_hand_weapon is not None):
                attack_speed = self.__attacker.character_class.right_hand_weapon.attack_speed / ((1/100)+1)
            sleep(attack_speed)
        if (self.__attacker.life.is_dead()):
            self.__message_broker.add_debug_message(self.name + " - " + self.__attacker.name + " the attacker is dead")
        if (self.__target.life.is_dead()):
            self.__message_broker.add_debug_message(self.name + " - " + self.__target.name + " the target is dead")
        self.__message_broker.add_debug_message(self.name + " - " + self.__attacker.name + " stop to attack " + self.__target.name)
        self.__attacker.is_in_fight_mode = False

    def stop(self):
        self.__message_broker.add_debug_message(self.name + " - " + self.__attacker.name + " must stoped to attack " + self.__target.name)
        self.__must_fight = False
        self.__attacker.is_in_fight_mode = False