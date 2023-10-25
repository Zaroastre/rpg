package io.nirahtech;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.CharacterFactory;
import io.nirahtech.rpg.characters.Faction;
import io.nirahtech.rpg.characters.Gender;
import io.nirahtech.rpg.characters.Level;
import io.nirahtech.rpg.characters.classes.ClassType;
import io.nirahtech.rpg.characters.classes.Demonist;
import io.nirahtech.rpg.characters.races.BreedType;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    void test() {
        Character<Demonist> vincent = CharacterFactory.create("Vincent", BreedType.HUMAN.create(), ClassType.DEMONIST.create(), Gender.MALE, Faction.ALLIANCE, Level.Factory.create(1));
        vincent.getCharacterClass();
    }
}
