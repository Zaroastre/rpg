package io.nirahtech.rpg.characters;

import java.util.Optional;

import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.inventories.Inventory;
import io.nirahtech.rpg.characters.races.Breed;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.infrastructure.Point;
import io.nirahtech.rpg.strategies.attacks.AttackStategy;
import io.nirahtech.rpg.teams.Group;
import io.nirahtech.rpg.teams.Raid;
import io.nirahtech.rpg.weapons.Weapon;

class CharacterImpl implements Character {

    private final String name;
    private final Breed breed;
    private final CharacterClass characterClass;
    private final Inventory inventory;

    private int level;
    private int maximalExperience;
    private int currentExperience;

    private int maximalLife;
    private int currentLife;

    private int maximalEndurance;
    private int currentEndurance;
    
    private int maximalResource;
    private int currentResource;

    private Point position;
    private float moveSpeed;

    private Character target = null;

    private Group group;
    private Raid raid;

    private int treat;
    private Weapon weapon;

    CharacterImpl() {
        
    }

    @Override
    public void attack(AttackStategy attackStategy, Character target) {
        attackStategy.attack(target);
    }

    @Override
    public void escape() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'escape'");
    }

    @Override
    public void wardOff() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'wardOff'");
    }

    @Override
    public void run() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'run'");
    }

    @Override
    public void walk() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'walk'");
    }

    @Override
    public void jump() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'jump'");
    }

    @Override
    public void squat() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'squat'");
    }

    @Override
    public void getUp() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getUp'");
    }

    @Override
    public void lieDown() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'lieDown'");
    }

    @Override
    public void invite(Group group) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'invite'");
    }

    @Override
    public void expel(Group group) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'expel'");
    }

    @Override
    public void invite(Raid raid) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'invite'");
    }

    @Override
    public void expel(Raid raid) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'expel'");
    }

    @Override
    public void focus(Character target) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'focus'");
    }

    @Override
    public void releaseFocus(Character target) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'releaseFocus'");
    }

    @Override
    public Optional<Character> getFocus() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getFocus'");
    }

    @Override
    public Breed getBreed() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getBreed'");
    }

    @Override
    public CharacterClass getCharacterClass() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getCharacterClass'");
    }

    @Override
    public int getLevel() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getLevel'");
    }

    @Override
    public Weapon getWeapon() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getWeapon'");
    }

    @Override
    public SkillsTree getSkillsTree() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getSkillsTree'");
    }

    @Override
    public Inventory getInventory() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getInventory'");
    }

    @Override
    public int getMaximalExperience() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getMaximalExperience'");
    }

    @Override
    public int getCurrentExperience() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getCurrentExperience'");
    }

    @Override
    public void levelUp() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'levelUp'");
    }

    @Override
    public void resetCurrentExperience() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'resetCurrentExperience'");
    }

    @Override
    public Point getPosition() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getPosition'");
    }

    @Override
    public int getThreat() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getThreat'");
    }
    
}
