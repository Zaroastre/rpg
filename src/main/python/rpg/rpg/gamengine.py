from random import randint, shuffle

from rpg.gameplay.breeds import Breed, BreedType, BreedFactory
from rpg.characters import Character, Enemy
from rpg.gameplay.classes import Class, ClassType, ClassFactory
from rpg.gameplay.genders import Gender
from rpg.gamedesign.faction_system import Faction


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
    def generate_random_gender() -> Gender:
        genders: list[Gender] = list(Gender)
        index = randint(0, len(genders)-1)
        return genders[index]
    
    @staticmethod
    def generate_random_faction() -> Faction:
        factions: list[Gender] = list(Faction)
        index = randint(0, len(factions)-1)
        return factions[index]
    
    @staticmethod
    def generate_random_name(gender: Gender = None) -> str:
        male_first_names: list[str] = ["Luke", "Phillip", "Tony", "Herman", "Elle", "Allec", "Oakley",  "Maxim", "Adem", "Dominik",  "Ivan", "Ted", "Han", "Dom", "Hal", "Malcolm", "Reese", "Nick", "Rick", "Klaus", "Harry"]
        female_first_names: list[str] = ["Kate", "Lauren", "Gemma", "Sophia", "Suzanne", "Kathleen", "Brooke", "Chloe","Alexandra", "Charlotte", "Jermaine", "Lois", "Sylvie", "Celia", "Constance", "Sallie", "Luna", "Robin"]
        last_names: list[str] = ["Rockatansky", "Blacksmith", "Parker", "Ballet", "Grey", "Rabbit", "Walker", "Blunder", "Nguyen", "Bishop", "Steele", "Mahoney", "Benson", "Atkins", "Suarez", "Gibbs", "Wilkinson", "Wright", "Woodward", "Montes", "Warner", "Velasquez", "Patton", "Levine"]
        name: str
        if (gender is not None):
            match (gender):
                case Gender.MAN:
                    name = f"{male_first_names[randint(0, len(male_first_names)-1)]} {last_names[randint(0, len(last_names)-1)].upper()}"
                case Gender.WOMAN:
                    name = f"{female_first_names[randint(0, len(female_first_names)-1)]} {last_names[randint(0, len(last_names)-1)].upper()}"
        else:
            first_names: list[str] = male_first_names.copy() + female_first_names.copy()
            shuffle(first_names)
            name = f"{first_names[randint(0, len(first_names)-1)]} {last_names[randint(0, len(last_names)-1)].upper()}"
        return name
    
    
    @staticmethod
    def generate_random_player() -> Character:
        breed: Breed = GameGenerator.generate_random_breed()
        character_class: Class = GameGenerator.generate_random_class()
        name: str = GameGenerator.generate_random_name()
        gender: Gender = GameGenerator.generate_random_gender()
        faction: Faction = GameGenerator.generate_random_faction()
        return GameGenerator.create_friend(name, breed, character_class, gender, faction)
    
    @staticmethod
    def generate_random_enemy() -> Character:
        breed: Breed = GameGenerator.generate_random_breed()
        character_class: Class = GameGenerator.generate_random_class()
        name: str = GameGenerator.generate_random_name()
        gender: Gender = GameGenerator.generate_random_gender()
        faction: Faction = GameGenerator.generate_random_faction()
        return GameGenerator.create_mob(name, breed, character_class, gender, faction)
    
    
    @staticmethod
    def create_friend(name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> Character:
        return Character(name, breed, character_class, gender, faction)
    
    @staticmethod
    def create_mob(name: str, breed: Breed, character_class: Class, gender: Gender, faction: Faction) -> Character:
        return Enemy(name, breed, character_class, gender, faction)
