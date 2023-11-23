from rpg.gameplay.player import Player
from json import dumps, load


class GameLoader:
    __BACKUP_FILE_NAME: str = "nemesys.bkp"
    def __init__(self) -> None:
        pass
    
    def convert_to_json(obj):
        if isinstance(obj, Character):
            return {
                "__class__": "Character",
                "__module__": obj.__module__,
                "character_data": obj.character_data,  # Ajoutez les attributs que vous souhaitez sauvegarder
                # ...
            }

    
    def save(self, player: Player):
        with open(GameLoader.__BACKUP_FILE_NAME, 'w') as file:
            backup: dict = {}
            for index, member in enumerate(player.group.members):
                character: dict = {}
                character["breed"] = member.breed.breed_type.name
                character["class"] = member.character_class.class_type.name
                character["level"] = member.level.value
                character["experience"] = member.level.experience.current                
                backup[str(index)] = character
            json: dict = dumps(backup)
            file.write(str(json))
    
    def load(self) -> Player:
        player: Player = None
        with open(GameLoader.__BACKUP_FILE_NAME, 'w') as file:
            json: dict = load(file)
            player = Player()
        return player