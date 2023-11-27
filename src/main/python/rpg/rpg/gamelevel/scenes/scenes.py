import pygame
from rpg.gameapi import Draw, InputEventHandler
from rpg.gameplay.player import Player


class Scene(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, player: Player) -> None:
        self.__player: Player = player
        self.__width: int = width
        self.__height: int = height
        self._background_texture: pygame.Surface = pygame.Surface((self.__width, self.__height))
    
    @property
    def width(self) -> Player:
        return self.__width
    @property
    def height(self) -> Player:
        return self.__height
    @property
    def player(self) -> Player:
        return self.__player
    
    def draw(self, master: pygame.Surface):
        master.blit(self._background_texture, (0,0))
