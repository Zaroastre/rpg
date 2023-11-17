import pygame

from geometry import Position
from characters import Character, Group
from gameapi import InputEventHandler, Draw

class MemberPanel(InputEventHandler, Draw):
    def __init__(self, member: Character) -> None:
        self.__member: Character = member
        self.position: Position = Position(0, 0)
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 22
        self.__avatar_picture_radius: float = 40
        self.__texture: pygame.Surface = pygame.Surface([250, self.__avatar_picture_radius*2], pygame.SRCALPHA)
        self.__font: pygame.font.Font = pygame.font.Font(
            None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255, 255, 255)
        self.__title: pygame.Surface = self.__font.render(
            self.__member.name, True, self.__font_color)
        self.__current_life_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__current_resource_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__current_menace_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__life_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__resource_bar: pygame.Surface = pygame.Surface((150, 10))
        self.__menace_bar: pygame.Surface = pygame.Surface((150, 10))

    @property
    def height(self) -> float:
        return self.__avatar_picture_radius*2

    def handle(self, event: pygame.event.Event):
        self.__current_life_bar = pygame.Surface((150, 10))
        self.__current_resource_bar = pygame.Surface((150, 10))
        self.__current_menace_bar = pygame.Surface(((self.__member.menace*150)/100, 10))

    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(30,30,30))
        pygame.draw.circle(self.__texture, pygame.Color(50,50,50), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius)
        if (self.__member.is_selected()):
            pygame.draw.circle(self.__texture, pygame.Color(100,200,0), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius, 5)
        else:
            pygame.draw.circle(self.__texture, pygame.Color(200,200,200), (self.__avatar_picture_radius, self.__avatar_picture_radius), self.__avatar_picture_radius, 5)
        self.__texture.blit(self.__title, (self.__avatar_picture_radius*2, 0))

        
        self.__life_bar.fill(pygame.Color(10, 10, 10))
        self.__resource_bar.fill(pygame.Color(10, 10, 10))
        self.__menace_bar.fill(pygame.Color(10, 10, 10))
        
        self.__current_life_bar.fill(pygame.Color(50, 200, 0))
        self.__current_resource_bar.fill(pygame.Color(0, 150, 200))
        self.__current_menace_bar.fill(pygame.Color(200, 0, 0))

        self.__texture.blit(self.__life_bar, ((self.__avatar_picture_radius*2)+10, self.__font_size))
        self.__texture.blit(self.__resource_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + self.__life_bar.get_height()+10)))
        self.__texture.blit(self.__menace_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + (self.__life_bar.get_height()+10)*2)))
        
        self.__texture.blit(self.__current_life_bar, ((self.__avatar_picture_radius*2)+10, self.__font_size))
        self.__texture.blit(self.__current_resource_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + self.__life_bar.get_height()+10)))
        self.__texture.blit(self.__current_menace_bar, ((self.__avatar_picture_radius*2)+10, (self.__font_size + (self.__life_bar.get_height()+10)*2)))

        master.blit(self.__texture, (self.position.x, self.position.y))

class GroupPanel(InputEventHandler, Draw):
    def __init__(self, group: Group, width: int, height: int, position: Position) -> None:
        self.__group: Group = group
        self.__members_panels: list[MemberPanel] = []
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position
        for member in self.__group.members:
            self.__members_panels.append(MemberPanel(member=member))

    
    def handle(self, event: pygame.event.Event):
        self.__group.handle(event)
        self.__members_panels.clear()
        member_panel_position: Position = Position(0, 0)
        for member in self.__group.members:
            member_panel: MemberPanel = MemberPanel(member=member)
            member_panel.position = Position(member_panel_position.x, member_panel_position.y)
            self.__members_panels.append(member_panel)
            member_panel_position.y += member_panel.height
            member_panel.handle(event)
        self.__texture = pygame.Surface((self.__texture.get_width(), member_panel_position.y))
    
    def draw(self, master: pygame.Surface):
        self.__group.draw(master)
        self.__texture.fill(pygame.Color(0,0,0, 0))
        for member_panel in self.__members_panels:
            member_panel.draw(self.__texture)
        master.blit(self.__texture, (self.__position.x,self.__position.y))

class ActionPanel(InputEventHandler, Draw):
    def __init__(self, width: int, height: int, position: Position) -> None:
        self.character: Character = None
        self.__texture: pygame.Surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__position: Position = position

    
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        self.__texture.fill(pygame.Color(200,200,200))
        master.blit(self.__texture, (self.__position.x, self.__position.y))

