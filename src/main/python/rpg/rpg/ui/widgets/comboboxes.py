from typing import TypeVar, Generic
from rpg.ui.widgets.widgets import Widget

T = TypeVar('T')

class CombobxItem(Widget, Generic[T]):
    def __init__(self, text: str, value: T, width: int, height: int) -> None:
        Widget.__init__(self, width, height)
        self.__text: str = text
        self.__value: T = value
        self.__is_selected: bool = False
    @property
    def text(self) -> str:
        return self.__text
    @property
    def value(self) -> T:
        return self.__value

    def select(self):
        self.__is_selected = True

    def unselect(self):
        self.__is_selected = False

    @property
    def is_selected(self) -> bool:
        return self.__is_selected

class Combobox(Widget, Generic[T]):
    def __init__(self, placeholder: str, width: int, height: int) -> None:
        Widget.__init__(self, width, height)
        self.__placeholder: str = placeholder
        self.__items: list[CombobxItem[T]] = []
        self.total_items_to_show: int = 10
    
    def select_item(self, item: CombobxItem[T]):
        if (item in self.__items):
            for combobox_item in self.__items:
                if (combobox_item is item):
                    combobox_item.select()
                else:
                    combobox_item.unselect()

    def add_item(self, text: str, value: T, is_selected: bool = False):
        combobox_item: CombobxItem = CombobxItem(text, value, self.rect.width, self.rect.height)
        self.__items.append(combobox_item)
        if (is_selected):
            self.select_item(combobox_item)

    @property
    def items(self) -> list[CombobxItem[T]]:
        return self.__items.copy()
