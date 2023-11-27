from threading import Thread
from rpg.characters import Character
from time import sleep

class Fight(Thread):
    def __init__(self, attacker: Character, target: Character) -> None:
        super().__init__()
        self.__attacker: Character = attacker
        self.__target: Character = target
        self.__must_fight: bool = False
        print("Hum?")
        
    def run(self) -> None:
        self.__must_fight = True
        while (self.__must_fight and (self.__attacker.life.is_alive() or self.__target.life.is_alive())):
            self.__attacker.attack(self.__target)
            sleep(0.1)
    
    def stop(self):
        self.__must_fight = False