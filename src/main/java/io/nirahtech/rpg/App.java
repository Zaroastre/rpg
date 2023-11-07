package io.nirahtech.rpg;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import io.nirahtech.drivers.gamepad.Gamepad;
import io.nirahtech.drivers.gamepad.Gamepads;
import io.nirahtech.drivers.keyboard.Keyboard;
import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.CharacterFactory;
import io.nirahtech.rpg.characters.Faction;
import io.nirahtech.rpg.characters.Gender;
import io.nirahtech.rpg.characters.Level;
import io.nirahtech.rpg.characters.classes.Demonist;
import io.nirahtech.rpg.characters.classes.Mage;
import io.nirahtech.rpg.characters.classes.Paladin;
import io.nirahtech.rpg.characters.classes.Priest;
import io.nirahtech.rpg.characters.classes.Warrior;
import io.nirahtech.rpg.characters.races.BloodElf;
import io.nirahtech.rpg.characters.races.BreedType;
import io.nirahtech.rpg.characters.races.Human;
import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.cli.CommandLineInterface;
import io.nirahtech.rpg.strategies.attacks.AttackStategy;
import io.nirahtech.rpg.strategies.attacks.AttackStrategyChooser;
import io.nirahtech.rpg.teams.Group;
import io.nirahtech.rpg.teams.Raid;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        final Map<String, Object> configuration = new HashMap<>();
        final UserInterface userInterface = new CommandLineInterface();
        userInterface.run(configuration);

        final Character<Paladin> nicolas = CharacterFactory.create("Nicolas", BreedType.BLOOD_ELF.create(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Mage> victor = CharacterFactory.create("Victor", new BloodElf(), new Mage(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Priest> rebecca = CharacterFactory.create("Rebecca", new BloodElf(), new Priest(), Gender.FEMALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Demonist> lucy = CharacterFactory.create("Lucy", new BloodElf(), new Demonist(), Gender.FEMALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Warrior> anthony = CharacterFactory.create("Anthony", new BloodElf(), new Warrior(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));

        victor.follow(nicolas);
        rebecca.follow(nicolas);
        lucy.follow(nicolas);
        anthony.follow(nicolas);

        final Character<Paladin> sargeras = CharacterFactory.create("Sargeras", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> arthas = CharacterFactory.create("Athas", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> kilJaeden = CharacterFactory.create("Kil'jaeden", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> deathWing = CharacterFactory.create("Deathwing", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> illidan = CharacterFactory.create("Illidan Stormrage", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> gulDran = CharacterFactory.create("Gul'dan", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> nerZhuul = CharacterFactory.create("Ner'zhul", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> azshara = CharacterFactory.create("Queen Azshara", new Human(), new Paladin(), Gender.FEMALE, Faction.HORDE, Level.Factory.create(1));
        final Character<Paladin> ragnaros = CharacterFactory.create("Ragnaros", new Human(), new Paladin(), Gender.MALE, Faction.HORDE, Level.Factory.create(1));

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

        final AttackStategy attackStategy = AttackStrategyChooser.chooseBestStrategy(nicolas, Set.of(arthas));
        nicolas.attack(attackStategy, arthas);

        final Gamepad gamepad = Gamepads.get();
        final Keyboard keyboard = new Keyboard();
        userInterface.addInputDevice(gamepad);
        userInterface.addInputDevice(keyboard);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            gamepad.shutdown();
        }));

        gamepad.onPressA(() -> {
            System.out.println("A pressed");
        });


    }
}
