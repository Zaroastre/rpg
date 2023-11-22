from rpg.gameplay.spells import Spell

class SpellsSet:
    def __init__(self, total_spells: int) -> None:
        self.__maximum_spells: int = total_spells
        self.__spells: list[Spell] = []
        for _ in range(self.__maximum_spells):
            self.__spells.append(None)
        self.__keyboard_bidings: dict[int, Spell] = {}
        self.__gamepad_bidings: dict[int, Spell] = {}
        self.__is_selected: bool = False
    @property
    def is_selected(self) -> bool:
        return self.__is_selected
    def select(self):
        self.__is_selected = True
    def unselect(self):
        self.__is_selected = False
        

    def list(self) -> list[Spell]:
        return self.__spells.copy()

    def register(self, spell: Spell, keyboard_key: int, gamepad_button: int):
        if (spell not in self.__spells):
            for index in range(len(self.__spells)):
                if (self.__spells[index] == None):
                    self.__spells[index] = spell
                    self.__keyboard_bidings[keyboard_key] = spell
                    self.__gamepad_bidings[gamepad_button] = spell
                    break

    def unregister(self, spell: Spell):
        if (spell in self.__spells):
            for index in range(len(self.__spells)):
                if (self.__spells[index] == spell):
                    self.__spells[index] = None
                    keys_to_remove = [k for k, v in self.__keyboard_bidings.items() if v == spell]
                    for key in keys_to_remove:
                        del self.__keyboard_bidings[key]
                    keys_to_remove = [k for k, v in self.__gamepad_bidings.items() if v == spell]
                    for key in keys_to_remove:
                        del self.__gamepad_bidings[key]
                    break

    def reset(self):
        self.__spells = [None]*self.__maximum_spells
        self.__keyboard_bidings.clear()
        self.__gamepad_bidings.clear()

class SpellsWheel:
    def __init__(self, number_of_sets: int, number_of_spells_by_set: int) -> None:
        if (number_of_sets < 1):
            raise ValueError()
        if (number_of_spells_by_set < 1):
            raise ValueError()
        self.__number_of_sets: int = number_of_sets
        self.__sets: list[SpellsSet] = []
        for _ in range(self.__number_of_sets):
            self.__sets.append(SpellsSet(number_of_spells_by_set))
        self.__sets[0].select()
        self.__index_of_selected_set: int = 0
    @property
    def sets(self) -> list[SpellsSet]:
        return self.__sets.copy()
    @property
    def number_of_sets(self) -> int:
        return self.__number_of_sets
    def select_next_set(self) -> SpellsSet:
        self.get_selected_set().unselect()
        self.__index_of_selected_set += 1
        if (self.__index_of_selected_set >= len(self.__sets)):
            self.__index_of_selected_set = 0
        self.get_selected_set().select()
        return self.get_selected_set()

    def get_selected_set(self) -> SpellsSet:
        return self.__sets[self.__index_of_selected_set]

    def select_previous_set(self) -> SpellsSet:
        self.get_selected_set().unselect()
        self.__index_of_selected_set -= 1
        if (self.__index_of_selected_set < 0):
            self.__index_of_selected_set = len(self.__sets)-1
        self.get_selected_set().select()
        return self.get_selected_set()

    def reset(self):
        for spells_set in self.__sets:
            spells_set.reset()
