import pygame
import rpg.constants
from rpg.characters import Character, Enemy
from rpg.gamedesign.difficulty_system import Difficulty
from rpg.gamedesign.fight_system import Fight
from rpg.gamedesign.interval_system import Range
from rpg.gamedesign.message_system import MessageBroker
from rpg.gamengine import GameGenerator
from rpg.gameplay.classes import ClassType
from rpg.gameplay.player import Player
from rpg.gameplay.spells import Spell
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry, Position
from rpg.ui.components import (CharacterComponent, EnemyComponent,
                               ProjectilComponent)
from rpg.ui.graphics import (ActionPanel, ExperiencePanel, GroupPanel,
                             MessagePanel, SpellDetailPopup)
from rpg.gamelevel.scenes.scenes import Scene

class GameScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        
        self.__action_panel: ActionPanel = ActionPanel(rpg.constants.ACTION_PANEL_WIDTH, rpg.constants.ACTION_PANEL_HEIGHT, rpg.constants.ACTION_PANEL_POSITION)
        self.__experience_panel: ExperiencePanel = ExperiencePanel(rpg.constants.EXPERIENCE_PANEL_WIDTH, rpg.constants.EXPERIENCE_PANEL_HEIGHT, rpg.constants.EXPERIENCE_PANEL_POSITION)
        self.__friends_group: Group = Group(max_capacity=5)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__friends_group, width=rpg.constants.GROUP_PANEL_WIDTH, height=rpg.constants.GROUP_PANEL_HEIGHT, position=rpg.constants.GROUP_PANEL_POSITION)
        self.__message_panel: MessagePanel = MessagePanel(width=rpg.constants.MESSAGE_PANEL_WIDTH, height=rpg.constants.MESSAGE_PANEL_HEIGHT, position=rpg.constants.MESSAGE_PANEL_POSITION)

        self.__friends_sprites: list[CharacterComponent] = []
        self.__enemies_sprites: list[EnemyComponent] = []
        
        self.__spell_detail_popup: SpellDetailPopup = None
        self.__message_broker: MessageBroker = MessageBroker()
        
        self.__fights: dict[str, Fight] = {}
        
        self.__on_game_over_event_listener: callable = None
        
        self.__generate_enemies()
        self.__initialize_events_listeners()
        
    def set_event_listener_on_game_over(self, callback: callable):
        self.__on_game_over_event_listener = callback

    def set_friends_group(self, friends: list[Character]):
        if (len(friends) > 0):
            player: Character = friends[0]
            player.get_position().x = Range(0, rpg.constants.WINDOW_WIDTH).random()
            player.get_position().y = Range(0, rpg.constants.WINDOW_HEIGHT).random()
            player.select()
            player.threat.increase(20.0)
            self.__friends_group.add_member(player)
            self.player.set_character(player)
            self.__friends_sprites.append(CharacterComponent(player))
            for friend in friends:
                if (friend is not player):
                    self.__friends_group.add_member(friend)
                    self.__friends_sprites.append(CharacterComponent(friend))

    def __initialize_events_listeners(self):
        self.__action_panel.on_spell_slot_hover(self.__handle_on_spell_slot_hover)
        self.__action_panel.on_spell_slot_press(self.__handle_on_spell_slot_press)
        self.__action_panel.on_spell_slot_release(self.__handle_on_spell_slot_release)
        self.__action_panel.on_spell_slot_leave(self.__handle_on_spell_slot_leave)
    
    def __handle_on_spell_slot_hover(self, spell: Spell):
        if (spell is not None):
            self.__spell_detail_popup = SpellDetailPopup(spell, self.player.character.character_class, rpg.constants.SPELL_POPUP_WIDTH, rpg.constants.SPELL_POPUP_HEIGHT, rpg.constants.SPELL_POPUP_POSITION)
    
    def __handle_on_spell_slot_press(self):
        if (self.__spell_detail_popup is not None):
            pass
    
    def __handle_on_spell_slot_release(self):
        if (self.__spell_detail_popup is not None):
            pass

    def __handle_on_spell_slot_leave(self):
        self.__spell_detail_popup = None

    def __generate_enemies(self):
        for _ in range(Range(10, 20).random()):
            enemy: Enemy = GameGenerator.generate_random_enemy()
            enemy.threat.increase(50.0)
            enemy.zone_radius = 200
            enemy.set_default_position(Position(Range(0, rpg.constants.WINDOW_WIDTH).random(), Range(0, rpg.constants.WINDOW_HEIGHT).random()))
            level: int = Range(1, 20).random()
            while (enemy.level.value < level):
                enemy.level.up()
            self.__enemies_sprites.append(EnemyComponent(enemy))

    def __prevent_character_to_disapear_from_scene(self, character: Character):
        if (character.get_position().x < (rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x)):
            character.get_position().x = rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x
        if (character.get_position().x > self.width):
            character.get_position().x = self.width
        if (character.get_position().y < 0):
            character.get_position().y = 0
        if (character.get_position().y > self.height):
            character.get_position().y = self.height

    def __handle_interaction_and_moves_for_friends(self):
        for friend in self.__friends_group.members:
            if (friend.life.is_alive()):
                if (not friend.is_in_fight_mode):
                    others: list[Character] = [other for other in self.__friends_group.members if other is not friend]
                    others += [other.character for other in self.__enemies_sprites]
                    for other in others:
                        if friend.is_touching(other):
                            friend.avoid_collision_with_other(other)
                    if friend.is_touching(self.player.character):
                        friend.avoid_collision_with_other(self.player.character)
                    else:
                        friend.follow(self.player.character)
                    self.__prevent_character_to_disapear_from_scene(friend)

    def __move_enemy_to_the_default_observation_position(self, enemy: Enemy):
        enemy.is_in_fight_mode = False
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
            enemy.get_position().x += direction_x * enemy.move_speed
            enemy.get_position().y += direction_y * enemy.move_speed

    def __move_enemy_to_the_patrol_position(self, enemy: Enemy):
        enemy.is_in_fight_mode = False
        if (Geometry.compute_distance(enemy.get_position(), enemy.patrol_destination) > 1):
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.patrol_destination.x - enemy.get_position().x
            direction_y = enemy.patrol_destination.y - enemy.get_position().y
            direction_length = Geometry.compute_distance(enemy.get_position(), enemy.patrol_destination)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa destination de patrouillage
            enemy.get_position().x += (direction_x * (enemy.move_speed/2))
            enemy.get_position().y += (direction_y * (enemy.move_speed/2))

    def __move_attacker_to_target_if_required(self, attacker: Character, target: Character):
        if (target.life.is_alive()):
            target.is_in_fight_mode = True
            if (not ClassType.is_damage_spell_caster(attacker.character_class.class_type)):
                distance_between_enemy_and_zone_center = Geometry.compute_distance(attacker.get_position(), target.get_position())
                if distance_between_enemy_and_zone_center < attacker.zone_radius:
                    attacker.follow(target)

    def __recruit_member(self, member: Character):
        if (not self.__friends_group.is_full()):
            self.__friends_group.add_member(member)

    def __recruit_member_if_is_touching(self, member: Character):
        if (member.is_touching(self.player.character)):
            self.__recruit_member(member)

    def __draw_hud(self, master: pygame.Surface):
        self.__group_panel.draw(master)
        self.__action_panel.draw(master)
        self.__experience_panel.draw(master)
        self.__message_panel.draw(master)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.draw(master)

    def __draw_scene(self, master: pygame.Surface):
        for hero_sprite in self.__friends_sprites:
            hero_sprite.draw(master)
        for vilain_sprite in self.__enemies_sprites:
            vilain_sprite.draw(master)
        
    def __handle_enemy_killed_by_friend(self, friend_sprite: CharacterComponent, enemy_sprite: CharacterComponent):
        if (enemy_sprite in self.__enemies_sprites):
            self.__enemies_sprites.remove(enemy_sprite)
        win_experience: int = (enemy_sprite.character.level.value*5) + 45
        friend_sprite.character.level.gain(win_experience)

    def __handle_projectil_sprite(self, attacker_sprite: CharacterComponent, projectil_sprite: ProjectilComponent, target_sprite: CharacterComponent):
        if (target_sprite.character.is_touching(projectil_sprite.projectil)):
            self.__message_broker.add_debug_message(f"{target_sprite.character.name} loose {projectil_sprite.projectil.payload} PVs.")
            target_sprite.character.life.loose(projectil_sprite.projectil.payload)
            if (projectil_sprite.projectil in attacker_sprite.character.trigged_projectils):
                attacker_sprite.character.trigged_projectils.remove(projectil_sprite.projectil)
                attacker_sprite.projectils.remove(projectil_sprite)
            if (target_sprite.character.life.is_dead()):
                self.__handle_enemy_killed_by_friend(attacker_sprite, target_sprite)

    def __handle_trigged_projectils_by_friends(self):
        for friend_sprite in self.__friends_sprites:
            for projectil_sprite in friend_sprite.projectils:
                for vilain_sprite in self.__enemies_sprites:
                    self.__handle_projectil_sprite(friend_sprite, projectil_sprite, vilain_sprite)

    def __terminate_fight(self, attacker: Character):
        if (attacker.name in list(self.__fights.keys())):
            existing_fight: Fight = self.__fights.get(attacker.name)
            if (existing_fight is not None):
                existing_fight.stop()
                print("Fight is stoped")
                del self.__fights[attacker.name]

    def __retrieve_most_threatening_character_for_enemy(self, enemy: Character) -> Character:
        threated_distances: dict[Character, float] = {}
        for potential_target in self.__friends_group.members:
            if (potential_target.life.is_alive()):
                enemy_is_already_threatened: bool = enemy.threat.is_threatened
                if (enemy.is_feel_threatened(potential_target)):
                    if (not enemy_is_already_threatened):
                        self.__message_broker.add_debug_message(f"Enemy {enemy.name} is feel threatened by {potential_target.name}.")
                    threated_distances[potential_target] = Geometry.compute_distance(potential_target.get_position(), enemy.get_position())
        most_threatening_target: Character = None
        if (threated_distances):
            most_threatening_target = min(threated_distances, key=threated_distances.get)
        return most_threatening_target

    def __can_attacker_attacks_target(self, attacker: Character, target: Character) -> bool:
        can_attack: bool = ClassType.is_damage_spell_caster(attacker.character_class.class_type)
        if (not can_attack):
            distance_between_enemy_and_zone_center = Geometry.compute_distance(attacker.get_position(), target.get_position())
            can_attack = distance_between_enemy_and_zone_center < attacker.zone_radius
        return can_attack

    def __is_future_attacker_already_running_fight(self, attacker: Character) -> bool:
        return (attacker.name in list(self.__fights.keys()))

    def __handle_enemy_actions(self, enemy_sprite: EnemyComponent):
        potential_target: Character = self.__retrieve_most_threatening_character_for_enemy(enemy_sprite.character)
        enemy_sprite.character.target = potential_target
        if (potential_target is not None):
            # Stop patrol
            if (enemy_sprite.character.is_patrolling):
                enemy_sprite.character.stop_patrolling()

            new_enemy_fight: Fight = None
            new_friend_fight: Fight = None
            if (not self.__is_future_attacker_already_running_fight(enemy_sprite.character)):
                # Start fight for enemy
                new_enemy_fight = Fight(enemy_sprite.character, potential_target)
                self.__fights[enemy_sprite.character.name] = new_enemy_fight
            
            if (not potential_target.is_in_fight_mode):
                if (potential_target.name not in list(self.__fights.keys())):
                    # start fight for friend
                    potential_target.is_in_fight_mode = True
                    potential_target.target = enemy_sprite.character
                    new_friend_fight = Fight(potential_target, enemy_sprite.character)

            self.__move_attacker_to_target_if_required(enemy_sprite.character, potential_target)
            if (self.__can_attacker_attacks_target(enemy_sprite.character, potential_target)):
                if (new_enemy_fight is not None):
                    if (not new_enemy_fight.is_alive()):
                        new_enemy_fight.start()
                        
            if (new_friend_fight is not None):
                if (not new_friend_fight.is_alive()):
                    if (self.__can_attacker_attacks_target(potential_target, enemy_sprite.character)):
                        new_friend_fight.start()
            # if (enemy_sprite.character.is_touching(target)):
            #     enemy_sprite.character.attack(target)
            #     if (len(enemy_sprite.character.trigged_projectils) > 0):
            #         projectil: Projectil = enemy_sprite.character.trigged_projectils[-1]
            #         projectil.to_position = target.get_position().copy()
            #         projectil_sprite: ProjectilComponent = ProjectilComponent(projectil)
            #         enemy_sprite.projectils.append(projectil_sprite)
                
        else:
            # Stop fight
            if (enemy_sprite.character.name in list(self.__fights.keys())):
                self.__terminate_fight(enemy_sprite.character)
                if (enemy_sprite.character.target is not None):
                    self.__terminate_fight(enemy_sprite.character.target)
                self.__enemies_sprites.remove(enemy_sprite)

            # Delete trigged projectils
            enemy_sprite.projectils.clear()
            enemy_sprite.character.trigged_projectils.clear()
            
            if (not enemy_sprite.character.is_patrolling):
                if (not enemy_sprite.character.is_arrived_to_default_position()):
                    # Go to Head Quarter
                    self.__move_enemy_to_the_default_observation_position(enemy_sprite.character)
                else:
                    # Begin patrol
                    self.__message_broker.add_debug_message(f"[ENEMY] {enemy_sprite.character.name} start patrol.")
                    enemy_sprite.character.generate_patrol_path()
                    enemy_sprite.character.patrol()
            else:
                if (not enemy_sprite.character.is_arrived_to_patrol_destination()):
                    # Continue patrol
                    self.__move_enemy_to_the_patrol_position(enemy_sprite.character)
                else:
                    # Start new patrol
                    enemy_sprite.character.generate_patrol_path()

    def __handle_event(self, event: pygame.event.Event):
        for friend_sprite in self.__friends_sprites:
            if (friend_sprite.character.is_selected()):
                friend_sprite.handle(event)
                break
        self.__group_panel.handle(event)
        self.__action_panel.handle(event)
        self.__experience_panel.handle(event)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.handle(event)
        self.__message_panel.handle(event)

    def __handle(self):
        self.__handle_trigged_projectils_by_friends()
        self.__group_panel.handle(None)
        self.__action_panel.handle(None)
        self.__experience_panel.handle(None)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.handle(None)
        for friend_sprite in self.__friends_sprites:
            friend_sprite.handle(None)
        for enemy_sprite in self.__enemies_sprites:
            enemy_sprite.handle(None)
        self.__message_panel.handle(None)
    
    def __change_character_for_player(self):
        previous_character: Character = self.player.character
        potential_new_character: Character = [character for character in self.__friends_group.members if character.is_selected()][0]
        if (previous_character is not potential_new_character):
            self.player.set_character([character for character in self.__friends_group.members if character.is_selected()][0])
            self.__action_panel.set_character(self.player.character)
            self.__action_panel.set_spells_wheel(self.player.spells_wheel)
            self.__experience_panel.set_character(self.player.character)
            self.__initialize_events_listeners()

    def handle(self, event: pygame.event.Event):
        if (event is not None):
            self.__handle_event(event)
        else:
            self.__handle()

        self.__change_character_for_player()
        
        if (self.player.character.is_moving):
            for member in self.__friends_group.members:
                self.__recruit_member_if_is_touching(member)

        self.__handle_interaction_and_moves_for_friends()

        # self.player.character.is_in_fight_mode = False
        for vilain_sprite in self.__enemies_sprites:
            if (vilain_sprite.character.life.is_alive()):
                difficulty: Difficulty = Difficulty.compute(self.player.character.level, vilain_sprite.character.level)
                vilain_sprite.set_difficulty_color(difficulty.value.color.to_tuple())
                self.__handle_enemy_actions(vilain_sprite)
            else:
                self.__terminate_fight(vilain_sprite.character)
                if (vilain_sprite.character.target is not None):
                    self.__terminate_fight(vilain_sprite.character.target)
                    vilain_sprite.character.target.target = None
                vilain_sprite.character.target = None

    def draw(self, master: pygame.Surface):
        heroes_alive: list[Character] = [member for member in self.__friends_group.members if member.life.is_alive()]
        if (len(heroes_alive) > 0):
            self.__draw_scene(master)
            self.__draw_hud(master)
        else:
            if (self.__on_game_over_event_listener is not None):
                self.__on_game_over_event_listener()