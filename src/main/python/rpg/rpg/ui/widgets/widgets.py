from pygame.sprite import Sprite
from pygame import Surface, Rect, SRCALPHA

class Widget(Sprite):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.image: Surface = Surface((width, height), SRCALPHA)
        self.rect: Rect = self.image.get_rect()