from rpg.gamengine import GameGenerator
from rpg.characters import Character

character: Character = GameGenerator.generate_random_player()
print(character.character_class.skills_trees[0].name)