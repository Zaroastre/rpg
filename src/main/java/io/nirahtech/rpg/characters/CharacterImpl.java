package io.nirahtech.rpg.characters;

import java.util.HashMap;
import java.util.Map;
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

class CharacterImpl<T extends CharacterClass> implements Character<T> {

    private static final int CHARACTER_HITBOX_RADIUS = 10;

    private final String name;

    private final Breed breed;
    private final T characterClass;
    
    private final Faction faction;
    private final Level level;
    private final Life life;
    
    private final Inventory inventory;

    private final Map<Character<? extends CharacterClass>, Threat> threats = new HashMap<>();

    private final HitBox hitBox;
    private final Gender gender;
    private float moveSpeed;

    private Character<? extends CharacterClass> target = null;

    private Group group;
    private Raid raid;

    private Weapon weapon;


    CharacterImpl(
        final String name,
        final Breed breed,
        final T characterClass,
        final Faction faction,
        final Gender gender,
        final Level level,
        final Life life,
        final Inventory inventory
    ) {
        this.name = name;
        this.breed = breed;
        this.faction = faction;
        this.characterClass = characterClass;
        this.level = level;
        this.life = life;
        this.inventory = inventory;
        this.life.winBoost(this.breed.getBaseHealth());
        this.hitBox = new HitBox(new Point(0, 0, 0), CHARACTER_HITBOX_RADIUS);
        this.moveSpeed = 1.1F;
        this.gender = gender;

    }

    @Override
    public void attack(AttackStategy attackStategy, Character<? extends CharacterClass> target) {
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
        this.group = group;
    }

    @Override
    public void expel(Group group) {
        if (this.group.equals(group)) {
            this.group = null;
        }
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
    public void focus(Character<? extends CharacterClass> target) {
        this.target = target;
    }

    @Override
    public void releaseFocus(Character<? extends CharacterClass> target) {
        if (this.target.equals(target)) {
            this.target = null;
        }
    }

    @Override
    public Optional<Character<? extends CharacterClass>> getFocus() {
        return Optional.ofNullable(this.target);
    }

    @Override
    public Breed getBreed() {
        return this.breed;
    }

    @Override
    public T getCharacterClass() {
        return this.characterClass;
    }


    @Override
    public Weapon getWeapon() {
        return this.weapon;
    }

    @Override
    public SkillsTree getSkillsTree() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getSkillsTree'");
    }

    @Override
    public Inventory getInventory() {
        return this.inventory;
    }

    @Override
    public Point getPosition() {
        return this.hitBox.getCenter();
    }

    @Override
    public Optional<Threat> getThreat(Character<? extends CharacterClass> target) {
        return Optional.ofNullable(this.threats.get(target));
    }

    @Override
    public Level getLevel() {
        return this.level;
    }

    @Override
    public Life getLife() {
        return this.life;
    }

    @Override
    public Faction getFaction() {
        return this.faction;
    }

    @Override
    public void follow(Character<? extends CharacterClass> target) {
        
        // TODO Auto-generated method stub
        
    }
    @Override
    public void sprint() {
        // TODO Auto-generated method stub
    }

    @Override
    public void stayInPlace() {
        // TODO Auto-generated method stub
    }

    @Override
    public void goTo(Point point) {
        // TODO Auto-generated method stub
        
    }

    @Override
    public HitBox getHitBox() {
        return this.hitBox;
    }

    @Override
    public boolean isMoving() {
        // TODO Auto-generated method stub
        return false;
    }

    @Override
    public Gender getGender() {
        return this.gender;
    }
    
}
