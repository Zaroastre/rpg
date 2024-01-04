from pathlib import Path

from rpg.characters import Character
from rpg.gameplay.breeds import BreedFactory, Breed
from rpg.gameplay.classes import Class, ClassFactory
from rpg.gameplay.genders import Gender
from rpg.gamedesign.faction_system import Faction
from rpg.gameplay.weapons import WeaponFactory, StuffPartType, QualityType, Range
from rpg.csv import CsvReader, Csv

def main():
    # name: str = "Hextanktion"
    # breed: Breed = BreedFactory.undead()
    # character_class: Class = ClassFactory.paladin()
    # gender: Gender = Gender.MAN
    # faction: Faction = Faction.HORDE
    # player: Character = Character(name, breed, character_class, gender, faction)
    # player.character_class.use_weapon(WeaponFactory.two_hands_mace(None, None, StuffPartType.RIGHT_HAND_OBJECT, QualityType.ARTIFACT, 1, Range(1, 10), 0.0))
    # print(player.character_class.right_hand_weapon.gem_box.maximum_capacity)
    # print(player.character_class.right_hand_weapon)
    
    csv = CsvReader.read(Path("C:/Users/NicolasMetivier/Documents/personal/rpg/src/main/python/rpg/resources/size-in-cm.csv"))
    print(csv.get_line_by_header("draenei").get())
    print(csv.get_column_by_header("woman_min").get())

if (__name__ == "__main__"):
    main()