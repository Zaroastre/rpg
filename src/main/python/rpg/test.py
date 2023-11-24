# from rpg.gamengine import GameGenerator
# from rpg.characters import Character
from rpg.geolocation import Position

# character: Character = GameGenerator.generate_random_player()
# print(character.character_class.class_type)
# print(character.character_class.resource)
# print(character.breed.breed_type)
# print(character.breed.life)
# print(character.level)
# print(character.character_class.spells_book.spells)
p1 = Position(827.6824019694969, 653.479818474593)
p2 = Position(827, 654)
print(Position.are_equivalent(p1, p2, 10))