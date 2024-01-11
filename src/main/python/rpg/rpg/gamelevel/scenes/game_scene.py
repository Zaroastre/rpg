import pygame
import rpg.constants
from rpg.characters import Character, Enemy
from rpg.gamedesign.difficulty_system import Difficulty
from rpg.gamedesign.fight_system import Fight
from rpg.gamedesign.geolocation_system import Position
from rpg.gamedesign.interval_system import Range
from rpg.gamedesign.message_system import MessageBroker
from rpg.gamelevel.scenes.scenes import Scene
from rpg.gamengine import GameGenerator
from rpg.gameplay.classes import ClassType
from rpg.gameplay.player import Player
from rpg.gameplay.spells import Spell
from rpg.gamedesign.camera_system import Camera
from rpg.gameplay.teams import Group
from rpg.math.geometry import Geometry
from rpg.ui.graphics import (ActionPanel, ExperiencePanel, GroupPanel,
                             MessagePanel, SpellDetailPopup, TargetHUD)
from rpg.ui.sprites import CharacterSprite, EnemySprite, ProjectilSprite
from rpg.artificial_intelligency.registry import ArtificialIntelligencyRegistry
  
class GameScene(Scene):
    def __init__(self, width: int, height: int, player: Player) -> None:
        super().__init__(width, height, player)
        self.__friends_group: Group = Group(max_capacity=5)
        
        self.__action_panel: ActionPanel = ActionPanel(rpg.constants.ACTION_PANEL_WIDTH, rpg.constants.ACTION_PANEL_HEIGHT, rpg.constants.ACTION_PANEL_POSITION)
        self.__experience_panel: ExperiencePanel = ExperiencePanel(rpg.constants.EXPERIENCE_PANEL_WIDTH, rpg.constants.EXPERIENCE_PANEL_HEIGHT, rpg.constants.EXPERIENCE_PANEL_POSITION)
        self.__group_panel: GroupPanel = GroupPanel(group=self.__friends_group, width=rpg.constants.GROUP_PANEL_WIDTH, height=rpg.constants.GROUP_PANEL_HEIGHT, position=rpg.constants.GROUP_PANEL_POSITION)
        self.__message_panel: MessagePanel = MessagePanel(width=rpg.constants.MESSAGE_PANEL_WIDTH, height=rpg.constants.MESSAGE_PANEL_HEIGHT, position=rpg.constants.MESSAGE_PANEL_POSITION)
        self.__target_hud: TargetHUD = TargetHUD(self.player.character, rpg.constants.HUD_TARGET_WIDTH, rpg.constants.HUD_TARGET_HEIGHT, rpg.constants.HUD_TARGET_THICKNESS, rpg.constants.HUD_TARGET_CORNER_LENGTH)

        self.__friends_sprites: list[CharacterSprite] = []
        self.__enemies_sprites: list[EnemySprite] = []
        
        self.__spell_detail_popup: SpellDetailPopup = None
        self.__message_broker: MessageBroker = MessageBroker()
        self.__ai_registry: ArtificialIntelligencyRegistry|None = None 
        self.__fights: dict[str, Fight] = {}
        
        self.__on_game_over_event_listener: callable = None
        
        self.__generate_enemies()
        self.__initialize_events_listeners()
    
    def set_event_listener_on_game_over(self, callback: callable):
        self.__on_game_over_event_listener = callback
    
    def set_ai_registry(self, ai_registry: ArtificialIntelligencyRegistry) -> None:
        self.__ai_registry = ai_registry

    def set_friends_group(self, friends: list[Character]):
        if (len(friends) > 0):
            player: Character = friends[0]
            if (player.current_position == Position(0,0)):
                player.set_current_position(Position(
                    Range(0, rpg.constants.WINDOW_WIDTH).random(),
                    Range(0, rpg.constants.WINDOW_HEIGHT).random()
                ))
            player.select()
            # player.threat.increase(20.0)
            self.__friends_group.add_member(player)
            self.player.set_character(player)
            self.__friends_sprites.append(CharacterSprite(player))
            for friend in friends:
                if (friend is not player):
                    self.__friends_group.add_member(friend)
                    self.__friends_sprites.append(CharacterSprite(friend))
        self.__update_character()
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

    def __handle_killed_enemy(self, enemy: Enemy):
        enemy_sprite_to_remove: EnemySprite = None
        for enemy_sprite in self.__enemies_sprites:
            if (enemy_sprite.character == enemy):
                enemy_sprite_to_remove = enemy_sprite
                break
        if (enemy_sprite_to_remove is not None):
            self.__enemies_sprites.remove(enemy_sprite_to_remove)
        win_experience: int = int((enemy.level.value*5) + 45)/len(self.__friends_group.members)
        self.__message_broker.add_debug_message(f"Exp: +{str(win_experience)}")
        for friend in self.__friends_group.members:
            friend.threat.decrease(friend.threat.level)
            if (friend.life.is_alive()):
                friend.level.gain(win_experience)
            if (friend.target == enemy):
                friend.set_target(None)
                friend.set_stay_in_place_mode()
                friend.is_in_fight_mode = False

    def __generate_enemies(self):
        for _ in range(Range(10, 20).random()):
            enemy: Enemy = GameGenerator.generate_random_enemy()
            enemy.threat.increase(50.0)
            enemy.zone_radius = 200
            enemy.set_default_position(Position(Range(0, rpg.constants.WINDOW_WIDTH).random(), Range(0, rpg.constants.WINDOW_HEIGHT).random()))
            enemy.set_on_die_event_listener(self.__handle_killed_enemy)
            level: int = Range(1, 20).random()
            while (enemy.level.value < level):
                enemy.level.up()
            self.__enemies_sprites.append(EnemySprite(enemy))

    def __prevent_character_to_disapear_from_scene(self, character: Character):
        new_position: Position = None
        if (character.current_position.x < (rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x)):
            new_position = Position(rpg.constants.GROUP_PANEL_WIDTH + rpg.constants.GROUP_PANEL_POSITION.x, character.current_position.y)
        if (character.current_position.x > self.width):
            new_position = Position(self.width, character.current_position.y)
        if (character.current_position.y < 0):
            new_position = Position(character.current_position.x, 0)
        if (character.current_position.y > self.height):
            new_position = Position(character.current_position.x, self.height)
        if (new_position is not None):
            character.set_current_position(new_position)

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
        if Geometry.compute_distance(enemy.current_position, enemy.zone_center) > 1:
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.zone_center.x - enemy.current_position.x
            direction_y = enemy.zone_center.y - enemy.current_position.y
            direction_length = Geometry.compute_distance(enemy.current_position, enemy.zone_center)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa position initiale
            new_x: int = enemy.current_position.x + direction_x * enemy.move_speed
            new_y: int = enemy.current_position.y + direction_y * enemy.move_speed
            new_position: Position = Position(new_x, new_y)
            enemy.set_current_position(new_position)

    def __move_enemy_to_the_patrol_position(self, enemy: Enemy):
        if (Geometry.compute_distance(enemy.current_position, enemy.patrol_destination) > 1):
            # Calculer le vecteur directionnel vers la position initiale
            direction_x = enemy.patrol_destination.x - enemy.current_position.x
            direction_y = enemy.patrol_destination.y - enemy.current_position.y
            direction_length = Geometry.compute_distance(enemy.current_position, enemy.patrol_destination)

            # Normaliser le vecteur directionnel
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Déplacer progressivement l'ennemi vers sa destination de patrouillage
            new_x: int = enemy.current_position.x + (direction_x * (enemy.move_speed/2))
            new_y: int = enemy.current_position.y + (direction_y * (enemy.move_speed/2))
            new_position: Position = Position(new_x, new_y)
            enemy.set_current_position(new_position)

    def __move_attacker_to_target_if_required(self, attacker: Character, target: Character):
        if (target.life.is_alive()):
            if (not ClassType.is_damage_spell_caster(attacker.character_class.class_type)):
                distance_between_enemy_and_zone_center = Geometry.compute_distance(attacker.current_position, target.current_position)
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
        self.__target_hud.draw(master)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.draw(master)

    def __draw_scene(self, master: pygame.Surface):
        for hero_sprite in self.__friends_sprites:
            hero_sprite.draw(master)
        for vilain_sprite in self.__enemies_sprites:
            vilain_sprite.draw(master)
       
    def __handle_projectil_sprite(self, attacker_sprite: CharacterSprite, projectil_sprite: ProjectilSprite, target_sprite: CharacterSprite):
        if (target_sprite.character.is_touching(projectil_sprite.projectil)):
            self.__message_broker.add_debug_message(f"{target_sprite.character.name} loose {projectil_sprite.projectil.payload} PVs.")
            target_sprite.character.life.loose(projectil_sprite.projectil.payload)
            if (projectil_sprite.projectil in attacker_sprite.character.trigged_projectils):
                attacker_sprite.character.trigged_projectils.remove(projectil_sprite.projectil)
                attacker_sprite.projectils.remove(projectil_sprite)

    def __handle_trigged_projectils_by_friends(self):
        for friend_sprite in self.__friends_sprites:
            for projectil_sprite in friend_sprite.projectils:
                for vilain_sprite in self.__enemies_sprites:
                    self.__handle_projectil_sprite(friend_sprite, projectil_sprite, vilain_sprite)

    def __terminate_fight(self, attacker: Character):
        if (attacker.name in list(self.__fights.keys())):
            existing_fight: Fight = self.__fights.get(attacker.name)
            if (existing_fight is not None):
                if (existing_fight.is_alive()):
                    existing_fight.stop()
                del self.__fights[attacker.name]

    def __retrieve_most_threatening_character_for_enemy(self, enemy: Character) -> Character:
        threated_distances: dict[Character, float] = {}
        for potential_target in self.__friends_group.members:
            if (potential_target.life.is_alive()):
                enemy_is_already_threatened: bool = enemy.threat.is_threatened
                if (enemy.is_feel_threatened(potential_target)):
                    if (not enemy_is_already_threatened):
                        self.__message_broker.add_debug_message(f"Enemy {enemy.name} is feel threatened by {potential_target.name}.")
                    threated_distances[potential_target] = Geometry.compute_distance(potential_target.current_position, enemy.current_position)
        most_threatening_target: Character = None
        if (threated_distances):
            most_threatening_target = min(threated_distances, key=threated_distances.get)
        return most_threatening_target

    def __can_attacker_attacks_target(self, attacker: Character, target: Character) -> bool:
        can_attack: bool = ClassType.is_damage_spell_caster(attacker.character_class.class_type)
        if (not can_attack):
            distance_between_enemy_and_zone_center = Geometry.compute_distance(attacker.current_position, target.current_position)
            can_attack = distance_between_enemy_and_zone_center < attacker.zone_radius
        return can_attack

    def __is_future_attacker_already_running_fight(self, attacker: Character) -> bool:
        return (attacker.name in list(self.__fights.keys()))

    def __set_enemy_color_difficulty(self, enemy_sprite: EnemySprite):
        difficulty: Difficulty = Difficulty.compute(self.player.character.level, enemy_sprite.character.level)
        enemy_sprite.set_difficulty_color(difficulty.value.color.to_tuple())
    
    def __handle_enemy_aggresive_actions(self, enemy_sprite: EnemySprite, targeted_friend: Character):
        # Stop patrol
        if (enemy_sprite.character.is_patrolling):
            enemy_sprite.character.stop_patrolling()

        new_enemy_fight: Fight = None
        new_friend_fight: Fight = None
        if (not self.__is_future_attacker_already_running_fight(enemy_sprite.character)):
            # Start fight for enemy
            new_enemy_fight = Fight(enemy_sprite.character, targeted_friend)
            self.__fights[enemy_sprite.character.name] = new_enemy_fight
        
        if (not targeted_friend.is_in_fight_mode):
            if (targeted_friend.name not in list(self.__fights.keys())):
                targeted_friend.set_target(enemy_sprite.character)
                new_friend_fight = Fight(targeted_friend, enemy_sprite.character)

        self.__move_attacker_to_target_if_required(enemy_sprite.character, targeted_friend)
        if (self.__can_attacker_attacks_target(enemy_sprite.character, targeted_friend)):
            if (new_enemy_fight is not None):
                if (not new_enemy_fight.is_alive()):
                    new_enemy_fight.start()
                    
        if (new_friend_fight is not None):
            if (not new_friend_fight.is_alive()):
                if (self.__can_attacker_attacks_target(targeted_friend, enemy_sprite.character)):
                    new_friend_fight.start()

    def __handle_enemy_neutral_actions(self, enemy_sprite: EnemySprite):
        # Stop fight
        if (enemy_sprite.character.name in list(self.__fights.keys())):
            self.__terminate_fight(enemy_sprite.character)
            if (enemy_sprite.character.target is not None):
                self.__terminate_fight(enemy_sprite.character.target)

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

    def __handle_enemy_actions(self, enemy_sprite: EnemySprite):
        self.__set_enemy_color_difficulty(enemy_sprite)
        potential_target: Character = self.__retrieve_most_threatening_character_for_enemy(enemy_sprite.character)
        enemy_sprite.character.set_target(potential_target)
        if (potential_target is not None):
            self.__handle_enemy_aggresive_actions(enemy_sprite, potential_target)
        else:
            self.__handle_enemy_neutral_actions(enemy_sprite)

    def __handle_event(self, event: pygame.event.Event):
        for friend_sprite in self.__friends_sprites:
            if (friend_sprite.character.is_selected()):
                friend_sprite.handle(event)
                break
        self.__group_panel.handle(event)
        self.__action_panel.handle(event)
        self.__target_hud.handle(event)
        self.__experience_panel.handle(event)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.handle(event)
        self.__message_panel.handle(event)

    def __handle(self):
        self.__handle_trigged_projectils_by_friends()
        self.__group_panel.handle(None)
        self.__action_panel.handle(None)
        self.__target_hud.handle(None)
        self.__experience_panel.handle(None)
        if (self.__spell_detail_popup is not None):
            self.__spell_detail_popup.handle(None)
        for friend_sprite in self.__friends_sprites:
            friend_sprite.handle(None)
        for enemy_sprite in self.__enemies_sprites:
            enemy_sprite.handle(None)
        self.__message_panel.handle(None)
    
    def __update_character(self):
        self.player.set_character([character for character in self.__friends_group.members if character.is_selected()][0])
        self.__action_panel.set_character(self.player.character)
        self.__target_hud.set_character(self.player.character)
        self.__action_panel.set_spells_wheel(self.player.spells_wheel)
        self.__experience_panel.set_character(self.player.character)
        # for friend_sprite in self.__friends_sprites:
        #     if (friend_sprite.character.is_selected()):
        #         # self.__camera_group.set_character_to_track(friend_sprite)
        #         break
    
    def __change_character_for_player(self):
        previous_character: Character = self.player.character
        potential_new_character: Character = [character for character in self.__friends_group.members if character.is_selected()][0]
        if (previous_character is not potential_new_character):
            self.__update_character()
            self.__initialize_events_listeners()

    def __handle_interaction_and_moves_for_enemies(self):
        for vilain_sprite in self.__enemies_sprites:
            if (vilain_sprite.character.life.is_alive()):
                self.__handle_enemy_actions(vilain_sprite)
            else:
                self.__terminate_fight(vilain_sprite.character)
                if (vilain_sprite.character.target is not None):
                    self.__terminate_fight(vilain_sprite.character.target)
                    
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
        self.__handle_interaction_and_moves_for_enemies()

    def draw(self, master: pygame.Surface):
        print(self.player.character.name)
        heroes_alive: list[Character] = [member for member in self.__friends_group.members if member.life.is_alive()]
        if (len(heroes_alive) > 0):
            self.__draw_scene(master)
            self.__draw_hud(master)
            # self.__camera.draw_tracking_target(master)
        else:
            if (self.__on_game_over_event_listener is not None):
                self.__on_game_over_event_listener()
