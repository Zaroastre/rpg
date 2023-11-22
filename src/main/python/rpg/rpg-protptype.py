import pygame

import rpg.constants
from rpg.characters import Character, Enemy
from rpg.gamedesign.interval_system import Range
from rpg.gamengine import GameGenerator
from rpg.math.geometry import Geometry
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.ui.components import CharacterComponent, EnemyComponent
from rpg.ui.graphics import ActionPanel, ExperiencePanel, GroupPanel, SpellDetailPopup
from rpg.configuration import Configuration
from rpg.gameplay.player import Player

pygame.init()
pygame.joystick.init()

class App:
    """Class that represents the program.
    """

    def __init__(self) -> None:
        print("Starting application...")
        print("Creating window...")
        self.__configuration: Configuration = Configuration()
        self.screen: pygame.Surface
        if (self.__configuration.fullscreen):
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.__configuration.window_width, self.__configuration.window_height))
        pygame.display.set_caption("World Of Nemesys")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running: bool = True
        self.__action_panel: ActionPanel = ActionPanel(rpg.constants.ACTION_PANEL_WIDTH, rpg.constants.ACTION_PANEL_HEIGHT, rpg.constants.ACTION_PANEL_POSITION)
        self.__experience_panel: ExperiencePanel = ExperiencePanel(rpg.constants.EXPERIENCE_PANEL_WIDTH, rpg.constants.EXPERIENCE_PANEL_HEIGHT, rpg.constants.EXPERIENCE_PANEL_POSITION)
        self.__available_friends: Group = Group(max_capacity=10)
        self.__enemies: Group = Group(max_capacity=100)
        self.__group_of_the_player: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__group_of_the_player, width=rpg.constants.GROUP_PANEL_WIDTH, height=rpg.constants.GROUP_PANEL_HEIGHT, position=rpg.constants.GROUP_PANEL_POSITION)
        self.__heroes_components: list[CharacterComponent] = []
        self.__vilains_components: list[EnemyComponent] = []
        self.__joystick: pygame.joystick.Joystick = None
        self.__spell_detail_popup: SpellDetailPopup = None
        self.__initialize_events_listeners()
        self.__player: Player = Player()
    
    def __initialize_events_listeners(self):
        self.__action_panel.on_spell_slot_hover(self.__handle_on_spell_slot_hover)
        self.__action_panel.on_spell_slot_press(self.__handle_on_spell_slot_press)
        self.__action_panel.on_spell_slot_release(self.__handle_on_spell_slot_release)
        self.__action_panel.on_spell_slot_leave(self.__handle_on_spell_slot_leave)
    
    def __handle_on_spell_slot_hover(self, spell: Spell):
        if (spell is not None):
            self.__spell_detail_popup = SpellDetailPopup(spell, self.__player.character.character_class, rpg.constants.SPELL_POPUP_WIDTH, rpg.constants.SPELL_POPUP_HEIGHT, rpg.constants.SPELL_POPUP_POSITION)
    
    def __handle_on_spell_slot_press(self):
        if (self.__spell_detail_popup is not None):
            pass
    
    def __handle_on_spell_slot_release(self):
        if (self.__spell_detail_popup is not None):
            pass

    def __handle_on_spell_slot_leave(self):
        self.__spell_detail_popup = None
        
    def __generate_friends(self):
        for _ in range(Range(4,10).random()):
            friend: Character = GameGenerator.generate_random_player()
            friend.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            friend.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            friend.threat.increase(20)
            self.__available_friends.add_member(friend)
            self.__heroes_components.append(CharacterComponent(friend))
        
    def __generate_enemies(self):
        for _ in range(Range(100, 100).random()):
            enemy: Enemy = GameGenerator.generate_random_enemy()
            enemy.threat.increase(100.0)
            enemy.zone_radius = 200
            enemy.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            enemy.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            enemy.zone_center = enemy.get_position().copy()
            self.__enemies.add_member(enemy)
            self.__vilains_components.append(EnemyComponent(enemy))

    def __generate_player_character(self):
        player: Character = GameGenerator.create_friend("Nicolas METIVIER", GameGenerator.generate_random_breed(), GameGenerator.generate_random_class())
        player.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
        player.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
        player.select()
        player.level.experience.gain(50)
        player.threat.increase(20.0)
        self.__group_of_the_player.add_member(player)
        self.__player.set_character(player)
        self.__heroes_components.append(CharacterComponent(player))
    
    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.get_position().x < (rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x)):
            character.get_position().x = rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x
        if (character.get_position().x > self.screen.get_width()):
            character.get_position().x = self.screen.get_width()
        if (character.get_position().y < 0):
            character.get_position().y = 0
        if (character.get_position().y > self.screen.get_height()):
            character.get_position().y = self.screen.get_height()

    def __handle_interaction_and_moves_for_friends(self, group: Group):
        for friend in group.members:
            others: list[Character] = [other for other in group.members if other is not friend]
            others += self.__available_friends.members
            others += self.__enemies.members
            for other in others:
                if friend.is_touching(other):
                    friend.avoid_collision_with_other(other)
            if friend.is_touching(self.__player.character):
                friend.avoid_collision_with_other(self.__player.character)
            else:
                friend.follow(self.__player.character)
            self.__prevent_character_to_disapear_from_scene(friend)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        
        # if (attacking_enemy is None):
        #     self.__player.character.is_in_fight_mode = False
        
        if Geometry.compute_distance(enemy.get_position(), enemy.zone_center) > 1:
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.zone_center.x - enemy.get_position().x
            direction_y = enemy.zone_center.y - enemy.get_position().y
            direction_length = Geometry.compute_distance(enemy.get_position(), enemy.zone_center)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa position initiale
            enemy.get_position().x += direction_x * rpg.constants.RETURN_SPEED
            enemy.get_position().y += direction_y * rpg.constants.RETURN_SPEED

    def __prepare_enemy_to_fight(self, enemy: Enemy, target: Character):
        target.is_in_fight_mode = True
        distance_between_enemy_and_zone_center = Geometry.compute_distance(enemy.get_position(), enemy.zone_center)
        if distance_between_enemy_and_zone_center < enemy.zone_radius:
            enemy.follow(target)

    def __recruit_member(self, member: Character):
        if (not self.__group_of_the_player.is_full()):
            self.__group_of_the_player.add_member(member)
            self.__available_friends.remove_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.__player.character)):
            self.__recruit_member(member)

    def __draw_hud(self, master: pygame.Surface):
        self.__group_panel.draw(master)
        self.__action_panel.draw(master)
        self.__experience_panel.draw(master)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.draw(master)

    def __draw_scene(self, master: pygame.Surface):
        # RENDER YOUR GAME HERE
        # self.__enemies.draw(self.screen)
        # self.__available_friends.draw(self.screen)
        for component in self.__heroes_components:
            component.draw(master)
        for component in self.__vilains_components:
            component.draw(master)

    def __handle(self):
        events: list[pygame.event.Event] = pygame.event.get()
        if (len(events) > 0):
            for event in events:
                if (event.type == pygame.JOYDEVICEADDED):
                    self.__joystick = pygame.joystick.Joystick(event.device_index)
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    # HANDLE YOUR GAME HERE
                    for component in self.__heroes_components:
                        component.handle(event)
                    for component in self.__vilains_components:
                        component.handle(event)
                    # self.__available_friends.handle(event)
                    self.__group_panel.handle(event)
                    self.__action_panel.handle(event)
                    self.__experience_panel.handle(event)
                    if (self.__spell_detail_popup is not None):
                        self.__spell_detail_popup.handle(event)
        else:
            # self.__available_friends.handle(None)
            self.__group_panel.handle(None)
            self.__action_panel.handle(None)
            self.__experience_panel.handle(None)
            if (self.__spell_detail_popup is not None):
                self.__spell_detail_popup.handle(None)
            for component in self.__heroes_components:
                component.handle(None)
            for component in self.__vilains_components:
                component.handle(None)
        
        self.__player.set_character([character for character in self.__group_of_the_player.members if character.is_selected()][0])
        self.__action_panel.set_character(self.__player.character)
        self.__action_panel.set_spells_wheel(self.__player.spells_wheel)
        self.__initialize_events_listeners()
        self.__experience_panel.set_character(self.__player.character)
        if (self.__player.character.is_moving):
            for member in self.__available_friends.members:
                self.__recruit_member_if_is_touching(member)

        self.__handle_interaction_and_moves_for_friends(self.__group_of_the_player)

        for enemy in self.__enemies.members:
            if (enemy.is_feel_threatened(self.__player.character)):
                self.__prepare_enemy_to_fight(enemy, self.__player.character)
            else:
                self.__move_enemy_to_the_default_observation_position(enemy)

        
    def __draw(self):
        self.screen.fill(rpg.constants.BACKGROUND_COLOR)
        self.__draw_scene(self.screen)
        self.__draw_hud(self.screen)

    def run(self):
        self.__generate_player_character()
        self.__generate_friends()
        self.__generate_enemies()
        self.__initialize_events_listeners()

        while (self.is_running):
            self.__handle()
            self.__draw()
            pygame.display.flip()
            self.clock.tick(self.__configuration.frames_per_second)
        pygame.quit()

    @staticmethod
    def main():
        app: App = App()
        app.run()


if (__name__ == "__main__"):
    App.main()
