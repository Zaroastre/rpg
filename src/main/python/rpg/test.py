from rpg.gamengine import GameGenerator
from rpg.characters import Character

character: Character = GameGenerator.generate_random_player()
print(character.character_class.class_type)
print(character.character_class.resource)
print(character.breed.breed_type)
print(character.breed.life)
print(character.level)
print(character.character_class.spells_book.spells)