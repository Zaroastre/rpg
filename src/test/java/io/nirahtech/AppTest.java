package io.nirahtech;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.CharacterFactory;
import io.nirahtech.rpg.characters.classes.Demonist;
import io.nirahtech.rpg.characters.classes.Mage;
import io.nirahtech.rpg.characters.classes.Paladin;
import io.nirahtech.rpg.characters.classes.Priest;
import io.nirahtech.rpg.characters.classes.Warrior;
import io.nirahtech.rpg.characters.races.BloodElf;
import io.nirahtech.rpg.characters.races.Human;
import io.nirahtech.rpg.strategies.attacks.AttackStrategyChooser;
import io.nirahtech.rpg.teams.Group;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    public static void main(String[] args) {
        final Character nicolas = CharacterFactory.create(new BloodElf(), new Paladin());
        final Character victor = CharacterFactory.create(new BloodElf(), new Mage());
        final Character rebecca = CharacterFactory.create(new BloodElf(), new Priest());
        final Character lucy = CharacterFactory.create(new BloodElf(), new Demonist());
        final Character anthony = CharacterFactory.create(new BloodElf(), new Warrior());

        final Character arthas = CharacterFactory.create(new Human(), new Paladin());

        final Group group = Group.create(5);
        group.add(nicolas);
        group.add(victor);
        group.add(rebecca);
        group.add(lucy);
        group.add(anthony);

        nicolas.attack(AttackStrategyChooser.chooseBestStrategy(nicolas, Set.of(arthas)), arthas);
    }
}
