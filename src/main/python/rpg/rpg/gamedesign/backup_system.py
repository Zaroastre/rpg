from rpg.gameplay.player import Player
from rpg.gameplay.breeds import BreedType, BreedFactory, Breed
from rpg.gameplay.classes import ClassType, ClassFactory, Class
from rpg.gamengine import GameGenerator
from rpg.gameplay.genders import Gender
from rpg.gamedesign.faction_system import Faction
from rpg.characters import Character
from pathlib import Path
from json import dumps, loads


class GameLoader:
    __BACKUP_FILE_NAME: str = "nemesys.bkp"
    __BREED_ATTRIBUTE: str = "breed"
    __CLASS_ATTRIBUTE: str = "class"
    __GENDER_ATTRIBUTE: str = "gender"
    __FACTION_ATTRIBUTE: str = "faction"
    __LEVEL_ATTRIBUTE: str = "level"
    __EXPERIENCE_ATTRIBUTE: str = "experience"
    __NAME_ATTRIBUTE: str = "name"
    def __init__(self) -> None:
        pass
    
    def is_backup_exists(self) -> bool:
        return Path(GameLoader.__BACKUP_FILE_NAME).exists()
    
    def save(self, player: Player):
        with open(Path(GameLoader.__BACKUP_FILE_NAME), 'w', encoding="UTF-8") as file:
            backup: dict = {}
            for index, member in enumerate(player.group.members):
                character: dict = {}
                character[GameLoader.__NAME_ATTRIBUTE] = member.name
                character[GameLoader.__GENDER_ATTRIBUTE] = member.gender.name
                character[GameLoader.__FACTION_ATTRIBUTE] = member.faction.name
                character[GameLoader.__BREED_ATTRIBUTE] = member.breed.breed_type.name
                character[GameLoader.__CLASS_ATTRIBUTE] = member.character_class.class_type.name
                character[GameLoader.__LEVEL_ATTRIBUTE] = member.level.value
                character[GameLoader.__EXPERIENCE_ATTRIBUTE] = member.level.experience.current                
                backup[str(index)] = character
            json: dict = dumps(backup)
            file.write(str(json))
    
    def load(self) -> Player:
        player: Player = Player()
        with open(Path(GameLoader.__BACKUP_FILE_NAME), 'r', encoding="UTF-8") as file:
            json: dict = loads(file.read())
            
            for character_identifier in list(json.keys()):
                character_configuration: dict[str, object] = json.get(character_identifier)
                name: str = character_configuration.get(GameLoader.__NAME_ATTRIBUTE)
                gender_value: str = character_configuration.get(GameLoader.__GENDER_ATTRIBUTE)
                faction_value: str = character_configuration.get(GameLoader.__FACTION_ATTRIBUTE)
                breed_value: str = character_configuration.get(GameLoader.__BREED_ATTRIBUTE)
                character_class_value: str = character_configuration.get(GameLoader.__CLASS_ATTRIBUTE)
                level: int = int(character_configuration.get(GameLoader.__LEVEL_ATTRIBUTE))
                experience: int = int(character_configuration.get(GameLoader.__EXPERIENCE_ATTRIBUTE))
                
                gender: Gender = [value for value in list(Gender) if value.name == gender_value][0]
                faction: Faction = [value for value in list(Faction) if value.name == faction_value][0]
                breed: Breed = BreedFactory.create([value for value in list(BreedType) if value.name == breed_value][0])
                character_class: Class = ClassFactory.create([value for value in list(ClassType) if value.name == character_class_value][0])
                character: Character = GameGenerator.create_friend(name, breed, character_class, gender, faction)
                while (character.level.value < level):
                    character.level.up()
                character.level.experience.gain(experience)
                if (player.character is None):
                    character.select()
                    player.set_character(character)
                    player.group.add_member(character)
                else:
                    player.group.add_member(character)
        return player