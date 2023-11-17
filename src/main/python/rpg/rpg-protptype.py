
from random import randint

import pygame

from geometry import Geometry, Position
from characters import Character, Enemy, Group
from ui import ActionPanel, GroupPanel

import constants

pygame.init()
pygame.joystick.init()

class App:
    """Class that represents the program.
    """

    def __init__(self) -> None:
        print("Starting application...")
        print("Creating window...")
        # self.screen: pygame.Surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.screen: pygame.Surface = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Sprites Motion Creator")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running: bool = True
        self.__action_panel: ActionPanel = ActionPanel(constants.ACTION_PANEL_WIDTH, constants.ACTION_PANEL_HEIGHT, constants.ACTION_PANEL_POSITION)
        self.__available_friends: Group = Group(max_capacity=10)
        self.__enemies: Group = Group(max_capacity=100)
        self.__group_of_the_player: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__group_of_the_player, width=constants.GROUP_PANEL_WIDTH, height=constants.GROUP_PANEL_HEIGHT, position=constants.GROUP_PANEL_POSITION)
        self.__played_character: Character = None
        
    def __generate_friends(self):
        for name in constants.FRIENDS_NAMES:
            friend: Character = Character(name)
            friend.position = Position(
                randint(0, constants.WINDOW_WIDTH), randint(0, constants.WINDOW_HEIGHT))
            friend.menace = 20
            self.__available_friends.add_member(friend)
        
    def __generate_enemies(self):
        for counter in range(randint(10, 100)):
            enemy: Enemy = Enemy("Vilain #" + str(counter))
            enemy.menace = 100
            enemy.zone_radius = 200
            enemy.position = Position(randint(0, constants.WINDOW_WIDTH), randint(0, constants.WINDOW_HEIGHT))
            enemy.zone_center = Position(enemy.position.x, enemy.position.y)
            self.__enemies.add_member(enemy)

    def __generate_player_character(self):
        player: Character = Character("Nicolas METIVIER")
        player.position = Position(
            randint(0, constants.WINDOW_WIDTH), randint(0, constants.WINDOW_HEIGHT))
        player.select()
        player.menace = 20.0
        self.__group_of_the_player.add_member(player)
        self.__played_character = player
    
    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.position.x < (constants.GROUP_PANEL_WIDTH + constants.GROUP_PANEL_POSITION.x)):
            character.position.x = constants.GROUP_PANEL_WIDTH + constants.GROUP_PANEL_POSITION.x
        if (character.position.x > self.screen.get_width()):
            character.position.x = self.screen.get_width()
        if (character.position.y < 0):
            character.position.y = 0
        if (character.position.y > self.screen.get_height()):
            character.position.y = self.screen.get_height()

    def __handle_interaction_and_moves_for_friends(self, group: Group):
        for member in group.members:
            others: list[Character] = [
                other for other in group.members if other is not member]
            others += self.__available_friends.members
            others += self.__enemies.members
            for other in others:
                if member.is_touching(other):
                    member.avoid_collision_with_other(other)
            if member.is_touching(self.__played_character):
                member.avoid_collision_with_other(self.__played_character)
            else:
                member.follow(self.__played_character)
            self.__prevent_character_to_disapear_from_scene(member)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        
        # if (attacking_enemy is None):
        #     self.__played_character.is_in_fight_mode = False
        
        if Geometry.compute_distance(enemy.position, enemy.zone_center) > 1:
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.zone_center.x - enemy.position.x
            direction_y = enemy.zone_center.y - enemy.position.y
            direction_length = Geometry.compute_distance(enemy.position, enemy.zone_center)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa position initiale
            enemy.position.x += direction_x * constants.RETURN_SPEED
            enemy.position.y += direction_y * constants.RETURN_SPEED

    def __prepare_enemy_to_fight(self, enemy: Enemy, target: Character):
        target.is_in_fight_mode = True
        distance_between_enemy_and_zone_center = Geometry.compute_distance(enemy.position, enemy.zone_center)
        if distance_between_enemy_and_zone_center < enemy.zone_radius:
            enemy.follow(target)
            

    def __recruit_member(self, member: Character):
        if (not self.__group_of_the_player.is_full()):
            self.__group_of_the_player.add_member(member)
            self.__available_friends.remove_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.__played_character)):
            self.__recruit_member(member)
        

    def run(self):
        
        self.__generate_player_character()
        self.__generate_friends()
        self.__generate_enemies()

        
        joystick: pygame.joystick.Joystick
        while (self.is_running):
            events: list[pygame.event.Event] = pygame.event.get()
            if (len(events) > 0):
                for event in events:
                    if (event.type == pygame.JOYDEVICEADDED):
                        joystick = pygame.joystick.Joystick(event.device_index)
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    else:
                        # HANDLE YOUR GAME HERE
                        self.__available_friends.handle(event)
                        self.__group_panel.handle(event)
                        self.__action_panel.handle(event)
            else:
                self.__available_friends.handle(None)
                self.__group_panel.handle(None)
                self.__action_panel.handle(None)
            
            self.__played_character = [character for character in self.__group_of_the_player.members if character.is_selected()][0]
            self.__action_panel.character = self.__played_character
            if (self.__played_character.is_moving):
                for member in self.__available_friends.members:
                    self.__recruit_member_if_is_touching(member)

            self.__handle_interaction_and_moves_for_friends(self.__group_of_the_player)

            for enemy in self.__enemies.members:
                if (enemy.is_feel_threatened(self.__played_character)):
                    self.__prepare_enemy_to_fight(enemy, self.__played_character)
                else:
                    self.__move_enemy_to_the_default_observation_position(enemy)
            self.screen.fill(constants.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            self.__enemies.draw(self.screen)
            self.__available_friends.draw(self.screen)
            self.__group_panel.draw(self.screen)
            self.__action_panel.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(constants.FRAMES_PER_SECOND)
        pygame.quit()

    @staticmethod
    def main():
        app: App = App()
        app.run()


if (__name__ == "__main__"):
    App.main()
