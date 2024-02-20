from typing import TypeVar, Generic

from rpg.ui.widgets.widgets import Widget
from rpg.colors import Color

T = TypeVar('T')

class RadioButton(Widget, Generic[T]):
    def __init__(self, text: str, value: T, width: int, height: int) -> None:
        Widget.__init__(self, width, height)
        self.__text: str = text
        self.__value: T = value
        self.__is_selected: bool = False

    @property
    def text(self) ->str:
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

class RadioButtonGroup(Widget, Generic[T]):
    def __init__(self, name: str, width: int, height: int) -> None:
        Widget.__init__(self, width, height)
        self.__name: str = name
        self.__buttons: list[RadioButton[T]] = []

    @property
    def buttons(self) -> list[RadioButton[T]]:
        return self.__buttons.copy()

    def add_radio_button(self, text: str, value: T, is_selected: bool = False):
        button: RadioButton = RadioButton(text, value, self.rect.width, self.rect.height)
        self.__buttons.append(button)
        if (is_selected):
            self.select_button(button)
    
    def select_button(self, button: RadioButton[T]):
        if (button in self.__buttons):
            for radio_button in self.__buttons:
                if (radio_button is not button):
                    radio_button.unselect()
                else:
                    radio_button.select()
    
    def update(self, *args, **kwargs) -> None:
        return super().update(*args, **kwargs)
    