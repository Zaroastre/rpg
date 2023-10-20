package io.nirahtech;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.CharacterFactory;
import io.nirahtech.rpg.characters.Level;
import io.nirahtech.rpg.characters.classes.Demonist;
import io.nirahtech.rpg.characters.classes.Mage;
import io.nirahtech.rpg.characters.classes.Paladin;
import io.nirahtech.rpg.characters.classes.Priest;
import io.nirahtech.rpg.characters.classes.Warrior;
import io.nirahtech.rpg.characters.races.BloodElf;
import io.nirahtech.rpg.characters.races.Human;
import io.nirahtech.rpg.strategies.attacks.AttackStrategyChooser;
import io.nirahtech.rpg.teams.Group;
import io.nirahtech.rpg.teams.Raid;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    public static void main(String[] args) {
        final Character nicolas = CharacterFactory.create("Nicolas", new BloodElf(), new Paladin(), Level.Factory.create(1));
        final Character victor = CharacterFactory.create("Victor", new BloodElf(), new Mage(), Level.Factory.create(1));
        final Character rebecca = CharacterFactory.create("Rebecca", new BloodElf(), new Priest(), Level.Factory.create(1));
        final Character lucy = CharacterFactory.create("Lucy", new BloodElf(), new Demonist(), Level.Factory.create(1));
        final Character anthony = CharacterFactory.create("Anthony", new BloodElf(), new Warrior(), Level.Factory.create(1));

        final Character sargeras = CharacterFactory.create("Sargeras", new Human(), new Paladin(), Level.Factory.create(1));
        final Character arthas = CharacterFactory.create("Athas", new Human(), new Paladin(), Level.Factory.create(1));
        final Character kilJaeden = CharacterFactory.create("Kil'jaeden", new Human(), new Paladin(), Level.Factory.create(1));
        final Character deathWing = CharacterFactory.create("Deathwing", new Human(), new Paladin(), Level.Factory.create(1));
        final Character illidan = CharacterFactory.create("Illidan Stormrage", new Human(), new Paladin(), Level.Factory.create(1));
        final Character gulDran = CharacterFactory.create("Gul'dan", new Human(), new Paladin(), Level.Factory.create(1));
        final Character nerZhuul = CharacterFactory.create("Ner'zhul", new Human(), new Paladin(), Level.Factory.create(1));
        final Character azshara = CharacterFactory.create("Queen Azshara", new Human(), new Paladin(), Level.Factory.create(1));
        final Character ragnaros = CharacterFactory.create("Ragnaros", new Human(), new Paladin(), Level.Factory.create(1));

        final Raid raid = new Raid();
        raid.add(sargeras);
        raid.add(arthas);
        raid.add(kilJaeden);
        raid.add(deathWing);
        raid.add(illidan);
        raid.add(gulDran);
        raid.add(nerZhuul);
        raid.add(azshara);
        raid.add(ragnaros);

        final Group group = Group.create(5);
        group.add(nicolas);
        group.add(victor);
        group.add(rebecca);
        group.add(lucy);
        group.add(anthony);

        nicolas.attack(AttackStrategyChooser.chooseBestStrategy(nicolas, Set.of(arthas)), arthas);

        rebecca.getCharacterClass().getResource();
    }
}
