from rpg.gamedesign.spells_system import SpellsWheel
from rpg.characters import Character
from rpg.gameplay.spells import Spell
from rpg.gameplay.storages import Storage

class Player:
    def __init__(self) -> None:
        self.__character: Character = None
        self.__spells_wheel: SpellsWheel = SpellsWheel(4, 4)
        self.__bags: list[Storage] = []
    
    @property
    def character(self)-> Character:
        return self.__character
    
    @property
    def spells_wheel(self)-> SpellsWheel:
        return self.__spells_wheel

    def __update_spells_wheel(self):
        self.__spells_wheel.reset()
        index: int = 0
        total_spells: int = len(self.__character.character_class.spells_book.spells)
        if (total_spells > 0):
            while (index < total_spells):
                spell: Spell = self.__character.character_class.spells_book.spells[index]
                self.__spells_wheel.get_selected_set().register(spell, 0, 0)
                index += 1
                if (index%len(self.__spells_wheel.get_selected_set().list()) == 0):
                    self.__spells_wheel.select_next_set()
        
    
    def set_character(self, character: Character):
        if (character is not None):
            self.__character = character
            self.__update_spells_wheel()