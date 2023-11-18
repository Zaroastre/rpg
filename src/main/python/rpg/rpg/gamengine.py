from random import randint

from rpg.breeds import Breed, BreedType, BreedFactory
from rpg.characters import Character
from rpg.classes import Class, ClassType, ClassFactory


class GameGenerator:
    
    @staticmethod
    def generate_random_breed() -> Breed:
        breed_types: list[BreedType] = [breed_type for breed_type in BreedType]
        index = randint(0, len(breed_types)-1)
        return BreedFactory.create(breed_types[index])
    
    @staticmethod
    def generate_random_class() -> Class:
        class_types: list[ClassType] = [class_type for class_type in ClassType]
        index = randint(0, len(class_types)-1)
        return ClassFactory.create(class_types[index])
    
    @staticmethod
    def generate_random_name() -> str:
        first_name: list[str] = ["Luke", "Kate", "Lauren", "Phillip", "Gemma", "Sophia", "Tony", "Herman", "Elle", "Allec", "Suzanne", "Kathleen", "Brooke", "Chloe", "Oakley", "Alexandra", "Maxim", "Luna", "Adem", "Jermaine", "Lois", "Dominik", "Sylvie", "Ivan", "Constance", "Sallie"]
        last_name: list[str] = ["Rockatansky", "Blacksmith", "Parker", "Grey", "Rabbit", "Walker", "Blunder", "Nguyen", "Bishop", "Steele", "Mahoney", "Benson", "Atkins", "Suarez", "Gibbs", "Wilkinson", "Wright", "Woodward", "Montes", "Warner", "Velasquez", "Patton", "Levine"]
        name: str = f"{first_name[randint(0, len(first_name)-1)]} {last_name[randint(0, len(last_name)-1)]}"
        return name
    
    
    @staticmethod
    def generate_random_player() -> Character:
        breed: Breed = GameGenerator.generate_random_breed()
        character_class: Class = GameGenerator.generate_random_class()
        name: str = GameGenerator.generate_random_name()
        return GameGenerator.create_player(name, breed, character_class)
    
    @staticmethod
    def create_player(name: str, breed: Breed, character_class: Class) -> Character:
        return Character(name, breed, character_class)
