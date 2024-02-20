from typing import TypeVar, Generic
from rpg.ui.widgets.widgets import Widget
import pygame


T = TypeVar('T')

class Button(Widget):
    def __init__(self, text: str, width: int, height: int) -> None:
        Widget.__init__(self, width, height)
        self.__text: str = text
        self.__on_click: callable|None = None

    @property
    def text(self) -> str:
        return self.__text

    def add_event_listern_on_click(self, callback: callable):
        self.__on_click = callback
    
    def click(self):
        if (self.__on_click is not None):
            self.__on_click()